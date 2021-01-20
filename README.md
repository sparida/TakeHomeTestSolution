# To run main file execute:
$ python3 Policies.py 

This will run a series of tests using simulated API datat contained in text files within the "APIFiles" folder

# "Policies.py" uses "DataAPI.py" and "Member.py"
Both files have furtehr tests which can be executed using:
$ python3 DataAPI.py 
$ python3 Member.py 


# Description of Files:

Member.py - Class to store individual API entries
DataAPI.py - Class to simulate API from text input files along with utility functions
Policies.py - Implements various policies to determine true deductible
APIFiles/* - Data files simulating DataAPI Calls
README.md - This file

# General terminology for files in APIFIles/* :
1. Consistent API- Return the same set of 3 values for a given member_id
2. Valid API- Return valid entries for a given member id where validity tests are defined in "isValidMember" inside the "Member" class

# Possible policies for determining true deductible in case of api results wit varying entries:
1. Simple Trust Policy - Choose an API to prefer in order specified in "api_priority_order"
2. Min Val Policy - Choose correct API based on min value of each field, with order of fields is specified in "field_priority order"
3. Max Val Policy - Choose correct API based on min value of each field, with order of fields specified in "field_priority order"
4. Democratic policy - Mode Policy - Choose correct API based on most common value of each field, with order of fields specified in "field_priority order"

 Here field refers to one of deductible, stop_loss or oop_max.

In addition, I wrote a helper function "funcFieldPolicy" which applies three a set of three functions, one each on the three fields to sort them and then find teh deductibel based oin that.

# FINAL RESULT:
If I had to pick one I would go with  democratic or mode based policy but with checks for consistency and validity for each API
This is implemented in "modeFieldPolicy" and two tests are simulated.

Final answer: 1200 
Assuming API1, API2 and API3 are consistent & valid
and field_priority_order = ['oop_max', 'deductible', 'stop_loss'] from most important to least important)

Got questions?
Drop a line at sidparida95@gmail.com
	 


