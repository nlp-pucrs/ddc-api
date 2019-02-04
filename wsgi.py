#!/usr/bin/python
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

##Virtualenv Settings
activate_this = os.path.join(BASE_DIR,'ddc-api/apienv/bin/activate_this.py')
with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

##Replace the standard out
sys.stdout = sys.stderr

##Add this file path to sys.path in order to import settings
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

##Add this file path to sys.path in order to import app
sys.path.append(os.path.join(BASE_DIR,'ddc-api/'))


##Create appilcation for our app
from ddcapi import app as application
