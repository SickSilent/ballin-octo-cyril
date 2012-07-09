#! /usr/bin/env python

#Gets the latest bids/offers from Mt. Gox

import json
import urllib
import sys

opener = urllib.FancyURLopener(urllib.getproxies())
average = 0
avg_amount = 0

try:
	amount = int(sys.argv[1])
except:
	print "Usage:", sys.argv[0], "[amount]"
	exit(1)

reader = opener.open("https://mtgox.com/api/0/data/getTrades.php")
raw_json = reader.read()
reader.close()
stuff = json.loads(raw_json)

print 'Price   Amount  Trade Type'

for i in xrange(0, amount):
	print '%2.5f %2.5f %s' % (float(stuff[i]['price']), float(stuff[i]['amount']), stuff[i]['trade_type'])
	average += float(stuff[i]['price'])
	avg_amount += float(stuff[i]['amount'])

print "\nAvg. price:", (average/amount)
print "Volume:", avg_amount
