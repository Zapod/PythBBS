#		PYTHBBS - A Python BBS Server
#
#
# Copyright (c) 2017, <REDACTED>
#  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the PythBBS nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <REDACTED>  BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import getopt
import socket
#import curses  -- Will use for custom SSH interface 
import sys
import threading
from threading import Thread
import datetime

#import code files
import MessageEditor
import ConfigurationfileParser
import MessageViewer

#import os
#from server import Server
'P', 6

#_TELNETPORT 
#_SSHPORT
#_SSH
#_MAXCONNECTIONS

BUFFER = 1024
VERSION = "PythBBS version: 1"
FILEPATH = './' #Gives the file path, used for dealing with Menus and config files
CLEARTERM = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'

# MAKE CONFIG FILE BE READ AND GIVE THESE VALUES
MAINMENU = './Menus/Main.mnu'





class MenuHandler():
		def __init__(self, client):
			self.client = client
	
		#def FindMenu(self, MenuNum):
		#	self.MenuNum = MenuNum
		#	if self.MenuNum == 2:
		#		self.MenuDisplay(MAINMENU)
		
		def MenuDisplay(self, Menu): # Menu display, takes location of menu to display
			self.client.send(CLEARTERM)
			self.location = Menu
			#print self.location
			self.MainFile = open(('./Menus/' + self.location + '.mnu'), 'r') # Opensmenu and sends it to connected client
			#print('./Menus/' + self.location + '.mnu')
			for self.line in self.MainFile.readlines():
				self.client.send(self.line)
			self.MainFile.close()
		
		def GoodBye(self): # Seperate Goodbye display, incase additional functions are desired
			self.client.send(CLEARTERM)
			self.GoodByeSplash = open('./Menus/GoodByeSplash.mnu', 'r')

			for self.line in self.GoodByeSplash.readlines():
					self.client.send(self.line)

			self.GoodByeSplash.close()


class ResponseHandler(): 
	def __init__(self, client):
		self.bool = 2
		self.op = 0
		self.current= ''
		self.client = client
		self.base = 'General'
	def Menu_Select(self, response, CurrentMenu, base):
		self.bool = 2
		self.current = CurrentMenu
		self.response = (''.join(response).upper()).rstrip() # Formats Character to specificatiom
		if self.response == 'Q':
			return [1, 0]

		self.parser = ConfigurationfileParser.ConfigParse(self.current)
		self.oparray = self.parser.Parse()
		
		self.MessageRead = MessageViewer.MessageView(self.client)
		#print self.oparray
		self.inc = 3
		self.l = 1
		while (self.bool / 2) <= self.oparray[0]:
			#print self.oparray[self.bool]
			#print self.bool
			#print self.inc
			#print self.oparray[self.inc]
			if self.response == self.oparray[self.bool]: 
				self.op = self.oparray[self.inc]
				#print self.op
				if self.op == 6:
					self.client.send(self.oparray[(((self.oparray[0] * 2 + 1)) + self.l)])
					#self.l += 1
					break
				elif self.op == 2:
					self.current = self.oparray[(((self.oparray[0] * 2) + 1) + self.l)]
					#self.l += 1
					break
	
				elif self.op == 3:
					self.edit = MessageEditor.MessageEdit(self.client, 'anon', self.base)
					self.edit.Editor()
					break

				elif self.op == 4:
					self.base = self.oparray[(((self.oparray[0] * 2) + 1) + self.l)]
					#print self.base
					#self.l += 1
					break	
				elif self.op == 5:
					self.client.send(CLEARTERM)
					self.file = self.oparray[(((self.oparray[0] * 2) + 1) + self.l)]
					self.bullit = open(('./TextFiles/' + self.file + '.txt'), 'r')
					self.file = self.bullit.readlines()
					self.file.close()
					for self.line in self.bullit.readlines():
						self.client.send(self.line)
					self.client.recv(512)

				elif self.op == 7:
					self.MessageRead.View(self.base)
			if str(self.oparray[self.inc]) in '6 2 4':
				self.l += 1
			self.bool += 2
                	self.inc += 2
	
		self.bool = [self.op, self.current, self.base]
		return self.bool

# class Login:



class ThreadedFUNC(threading.Thread): # Opens thread for clients
	def __init__(self, connection, address):
		threading.Thread.__init__(self)
		self.client = connection
		self.addr = address
		self.Pass = [0, 'Main', 'General']
		self.MenuHandler = MenuHandler(self.client)
		self.ResponseHandler = ResponseHandler(self.client)
	def run(self):
		while self.Pass[0] != 1:
			self.MenuHandler.MenuDisplay(self.Pass[1])
			self.client.send('$>')
			self.Response = self.client.recv(2048)
			self.Pass = self.ResponseHandler.Menu_Select(self.Response, self.Pass[1], self.Pass[2])
		self.MenuHandler.GoodBye()	
		self.client.close()

def main(argv):

	# Handles Command line Arguments 
	global _SSH
	try:
		opts, args = getopt.getopt(argv, "hvn:m:so:", ["help", "version", "telnet-port=", "--ssh-port="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-v", "--version"):
			print VERSION
			sys.exit(2)
		elif opt in ("-m", "--telnet-port"):
			global _TELNETPORT
			_TELNETPORT = int(arg)
		elif opt in ("-n", "--ssh-port"):
			global _SSHPORT 
			_SSHPORT = int(arg)
		elif opt == "-s":
			_SSH = 1
		elif opt == "-o":
			global _MAXCONNECTIONS
			_MAXCONNECTIONS = int(arg)
		elif args == NULL:
			print "NO COMMANDS SPECIFIED \n"
			usage()
			sys.exit(2)
		elif _SSH != 1:
			_SSH = 0
			
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind(('0.0.0.0', _TELNETPORT))  # Creates port open for Telnet Connections
	serversocket.listen(_MAXCONNECTIONS)
	print 'Server Running'
	while True:
		(socketconnection, address) = serversocket.accept()	
		ClientThread = ThreadedFUNC(socketconnection, address) #Starts new client thread, passes socket connection
		ClientThread.start() 
		print('NEW CONNECTION AT: ' + datetime.datetime.now().strftime("%m-%d-%H-%M")) # system out for logging 


def usage(): #Simply the Usage terms
	print "            Available Command Line Arguments are: \n "
	print " --help / -h: "
	print "         Display help \n"
	print " -v / --version: "
	print "         Display Version \n"
	print " -m / --telnet-port: "
	print "         Port to run telnet server, 23 by default \n"
	print " -s:"
	print "         Enable SSH support, disabled by defualt \n"
	print " -n / --ssh-port: "
	print "         Port to run ssh server, 22 by default \n"
	print " -o : "
	print "		Max Connections allowed\n"


	

if __name__ == "__main__":
	main(sys.argv[1:])
