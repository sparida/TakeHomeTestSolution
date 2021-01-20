#!/usr/bin/python3

import os
import re
from statistics import mode
from DataAPI import DataAPI
from Member import Member

debug_print = False

# Implements various policies to determine true deductible
class Policies:
	
	DB1 = None
	DB2 = None
	DB3 = None
	fieldPriority = None
	policyPriority = None

	def __init__(self, DB1 = None, DB2 = None, DB3 = None):
		self.DB1 = DB1
		self.DB2 = DB2
		self.DB3 = DB3

	def loadDBs(self, infile1, infile2, infile3):
		# Reinitialize DBs
		self.DB1 = DataAPI()
		self.DB2 = DataAPI()
		self.DB3 = DataAPI()

		# Read API Files
		self.DB1.readAPIFile(infile1)
		self.DB2.readAPIFile(infile2)
		self.DB3.readAPIFile(infile3)

	def returnConsistentAPIs(self, APIList):
		consistent_APIs = []
		for db in APIList:
			if db.isConsistentAPI():
				consistent_APIs.append(db)
		return consistent_APIs

	def returnValidAPIs(self, APIList):
		valid_APIs = []
		for db in APIList:
			if db.isValidAPI():
				valid_APIs.append(db)
		return valid_APIs

	# Specify which API to trust and in what order 
	def simplePolicy(self, member_id, api_priority_order = [1, 3, 2], check_consistency = False,  check_validity = False):
		APIList = [self.DB1, self.DB2, self.DB3]

		# Restrutcure based on priority
		APIList = [APIList[api_priority_order[i] - 1] for i in list(range(3))]

		if check_consistency:
			APIList = self.returnConsistentAPIs(APIList)

		if check_validity:
			APIList = self.returnValidAPIs(APIList)

		if len(APIList) > 0:
			return(APIList[0].getDeductible(member_id))	
		else:
			return ("No DB is consistent and valid")

	# Define a policy based on funcs to use for filtering each field
	def funcFieldPolicy(self, member_id, field_priority_order = ['deductible', 'stop_loss', 'oop_min'], funcs = [min, min, min], check_consistency = False,  check_validity = False):
		APIList = [self.DB1, self.DB2, self.DB3]

		if check_consistency:
			APIList = self.returnConsistentAPIs(APIList)

		if check_validity:
			APIList = self.returnValidAPIs(APIList)

		if len(APIList) > 0:
			dS  = [APIList[i].getDeductible(member_id) for i in range(len(APIList))]
			slS = [APIList[i].getStopLoss(member_id) for i in range(len(APIList))]
			omS = [APIList[i].getOOPMax(member_id) for i in range(len(APIList))]
			#print(dS, slS, omS)

			valDict = {'deductible':dS, 'stop_loss': slS, 'oop_max':omS}
			vals = [valDict[fpo] for fpo in field_priority_order]
			v1 = vals[0]
			v2 = vals[1]
			v3 = vals[2]

			if debug_print:
				print([f.__name__ for f in funcs])

			# Check for 1st field
			if debug_print:
				print(v1, v2, v3)
			func_val = funcs[0](v1)
			val_inds = [i for i,val in enumerate(v1) if val == func_val]
			if len(val_inds) == 1:
				if debug_print:
					print(1, 'if')
				return dS[val_inds[0]]
			else:
				if debug_print:
					print(1, 'else')	
				dS  = [dS[i]  for i in range(len(dS)) if i in val_inds]
				slS = [slS[i] for i in range(len(slS))if i in val_inds]
				omS = [omS[i] for i in range(len(omS))if i in val_inds]
				v1  = [v1[i]  for i in range(len(v1)) if i in val_inds]
				v2  = [v2[i]  for i in range(len(v2)) if i in val_inds]
				v3  = [v3[i]  for i in range(len(v3)) if i in val_inds]

			# Check for 2nd field
			if debug_print:
				print(v1, v2, v3)
			func_val = funcs[1](v2)
			val_inds = [i for i,val in enumerate(v2) if val == func_val]
			if debug_print:
				print(val_inds)
			if len(val_inds) == 1:
				if debug_print:
					print(2, 'if')	
				return dS[val_inds[0]]
			else:	
				if debug_print:
					print(2, 'else')	
				dS  = [dS[i]  for i in range(len(dS)) if i in val_inds]
				slS = [slS[i] for i in range(len(slS))if i in val_inds]
				omS = [omS[i] for i in range(len(omS))if i in val_inds]
				v1  = [v1[i]  for i in range(len(v1)) if i in val_inds]
				v2  = [v2[i]  for i in range(len(v2)) if i in val_inds]
				v3  = [v3[i]  for i in range(len(v3)) if i in val_inds]

			# Check for 3rd field
			# print(v1, v2, v3)
			func_val = funcs[2](v3)
			val_inds = [i for i,val in enumerate(v3) if val == func_val]
			if len(val_inds) == 1:
				if debug_print:	
					print(3, 'if')	
				return dS[val_inds[0]]
			else:
				if debug_print:	
					print(3, 'else')	
				dS  = [dS[i]  for i in range(len(dS)) if i in val_inds]
				slS = [slS[i] for i in range(len(slS))if i in val_inds]
				omS = [omS[i] for i in range(len(omS))if i in val_inds]
				v1  = [v1[i]  for i in range(len(v1)) if i in val_inds]
				v2  = [v2[i]  for i in range(len(v2)) if i in val_inds]
				v3  = [v3[i]  for i in range(len(v3)) if i in val_inds]

			return dS[val_inds[0]]

		else:
			return ("No DB is consistent and valid")

	# Define a policy based on min value of a certain field
	def maxFieldPolicy(self, member_id, field_priority_order = ['deductible', 'stop_loss', 'oop_min'], check_consistency = False,  check_validity = False):
		funcs = [max, max, max]
		return self.funcFieldPolicy(member_id, field_priority_order = field_priority_order, funcs = funcs, check_consistency = check_consistency,  check_validity = check_validity)


	# Define a policy based on min value of a certain field
	def minFieldPolicy(self, member_id, field_priority_order = ['deductible', 'stop_loss', 'oop_min'], check_consistency = False,  check_validity = False):
		funcs = [min, min, min]
		return self.funcFieldPolicy(member_id, field_priority_order = field_priority_order, funcs = funcs, check_consistency = check_consistency,  check_validity = check_validity)

	# Define a policy based on min value of a certain field
	def modeFieldPolicy(self, member_id, field_priority_order = ['deductible', 'stop_loss', 'oop_min'], check_consistency = False,  check_validity = False):
		funcs = [mode, mode, mode]
		return self.funcFieldPolicy(member_id, field_priority_order = field_priority_order, funcs = funcs, check_consistency = check_consistency,  check_validity = check_validity)

