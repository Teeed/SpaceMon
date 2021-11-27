__version__ = 1.0
__cacheable__ = True

import urllib.request, urllib.error, urllib.parse
import json
import time
from application import config

from datetime import timezone
import datetime


def utc_epoch() -> int:
	dt = datetime.datetime.now(timezone.utc)
	
	utc_time = dt.replace(tzinfo=timezone.utc)
	return int(utc_time.timestamp())

CONFIG_KEY = 'module_mqtt2json_open'

def update_document(data):
	remote = urllib.request.urlopen(config.get(CONFIG_KEY, 'url'), timeout=config.getint(CONFIG_KEY, 'timeout')).read()
	remote = json.loads(remote)

	if remote['zm/hs_active']['timestamp'] < utc_epoch() - 120:
		return data

	is_open = remote['zm/hs_active']['payload'] == 1
	
	if not data.get('sensors'):
		data['sensors'] = {}

	if not data.get('state'):
		data['state'] = {'open': False}

	data['state']['open'] |= is_open 

	return data

