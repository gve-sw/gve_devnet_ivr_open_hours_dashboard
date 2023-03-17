""" Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

# Import Section
import os
import identity
import identity.web
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_session import Session
from functools import wraps
from dotenv import load_dotenv

from jsonfile import JSONFile
from logger import LogFile
from datahandler import DataHandler
import app_config

load_dotenv()

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


auth = identity.web.Auth(
    session=session,
    authority=app.config.get("AUTHORITY"),
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
)


'''
Decorator for routes that require authentication via Microsoft
'''
def auth_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        if auth.get_user():
            return fn(*args, **kwargs)
        else:
            return redirect(auth.log_out(url_for("login", _external=True)))
    return decorated


'''
Login page route
'''
@app.route('/', methods=['GET'])
def login():
    try:
        if request.method == 'GET':

            if auth.get_user():   
                return redirect(url_for("main"))

            else:
                return render_template('login.html', show_main_menu=False, **auth.log_in(
                                        scopes=app_config.SCOPE, # Have user consent to scopes during log-in
                                        redirect_uri=url_for("auth_response", _external=True), # Optional. If present, this absolute URL must match your app's redirect_uri registered in Azure Portal
                                        ))

    except Exception as e: 
        flash(f"Error occured: {e}")
        return render_template('login.html', show_main_menu=False)


'''
App response route
'''
@app.route(app_config.REDIRECT_PATH)
def auth_response():

    result = auth.complete_log_in(request.args)

    if "error" in result:
        flash(f"Error occured: {result}")
        return redirect(url_for("login"))

    app.logger.info(f"User logging in - User: {result['name']}")

    return redirect(url_for("main"))


'''
Main page frame route
'''
@app.route('/main', methods=['GET'])
@auth_required
def main():

    username=auth.get_user()['name']

    try: 
        
        location_id = ""
        if 'location_id' in session:
            location_id = session['location_id']   
        
        ivr_data = IVR_JSON_FILE.read_file()

        return render_template('main.html', show_main_menu=True, ivr_data = ivr_data, selected_location_id=location_id, username=username)
    
    except Exception as e: 
        flash(f"Error occured: {e}")
        return render_template('main.html', show_main_menu=True, ivr_data = [], username=username)


'''
Location section route - part of main page
'''
@app.route('/location', methods=['GET'])
@app.route('/location/<id>', methods=['GET'])
@auth_required
def location(id=None):

    username=auth.get_user()['name']

    try:
        
        location_id = request.view_args['id']
        session['location_id'] = location_id

        ivr_data = IVR_JSON_FILE.read_file()

        location_IVR_data = DataHandler.filter_data_for_location(location_id, ivr_data)

        return render_template('location_data.html', selected_location_id=location_id, selected_location_IVR_data=location_IVR_data, username=username)
        
    except Exception as e: 
        flash(f"Error occured: {e}")
        return render_template('location_data.html', selected_location_id=None, selected_location_IVR_data=[], username=username)


'''
Route for updating location hours
'''
@app.route('/hours_update', methods=['GET','POST'])
@app.route('/hours_update/<id>', methods=['GET','POST'])
@auth_required
def hours_update(id=None):
    try:
        ivr_data = IVR_JSON_FILE.read_file()

        location_id = request.view_args['id']
        location_IVR_data = DataHandler.filter_data_for_location(location_id, ivr_data)
        username = auth.get_user()['name']

        updated_location_IVR_data = location_IVR_data.copy()
        ivr_data_copy_to_update = []

        day_abb = request.form.get("day_abb")
        fe_open = request.form.get("fe_open")
        fe_close = request.form.get("fe_close")
        rx_open = request.form.get("rx_open")
        rx_close = request.form.get("rx_close")

        previous_fe_open = location_IVR_data[location_id]['Hours'][day_abb]['Open']
        previous_fe_close = location_IVR_data[location_id]['Hours'][day_abb]['Close']
        previous_rx_open = location_IVR_data[location_id]['RXHours'][day_abb]['Open']
        previous_rx_close = location_IVR_data[location_id]['RXHours'][day_abb]['Close']

        updated_location_IVR_data[location_id]['Hours'][day_abb]['Open'] = fe_open
        updated_location_IVR_data[location_id]['Hours'][day_abb]['Close'] = fe_close
        updated_location_IVR_data[location_id]['RXHours'][day_abb]['Open'] = rx_open
        updated_location_IVR_data[location_id]['RXHours'][day_abb]['Close'] = rx_close

        ivr_data_copy_to_update = DataHandler.update_data_for_location(location_id, ivr_data, updated_location_IVR_data)
        IVR_JSON_FILE.update_file(ivr_data_copy_to_update)
        ivr_data = IVR_JSON_FILE.read_file()

        app.logger.info(f"Opening Hours changed - User: {username}, Location {location_id}, Day: {day_abb}, Change: FE Open: {previous_fe_open} -> {fe_open}, FE Close: {previous_fe_close} -> {fe_close}, RX Open: {previous_rx_open} -> {rx_open}, RX Close: {previous_rx_close} -> {rx_close}")
        
        flash('Opening hours successfully updated')

        session['location_id'] = location_id

        return redirect(url_for("main"))

    except Exception as e: 
        flash(f"Error occured: {e}")
        return redirect(url_for("main"))


'''
Route for updating location emergency settings
'''
@app.route('/update_emergency_settings', methods=['GET','POST'])
@app.route('/update_emergency_settings/<id>', methods=['GET','POST'])
@auth_required
def update_emergency_settings(id=None):
    
    try:
        ivr_data = IVR_JSON_FILE.read_file()
    
        location_id = request.view_args['id']
        location_IVR_data = DataHandler.filter_data_for_location(location_id, ivr_data)
        username = auth.get_user()['name']
    
        updated_location_IVR_data = location_IVR_data.copy()
        ivr_data_copy_to_update = []

        triggered_emergency_action = request.form['emergency_button']
        updated_setting_key_value_list = triggered_emergency_action.split("__")
        updated_setting_key = updated_setting_key_value_list[0]
        updated_setting_val = int(updated_setting_key_value_list[1])

        previous_emergency_value = location_IVR_data[location_id][updated_setting_key]

        updated_location_IVR_data[location_id][updated_setting_key] = updated_setting_val

        ivr_data_copy_to_update = DataHandler.update_data_for_location(location_id, ivr_data, updated_location_IVR_data)
        IVR_JSON_FILE.update_file(ivr_data_copy_to_update)

        app.logger.info(f"Emergeny Close settings changed - User: {username}, Location {location_id}, Change: {updated_setting_key}: {previous_emergency_value} -> {updated_setting_val}")

        flash('Emergency settings successfully updated')
        
        location_id = session['location_id']
        
        return redirect(url_for("main"))

    except Exception as e: 
        flash(f"Error occured: {e}")
        return redirect(url_for("main"))

'''
Route for logs page
'''
@app.get("/logs")
@auth_required
def logs():
    
    try:
        global LOG_FILE
        
        logs = LOG_FILE.read_file()

        username=auth.get_user()['name']

        return render_template('logs.html', show_main_menu=True, logs= logs, username=username)

    except Exception as e: 
        print(f"Error occured: {e}")


'''
Route for logout
'''
@app.route("/logout")
def logout():

    username=auth.get_user()['name']

    app.logger.info(f"User logging out - User: {username}")

    session.clear()

    return redirect(auth.log_out(url_for("login", _external=True)))


if __name__ == "__main__":

    CONFIG_PATH = os.environ['CONFIG_PATH']

    IVR_JSON_FILE = JSONFile(CONFIG_PATH, "utf-8-sig")
    LOG_FILE = LogFile("logs.log")

    app.run(host='0.0.0.0', debug=True)



