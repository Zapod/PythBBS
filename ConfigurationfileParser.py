# Parses configuration files and returns an array in the following format
# 
#
# [ A, B, 1, 2 , 1 , 2, VAL1, VAL2]
# Where 1 is the Key code and 2 is the function
# A is the number of options 
# B is the number of operation specific values 
# VALx are the Values needed for an operation Say a 2 was GOTO, it would need a place to jump
#
#   FUNCTION VALUES
#
# 1 - Go back a Menu -- DEFAULT VALUE, NOT USED HERE OR MODIFIABLE
#
# 2 - GOTO Another Menu
#
# 3 - POST
#
# 4 - SELECT
#
# 5 - LINKTO
#
# 6 - PRINT
#
# 7 - VIEW
class ConfigParse(): #This is the worst speghetti code i've ever written. 
	def __init__(self, Menu):
		self.Menu = Menu
	        self.returnarray = []
	        self.specialarray = [] 

	def Special(self, temp, VAL):
			self.temp = temp
			self.VAL = VAL
                        self.returnarray.append(''.join(self.temp[0].replace(' ', '')))
                        self.temp = self.temp[1].split(' ')
                        self.temp = self.temp[1::] # I'm sorry. I truely am
                        self.returnarray.append(VAL)
			#print ('In Special: ')
			#print (self.temp)
                        self.specialarray.append(self.temp[1])
	def Parse(self):	
		self.config_file = open(('./MenuCONFIG/' + self.Menu + '.config'), 'r')
		self.config_lines = self.config_file.readlines()
		self.config_file.close()
	
		self.linecounter = 0
		self.Additional_Values = 0

		for self.line in enumerate(self.config_lines):
			#print self.line
			self.temp = (self.line[1].rstrip('\n')).split('=')
			#print self.temp


			if '#' in self.line[1]:
				continue
			elif self.linecounter == 0:
				self.temp = (''.join(self.line[1]).split('|'))
				#print self.temp
				self.returnarray.append(int(self.temp[1]))
				self.returnarray.append(0)	
				self.linecounter = 1
				continue
			elif len(self.line) < 2:
				continue
			elif '\n' == self.line[1]:
				continue

                        self.str = ''.join(self.temp[1].replace(' ',''))


			if 'GOTO' in self.str:
				self.Additional_Values += 1
				self.Special(self.temp, 2)

			elif 'POST' in self.str:
				self.returnarray.append(''.join(self.temp[0].replace(' ', '')))
				self.returnarray.append(3)

			elif 'SELECT' in self.str:
				self.Additional_Values += 1
				self.Special(self.temp, 4)
		
			elif 'LINKTO' in self.str:
				self.Additional_Values += 1
				self.Special(self.temp, 5)

			elif 'PRINT' in self.str:
				self.returnarray.append(''.join(self.temp[0].replace(' ', '')))
				self.returnarray.append(6)
				self.temp = self.temp[1].split('-')
				self.temp = self.temp[1::]
				#print('IN PRINT :' )
				#print self.temp
				self.specialarray.append(self.temp[0])				
				self.Additional_Values += 1
			elif 'VIEW' in self.str:
				self.returnarray.append(''.join(self.temp[0].replace(' ', '')))
				self.returnarray.append(7)


			self.linecounter += 1

		self.returnarray[1] = self.Additional_Values
		self.returnarray[0] = (self.linecounter - 1)
		for self.Spec in enumerate(self.specialarray):
			self.returnarray.append(self.Spec[1])

		return self.returnarray


# .............. yeah ....
