# Program to view posts 
#
# Implement it to show title later
#
#
class MessageView():
	def __init__(self, client):
		self.client = client

	def View(self, base):
		self.base = base

		self.client.send('View Post (V), View Posts list (L), Exit (E): ')
		self.data = self.client.recv(1024).rstrip().upper()
		if self.data == 'L':

			self.client.send('How many rows to display? ')
			
			try:
				self.termrows = int(self.client.recv(1024).rstrip())
			except:
				self.termrows = 25
		
			self.Tree = open(('./Posts/' + self.base + '/MessageTree.dat'), 'r')
			self.MesTree = self.Tree.readlines()
			self.Tree.close()
			self.i = 0
		
			for self.line in self.MesTree: # Shows Posts in base
				if self.i >= self.termrows:
					self.client.recv(512)
					self.client.send('Show More? ')
					self.data = self.client.recv(1024).rstrip().upper()

					if self.data == 'Y':
						self.client.send(self.line)
						self.i = 0
					elif self.data == 'N':
						break
					else:
						self.client.send('Unkown command, exiting')
		
				else: 
					self.client.send(self.line)
				self.i += 1
		elif self.data == 'V':
			self.client.send('Post Number? ')
                        self.data = self.client.recv(1024)

			try:
				self.post = open(('./Posts/' + self.base + '/' + (self.data.rstrip().replace(' ' , "" )) + '.txt' ), 'r')
				self.postr = self.post.readlines()
				self.post.close()
			except:
				self.client.send('Post' + self.data + ' Not Found')
				self.client.recv(1024)
				return 0
                        self.client.send('How many rows to display? ')
 			try:
	                       self.termrows = int(self.client.recv(1024).rstrip())
			except:
				self.termrows = 25
			self.client.send("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
			self.i = 0
			for self.lines in self.postr:
				self.client.send(self.lines)
				if self.i >= self.termrows:
					self.client.recv(512)
                     		self.i += 1

		elif self.data == 'Q':
			return 0

		else:	
			return 1		

		self.client.recv(512)
		return 0
