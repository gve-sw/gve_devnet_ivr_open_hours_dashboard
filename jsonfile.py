
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

import json
import codecs

class JSONFile():

    def __init__(self, path, codec):

        self.path = path
        self.codec = codec
        self.data = ""


    def read_file(self):

        with codecs.open(self.path, 'r', encoding=self.codec) as file:
            self.data = json.loads(file.read())

        file.close()

        return self.data


    def update_file(self, data):
        
        with codecs.open(self.path, 'w', encoding=self.codec) as file:
            json.dump(data, file, ensure_ascii=False)
        
        file.close()
