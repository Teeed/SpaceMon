__version__ = 1.0
__cacheable__ = True

import json
import configparser
from application import config

def update_document(data):
       if not data.get('state'):
           data['state'] = {}
           
       data['open'] = data['state'].get('open', False)

       return data
