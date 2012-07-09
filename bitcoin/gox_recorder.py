#! /usr/bin/env python

#Records Mt. Gox trades in a file until stopped

import json
import urllib
from time import sleep
import signal


ticker_url = "https://mtgox.com/api/0/data/ticker.php"

class Alerter():
	def __init__(self, tickerurl):
		self.ticker_url = tickerurl
		self.raw_json = ""
		self.opener = urllib.FancyURLopener(urllib.getproxies())

	def alert_loop(self):
		output = open('ticker_output.txt', 'a')
		while 1:
			reader = self.opener.open(self.ticker_url)
			self.raw_json = reader.read()
			reader.close()
			output.write(str(self.raw_json + "\n"))
			sleep(90)

print "Starting recorder..."
thingy = Alerter(ticker_url)

thingy.alert_loop()
