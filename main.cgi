#!/usr/bin/python3


import sys

sys.path.append('./lib/')

import bottle

from application import main

main(False)

bottle.run(server='cgi')
