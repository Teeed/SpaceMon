# coding: utf-8

__version__ = 1.0
__cacheable__ = True

import urllib.request, urllib.error, urllib.parse
import json
import configparser
from application import config

CONFIG_KEY = 'module_temp'


def update_document(data):
	remote = urllib.request.urlopen(config.get(CONFIG_KEY, 'url'), timeout=config.getint(CONFIG_KEY, 'timeout'))

	if not data.get('sensors'):
		data['sensors'] = {}

	if not data['sensors'].get('temperature'):
		data['sensors']['temperature'] = []

	sensor = {
		'value': float(remote.read()),
		'unit': '°C',
		'location': 'Inside',
	}

	data['sensors']['temperature'].append(sensor)

	return data