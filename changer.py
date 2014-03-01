"""
Copyright (c) <2014> <Sindre Knudsen Smistad>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
This short script is used to change the description of the random channel on my
Teamspeak server. It randomly selects a image in a directory and sets the
description of the channel to that image. The script should be easy to modify
to change the behavior. 
"""
import ts3
from os import listdir
from os.path import isfile, join
import random
import shutil
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('serveradmin', action='store',
                help='Username of the serveradmin', default="serveradmin")
parser.add_argument('password', action='store',
                help='Password of the serveradmin', default=None)
parser.add_argument('webpath', action='store',
                help='Path to the web directory storing the images.', default=None)
parser.add_argument('basic_url', action='store',
                help='The public url to the webpath.', default=None)

results = parser.parse_args()

web_path = results.webpath
basic_url = results.basic_url
username = results.serveradmin
password = results.password

while True:
	onlyfiles = [ f for f in listdir(web_path) if isfile(join(web_path,f)) ]
	img = random.choice(onlyfiles)

	# This is the what the description will be set too.
	description = "[IMG]%s[/IMG]" % (basic_url+img)

	# Server info change the port and address to what you need.
	server = ts3.TS3Server('127.0.0.1', 10011)
	server.login(username, password)

	# Which virtualserver to use
	server.use(1)

	# Set cid to the channel you want to modify.
	response = server.send_command('channeledit', keys={'cid': '4', 'channel_description': description})
	#print(response)

	# Time to sleep before changing the description again.
	time.sleep(60*60*5)
