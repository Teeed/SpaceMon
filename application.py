# -*- coding: utf-8 -*-

# Appplication that responds to SpaceAPI [http://spaceapi.net] requests
# Copyright (C) 2013 Tadeusz Magura-Witkowski
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging
logging.basicConfig(level=logging.ERROR)

import os
import sys
import json
from typing import Callable, Dict

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

import copy
import configparser
from copy import deepcopy
from threading import Thread
from bottle import route, run, response

config = configparser.ConfigParser()
config.read(('localconfig.cfg'))

yamldata = ''
with open(config.get('data', 'file'), 'r') as f:
	yamldata = f.read()

yamldata = load(yamldata, Loader=Loader)

def main(run_server=True):
	modules_enabled: Dict[str, Callable[[dict], dict]] = {}

	for module_name, enabled in config.items('modules'):
		if config.getboolean('modules', module_name):
			try:
				__import__('modules.%s' % module_name)
				module = sys.modules['modules.%s' % module_name]
				function_pointer = getattr(module, 'update_document')

				if not callable(function_pointer):
					logging.warning('modules.%s.update_document is not callable!', module_name)
					continue

				modules_enabled[module_name] = function_pointer

			except ImportError as e:
				logging.warning('can not import module "%s": %s', module_name, str(e))

	logging.info('Loaded modules: %s', ', '.join(modules_enabled.keys()))

	@route('/')
	def index():
		data = copy.deepcopy(yamldata)

		mods_ok: set[str] = set([])
		mods_fail: set[str] = set([])

		# will exec modules 
		# or exec merge for threaded modules
		for module_name, function_pointer in modules_enabled.items():
			new_data = None
			try:
				new_data = function_pointer(copy.deepcopy(data))
				data = new_data

				mods_ok.add(module_name)
			except:
				logging.exception('module "%s" failed', module_name)
				mods_fail.add(module_name)

		# response.charset = 'utf8'
		response.set_header('Content-Type', 'application/json')
		response.set_header('Access-Control-Allow-Origin', '*')
		response.set_header('Cache-Control', 'max-age=60')
		
		if mods_ok:
			response.set_header('X-Used-Modules', ','.join(mods_ok))

		if mods_fail:
			response.set_header('X-Failed-Modules', ','.join(mods_fail))
		
		return json.dumps(data)

	if run_server:
		run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=config.getboolean('application', 'debug'))

if __name__ == '__main__':
	main()