if __name__ == '__main__':
	p = Policies()

	# Simple Policy Test
	infile1  = os.path.join('APIFiles', 'api1_consistent_notvalid.txt')
	infile2  = os.path.join('APIFiles', 'api2_consistent_valid.txt')
	infile3  = os.path.join('APIFiles', 'api3_consistent_notvalid.txt')
	p.loadDBs(infile1, infile2, infile3)

	member_id = 1234
	result = p.simplePolicy(member_id, api_priority_order = [3, 1, 2], check_consistency = True,  check_validity = True)
	print('Testing simple policy')
	print('Member Deductible: ', result)
	print('')

	# Max Field Policy Test #1
	infile1  = os.path.join('APIFiles', 'api1_consistent_valid.txt')
	infile2  = os.path.join('APIFiles', 'api2_consistent_valid.txt')
	infile3  = os.path.join('APIFiles', 'api3_consistent_valid.txt')
	p.loadDBs(infile1, infile2, infile3)
	member_id = 1234
	field_priority_order = ['stop_loss', 'deductible', 'oop_max']
	result = p.maxFieldPolicy(member_id, field_priority_order = field_priority_order, check_consistency = False,  check_validity = False)
	print('Testing max field policy with field_priority_order:', field_priority_order)
	print('Member Deductible: ', result)
	print('')

	# Min Field Policy Test #1
	infile1  = os.path.join('APIFiles', 'api1_consistent_valid.txt')
	infile2  = os.path.join('APIFiles', 'api2_consistent_valid.txt')
	infile3  = os.path.join('APIFiles', 'api3_consistent_valid.txt')
	p.loadDBs(infile1, infile2, infile3)
	member_id = 1234
	field_priority_order = ['oop_max', 'stop_loss', 'deductible']
	result = p.minFieldPolicy(member_id, field_priority_order = field_priority_order, check_consistency = False,  check_validity = False)
	print('Testing min field policy with field_priority_order:', field_priority_order)
	print('Member Deductible: ', result)
	print('')

	# Func Field Policy Test #1
	infile1  = os.path.join('APIFiles', 'api1_consistent_valid.txt')
	infile2  = os.path.join('APIFiles', 'api2_consistent_valid.txt')
	infile3  = os.path.join('APIFiles', 'api3_consistent_valid.txt')
	p.loadDBs(infile1, infile2, infile3)
	member_id = 1234
	field_priority_order = ['oop_max', 'stop_loss', 'deductible']
	funcs = [min, max, min]
	result = p.funcFieldPolicy(member_id, field_priority_order = field_priority_order, funcs = funcs, check_consistency = False,  check_validity = False)
	print('Testing funcs field policy:')
	print('field_priority_order:', field_priority_order)
	print('funcs:', [f.__name__ for f in funcs])
	print('Member Deductible: ', result)
	print('')

	# Mode Field Policy Test #1
	infile1  = os.path.join('APIFiles', 'api1_consistent_valid.txt')
	infile2  = os.path.join('APIFiles', 'api2_consistent_notvalid.txt')
	infile3  = os.path.join('APIFiles', 'api3_consistent_valid.txt')
	p.loadDBs(infile1, infile2, infile3)
	member_id = 1234
	field_priority_order = ['oop_max', 'deductible', 'stop_loss']
	result = p.modeFieldPolicy(member_id, field_priority_order = field_priority_order, check_consistency = False,  check_validity = False)
	print('Testing mode field policy #2:')
	print('field_priority_order:', field_priority_order)
	print('Member Deductible: ', result)
	print('')


	# Mode Field Policy Test #2
	print('Main Test')
	infile1  = os.path.join('APIFiles', 'api1_consistent_valid.txt')
	infile2  = os.path.join('APIFiles', 'api2_consistent_valid.txt')
	infile3  = os.path.join('APIFiles', 'api3_consistent_valid.txt')
	p.loadDBs(infile1, infile2, infile3)
	member_id = 1234
	field_priority_order = ['oop_max', 'deductible', 'stop_loss']
	result = p.modeFieldPolicy(member_id, field_priority_order = field_priority_order, check_consistency = False,  check_validity = False)
	print('Testing mode field policy:')
	print('field_priority_order:', field_priority_order)
	print('Member Deductible: ', result)
	print('')