#! /usr/bin/env python

#Mt. Gox Live ticker thingy. Might work for other exchanges.
#Updates every 120 seconds, can add/remove/list notifications
#Version: 1.5.2
#Made by Sick_Silent

##CHANELOG:
#1.5.2 Added "notify only" mode (change True to False at the bottom for ticker
#1.5.1: Fixed in notifications
#1.5: Added saving alerts to file (alerts.txt)
#1.4: Added multithreading, interface
#1.0: Initial release

##TODO:
#Implement command-line options
#Figure out how to get "live" updates
#Make it work with other exchanges (not likely)
#Alternate alerting methods (not likely)

import json
import urllib
from hashlib import md5
from time import sleep
from threading import Thread
import signal


ticker_url = "https://mtgox.com/api/0/data/ticker.php"

class CheckerThread(Thread):
	def __init__(self):
		Thread.__init__(self)
	
	def run(self):
		for al in thingy.alerts:
			op = al.split()

			if op[0] == "drops":
				if float(thingy.ticker['last']) <= float(op[1]):
					print  "" + "Alert! Last price fell below", op[1]
					thingy.alerts.remove(al)
					
			elif op[0] == "rises":
				if float(thingy.ticker['last']) >= float(op[1]):
					print  "" + "Alert! Last price rose above", op[1]
					thingy.alerts.remove(al)
		
class InputThread(Thread):
	def __init__(self):
		Thread.__init__(self)
		signal.signal(signal.SIGINT, self.catch_int)
		
	def catch_int(self, signal, frame):
		print "Exiting..."
		file = open("alerts.txt", "w")
		for i in thingy.alerts:
			file.write(i + "\n")
		file.close()
		exit(0)
	
	def run(self):
		try:
			while 1:
				incoming = raw_input()
				incoming = incoming.split()
			
				if incoming[0] == "add":
					if incoming[1] == "drops":
						self.add_alert("drops", float(incoming[2]))
					elif incoming[1] == "rises":
						self.add_alert("rises", float(incoming[2]))
				elif incoming[0] == "list":
					print "Alerts:",
					for i in thingy.alerts:
						print (str(i) + ","),
					print ""
				elif incoming[0] == "del":
					self.del_alert(' '.join(incoming[1:]))
				elif incoming[0] == "price":
					thingy.check_tick()
					thingy.print_info()
					thingy.checker.run()
				
				else:
					print "Usage: [add (rises|drops) (amount)] [list] [del (alert)] [price]"
		except EOFError:
			pass
	
	def add_alert(self, kind, amount):
		thingy.alerts.append(str(kind) + " " + str(amount))
	
	def del_alert(self, alert):
		try:
			thingy.alerts.remove(alert)
		except:
			print ("Something went wrong. Are you sure you're" + \
					"deleting something that exists?")

class Alerter():
	def __init__(self, tickerurl, notify_only):
		self.ticker_url = tickerurl
		self.checksum = ""
		self.raw_json = ""
		self.alerts = []
		self.opener = urllib.FancyURLopener(urllib.getproxies())
		self.inputer = InputThread()
		self.checker = CheckerThread()
		self.notify_only = notify_only
		output = open('ticker_output.txt','a')
		try:
			file = open("alerts.txt", "r")
			for line in file.readlines():
				if line.strip(): self.alerts.append(line.strip())
			file.close()
		except:
			pass
			
	def print_info(self):
		print "Latest:\t", self.ticker['last']
		print "Sell:\t", self.ticker['sell']
		print "Buy:\t", self.ticker['buy']
		print "High/Low/Avg:\t", (str(self.ticker['high']) + "/" \
										+ str(self.ticker['low']) + "/" \
										+ str(self.ticker['avg']))
		print "VWAP:\t", self.ticker['vwap'], "\n"	

	def check_tick(self):
		reader = self.opener.open(self.ticker_url)
		self.raw_json = reader.read()
		reader.close()
		self.ticker = json.loads(self.raw_json)['ticker']
		self.new_checksum = md5(str(self.ticker['last'])).hexdigest()

		
	def alert_loop(self):
		self.inputer.start()
		while 1:
			self.check_tick()
			if self.new_checksum != self.checksum:
				self.checksum = self.new_checksum
				if not self.notify_only:
					self.print_info()
			self.checker.run()
			sleep(90)

print "Starting ticker..."

#thingy = Alerter(ticker_url, False) #Notify and ticker
thingy = Alerter(ticker_url, True) #Notify only

thingy.alert_loop()
