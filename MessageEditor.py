# Message editing Program
# I am disapointed at myself with this code I wrote


CLEARTERM = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
BUFFER = 8192

class MessageEdit():
	def __init__(self, client, user, base):
		self.client = client
		self.user = user
		self.base = base
	def Editor(self):
		self.linenum = 0
		self.input = []
	
		# Gets Title for post
		self.client.send(CLEARTERM + 'Title? ')
		self.title = self.client.recv(512)
		self.client.send(CLEARTERM)
 		self.quit = 0
		# MESSAGE EDITOR SECTION WITH USE INPUT
                self.client.send('              MESSAGE EDITOR                  \n')
                self.client.send('              /s to post \n\n\n\n\n\n\n\n')
		while self.quit != 1 :#looks for '/s' which dictates a post
			self.client.send(':')
			self.lineinput = self.client.recv(BUFFER)	
			if '/S' in  ((''.join(self.lineinput).upper()).replace(' ', '')).replace('\n', ''):
				self.quit = 1
				break
			self.input.append(self.lineinput)
                        self.linenum += 1


		#Gets all lines from Message Tree of the base 
		self.MessageTree = open(('./Posts/' + (self.base) + '/MessageTree.dat'), 'r')		
		self.lines = self.MessageTree.readlines()
		self.MessageTree.close()
		
		# Gets post number of last post to the base
		self.lines = ''.join(self.lines[-1]).split('|')
		print self.lines
		if self.lines[0].replace(' ', '') != '\n':
			self.lines = int(self.lines[0])
		else:
			self.lines = 0
		print self.lines
		# Appends to Message Tree File and adds File listing
		self.MessageTree = open(('./Posts/' + (self.base) + '/MessageTree.dat'), 'a')
		self.MessageTree.write(str((self.lines + 1)) + ' | ' + self.user + ' | ' + self.title)
		self.MessageTree.close()
		
		# Opens New file post and posts
		self.Post_File = open(('./Posts/' + self.base + '/' + str(self.lines) + '.txt'), 'w')
		for self.line in enumerate(self.input):
			self.Post_File.write(self.line[1])
		self.Post_File.close()
						
