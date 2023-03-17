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

class DataHandler():

    @staticmethod
    def filter_data_for_location(location_id, IVR_DATA):
        return [element for element in IVR_DATA.copy() if location_id in element][0]


    @staticmethod
    def update_data_for_location(location_id, IVR_DATA, updated_location_IVR_data):

        ivr_data_copy_to_update = IVR_DATA.copy()

        for index, element in enumerate(IVR_DATA.copy()):
            if location_id in element:
                                
                ivr_data_copy_to_update[index].update(updated_location_IVR_data)
                return ivr_data_copy_to_update
