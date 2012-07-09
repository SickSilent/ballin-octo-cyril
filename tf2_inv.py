#!/usr/bin/env python
#Sick_Silent's TF2 idle item alerter, v0.99
#Prints a message when a new item is detected in a player's inventory
#Do what you want with it, just give some credit if you use this
#Also a heads up would be nice

import json
import urllib
from time import sleep

#Change this to your TF2 inventory JSON URL. (Append /inventory/json/440/2/ to your profile URL).
ticker_url = ""

opener = urllib.FancyURLopener(urllib.getproxies())
reader = opener.open(ticker_url)
raw_json = reader.read()
reader.close()
whole_inv = json.loads(raw_json)['rgInventory']
whole_desc = json.loads(raw_json)['rgDescriptions']
new_count = 999
cooldown = 15

count = len(whole_inv)
print "Starting item count:", count

def list_items():
	for item in whole_desc:
		print "Name:", whole_desc[item]['name']
		'''
		print "Description:", 
		for i in xrange(len(whole_desc[item]['descriptions'])):
			if (whole_desc[item]['descriptions'][i]['value']):
				print (whole_desc[item]['descriptions'][i]['value'].strip() + ", "),
		'''

def check_loop():
	while 1:
		sleep(cooldown*60)
		new_raw_json = opener.open(ticker_url).read()
		new_whole_inv = json.loads(new_raw_json)['rgInventory']
		new_whole_desc = json.loads(new_raw_json)['rgDescriptions']
		new_count = len(new_whole_inv)
		if (new_count > count):
			print "NEW ITEMS!"
			for i in xrange(new_count - count):
				item = sorted(new_whole_inv)[len(new_whole_inv) - i - 1]
				classid = new_whole_inv[str(item)]['classid']
				instance_id = new_whole_inv[str(item)]['instanceid']
				print new_whole_desc[str(classid) + "_" + str(instance_id)]['name']
		#else:
		#	print "%s minutes pass, no new items." % cooldown
		count = new_count
		whole_inv = new_whole_inv
		whole_desc = new_whole_desc
		raw_json = new_raw_json
		
#list_items()
check_loop()