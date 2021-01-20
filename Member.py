#!/usr/bin/python3

# Class to store individual API entries
class Member:
	# 4 Fields in member
	member_id  = None
	deductible = None
	stop_loss  = None
	oop_max   = None


	def __init__(self, member_id, deductible, stop_loss, oop_max):
		self.member_id  = member_id
		self.deductible = deductible
		self.stop_loss  = stop_loss
		self.oop_max   = oop_max

	def __hash__(self):
		return hash(self.member_id)

	def __eq__(self, another):
		return hasattr(another, 'member_id') and self.member_id == another.member_id

	# Returns memeberID
	def getID(self):
		return self.member_id

	# String represantation of Memner object
	def __str__(self):
		string  = str(self.member_id) + ': {'
		string += 'deductible: ' + str(self.deductible) + ', '
		string += 'stop_loss: '  + str(self.stop_loss)  + ', '
		string += 'oop_max: '   + str(self.oop_max)   + '}'
		return string

	# Function to perform individual tests on members
	def isValidMember(self):

		# Is out of pocket max greater than deductible
		if self.deductible > self.oop_max: 
			return False

		# Is stop loss greater than out of pocket max
		if self.oop_max > self.stop_loss: 
			return False

		# Add further tests here

		return True


if __name__ == '__main__':

	# Initialization Test
	print('\nInitialization Test')
	m = Member(member_id = 1, deductible = 6000, stop_loss = 13000, oop_max = 6000)
	print('Member: ' + '\n' + str(m))
	print('')

	# Validity Test
	m = Member(member_id = 1, deductible = 6000, stop_loss = 13000, oop_max = 600)
	print('Validity Test')
	print('Member: ' + '\n' + str(m))
	print('Member Valid: ', m.isValidMember())
	print('')
