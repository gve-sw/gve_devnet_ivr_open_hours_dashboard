
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

import logging

class UserInteractionFilter(logging.Filter):
    def filter(self, record):
        return 'INFO app:' in record.getMessage()


logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(levelname)s %(name)s: %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger("werkzeug").addFilter(UserInteractionFilter())


class LogFile():

    def __init__(self, path):
        self.path = path

    def read_file(self):

        lines = []

        with open(self.path) as file:
            lines = [ line.strip( "\n") for line in file ]
            lines_filtered = [  x for x in lines if "INFO app" in x  ]
            lines_filteres_formatted = [ line.strip( "INFO app: ") for line in lines_filtered ]

        file.close()

        return lines_filteres_formatted



