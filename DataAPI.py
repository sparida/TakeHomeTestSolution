#!/usr/bin/python3
from Member import Member
import re
import os

# Class to simulate API from text input files
# Along iwth utility functions
class DataAPI:
	DB  = None
	repeatable = None

	def __init__(self, DB = {}, repeatable = True):

		# Database dictionary
		self.DB  = {}
		self.repeatable = repeatable

	# Add memeber to API Database
	def addMember(self, member):
		member_id = member.getID()
		# If repeats are allowed
		if member_id in self.DB and self.repeatable:
			self.DB[member_id].append(member)
		else:
			self.DB[member_id] = [member]

	# Return DB object
	def getDB(self):
		return self.DB

	# Reset DB object
	def resetDB(self):
		self.DB = {}

	# Given member_id return deductible
	def getDeductible(self, member_id):
		if member_id in self.DB:
			return (self.DB[member_id])[0].deductible
		else:
			return None

	# Given member_id return stop_loss
	def getStopLoss(self, member_id):
		if member_id in self.DB:
			return (self.DB[member_id])[0].stop_loss
		else:
			return None

	# Given member_id return oop_max
	def getOOPMax(self, member_id):
		if member_id in self.DB:
			return (self.DB[member_id])[0].oop_max
		else:
			return None

	# Check if entries for a given member_id are consistent
	# Consistency defined as each field has the same result for each entry returned by the API for the same member
	# Hostile witness test :D
	def isConsistentMember(self, member_id):
		if self.repeatable is False:
			return True
		elif member_id in self.DB:
			oop_maxes = set()
			deductibles = set()
			stop_losses = set()
			for m in self.DB[member_id]:
				deductibles.add(m.deductible)
				stop_losses.add(m.stop_loss)
				oop_maxes.add(m.oop_max)
			#print(deductibles, stop_losses, oop_maxes)
			return len(deductibles) == len(stop_losses) == len(oop_maxes) == 1
		else:
			return False

	# Check if all members pass individual member validity tests
	# Tests are defined in class Member: 
	# Currently oop_max > deductible
	# And stop_loss > oop_max
	def isValidMember(self, member_id):
		for m in self.DB[member_id]:
			if not m.isValidMember():
				return False
		return True

	# Check if all members in DB are consistent
	def isConsistentAPI(self):
		for member_id in self.DB:
			if not self.isConsistentMember(member_id):
				return False
		return True

	# Check if all members in DB are valid
	def isValidAPI(self):
		for member_id in self.DB:
			if not self.isValidMember(member_id):
				return False
		return True

	# Check if API is consistent and valid
	def isConsistentAndValidAPI(self):
		return self.isConsistentAPI() and self.isValidAPI()


	# Read API File
	def readAPIFile(self, filename):
		with open(filename, 'r') as f: 
			for line in f:
				if len(line) <= 2:
					continue 
				vals = re.findall('[0-9]+', line)
				m = Member(int(vals[0]), int(vals[1]), int(vals[2]), int(vals[3]))
				self.addMember(m)

	# Write API File
	def writeAPIFile(self, filename):
		writeStr = ''
		with open(filename, 'w') as f: 
			for member_id in self.DB.keys():
				for member in self.DB[member_id]:
					f.write(str(member) + '\n')
        			
if __name__ == '__main__':

	# Test readAPIFile
	DA = DataAPI()
	in_filename = os.path.join('APIFiles', 'api_in.txt')
	out_filename = os.path.join('APIFiles', 'api_out.txt')
	out_filename2 = os.path.join('APIFiles', 'api_out2.txt')


	## Read and write checks
	print('\nPerforming read write API check from txt files')
	
	# Check readAPIFIle
	print('Reading file {}'.format(in_filename))
	DA.readAPIFile(in_filename)

	# Check write API File
	print('Writing {} to {}'.format(in_filename, out_filename))
	DA.writeAPIFile(out_filename)

	# Check read from written file and write to new file
	DA.resetDB()
	print('Reading file {}'.format(out_filename))
	DA.readAPIFile(out_filename)
	print('Writing {} to {}\n'.format(out_filename, out_filename2))
	DA.writeAPIFile(out_filename2)

	# Check consistent member entry
	print('Performing member consistency test')
	member_id = 1234
	print('Member {} entries are consistent: {}\n'.format(member_id, DA.isConsistentMember(member_id))) 

	## Check consistency and validity of APIs
	print('Checking consistency and validity of API')

	for api_num in [1, 2, 3]:
		# Check consistent API and valid API
		in_filename = os.path.join('APIFiles', 'api{}_consistent_valid.txt'.format(api_num))
		DA.resetDB()
		DA.readAPIFile(in_filename)
		print('API ' + in_filename + ':')
		print('Consistent: ' + str(DA.isConsistentAPI()))
		print('Valid : '     + str(DA.isValidAPI()))
		print('')

		# Check consistent API and not valid API
		in_filename = os.path.join('APIFiles', 'api{}_consistent_notvalid.txt'.format(api_num))
		DA.resetDB()
		DA.readAPIFile(in_filename)
		print('API ' + in_filename + ':')
		print('Consistent: ' + str(DA.isConsistentAPI()))
		print('Valid : '     + str(DA.isValidAPI()))
		print('')

		# Check not consistent API and valid API
		in_filename = os.path.join('APIFiles', 'api{}_notconsistent_valid.txt'.format(api_num))
		DA.resetDB()
		DA.readAPIFile(in_filename)
		print('API ' + in_filename + ':')
		print('Consistent: ' + str(DA.isConsistentAPI()))
		print('Valid : '     + str(DA.isValidAPI()))
		print('')

		# Check not consistent API and not valid API
		in_filename = os.path.join('APIFiles', 'api{}_notconsistent_notvalid.txt'.format(api_num))
		DA.resetDB()
		DA.readAPIFile(in_filename)
		print('API ' + in_filename + ':')
		print('Consistent: ' + str(DA.isConsistentAPI()))
		print('Valid : '     + str(DA.isValidAPI()))
		print('')