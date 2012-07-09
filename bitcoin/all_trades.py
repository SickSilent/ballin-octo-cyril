#! /usr/bin/env python

#Gets a list of every trade in Mt. Gox, since the beginning.

import json
import urllib
import sys
from hashlib import md5

opener = urllib.FancyURLopener(urllib.getproxies())
average = 0
avg_amount = 0
hash = ""
new_hash = "a"
list = open("all_trades.txt","w")
i = 0

try:
	prog = open("all_trades_progress.txt","r")
	i = prog.read()
	if i == "":
		i = 0
	prog.seek(0)
except:
	pass

prog = open("all_trades_progress.txt","w")

print "Starting..."

while new_hash != hash:
	print "At", str(i) + "th entry"
	hash = new_hash
	reader = opener.open("https://mtgox.com/api/0/data/getTrades.php?since=%d" % i)
	raw_json = reader.read()
	reader.close()
	list.write(str(raw_json) + ",")
	prog.write(str(i))
	prog.seek(0)
	#stuff = json.loads(raw_json)
	hash = md5(str(raw_json)).hexdigest()
	i += 100
