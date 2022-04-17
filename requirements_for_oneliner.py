#!/usr/bin/env python3

try:
    import netifaces
    from argparse import ArgumentParser
    import urllib.parse
	from base64 import *
	import codecs
except ImportError:
    import os
    os.system('clear')
    os.system('pip3 install argparse')
    os.system('pip3 install netifaces')
    os.system('pip3 install urllib.parse')
    os.system('pip3 install base64')
    os.system('pip3 install codecs')
    os.system('clear')