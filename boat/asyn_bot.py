import asyncore, socket

server = "irc.anonops.bz"
port = 6667
CRLF = "\r\n"

class IRCBot(asyncore.dispatcher):
    def __init__(self, server, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((server, port))
        self.buffer = ''
        self.file = self.makefile('rb')
        self.nick = "Winnie_Pooh"
        self.username = "winnie"
        self.realname = "Woooo"
        self.chans = ["#sick"]

    def handle_connect(self):
        print "Connected!"
        self.auth()

    def handle_close(self):
        self.close()

    def handle_read(self):
        while 1:
            try:
                s = self.file.readline()
                if not s:
                    raise EOFError
                if s[-2:] == CRLF:
                    s = s[:-2]
                elif s[-1:] in CRLF:
                    s = s[:-1]
                if not s:
                    break
                self.irc_handle(s)
            except:
                break

    def parse_line(self, line):
        #print line
        linex = line.split( )
        #print linex
        if (linex[0] == "PING"):
            self.write("PONG " + linex[1] + CRLF)
            print "Pong!"
        sendsd = linex[0]
        sendsd = sendsd[1:]
        text = ' '.join(linex[3:])
        text = text[1:]
        parts = {
            'sender': linex[0][1:],
            'target': linex[2],
            'action': linex[1],
            'msg': ' '.join(linex[3:])[1:]
            }
        print parts
        return parts

    def irc_handle(self, line):
        #print line
        parts = self.parse_line(line)
        print parts
        if parts['action'] == '451': self.auth()
        #if parts['sender'] == 'PING': self.write('PONG ' + \
        #                                         parts['action'])
        if parts['action'] == '001':
            print "Authed!"
            for chan in self.chans:
                self.write("JOIN " + chan + CRLF)

        
    def handle_write(self):
        print self.buffer
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def writable(self):
        return (len(self.buffer) > 0)

    def write(self, buf):
        self.buffer += buf

    def auth(self):
        self.write("NICK " + self.nick + CRLF)
        self.write("USER " + self.username + " 0 * :" + self.realname + CRLF)

    def read_loop(self):
        try:
            s = raw_input("Command: ")
            self.write(s)
        except e:
            print e

client = IRCBot(server, port)    
asyncore.loop()
