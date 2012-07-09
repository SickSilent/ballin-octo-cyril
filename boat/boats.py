from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
import bots
#import multiprocessing

#Oh, by the way, the bot to be imported can be changed in line 67.
#The file containing the bot(s) can be changed in line 3.

OWNER = "someone"
CMDCHAR = "$"
SERVER = "irc.rizon.net"
PORT = 6667
NICK_PASS = "asdfsdaf"
CHANNELS = []
REJOIN_CHAN = []

class IrcBot(irc.IRCClient):
    nickname = "HUashdk"
    password = ""
    realname = "BOTS"
    username = "bot"
    #log = open("log.txt", "a")
    def __init__(self):
        global OWNER, CMDCHAR, REJOIN_CHAN
        self.rejoin_chan = REJOIN_CHAN
        self.owner = OWNER
        self.cmdchar = CMDCHAR
        self.bot = bots.BrainStorm(self.owner)

    def connectionMade(self):
        global SERVER, PORT
        irc.IRCClient.connectionMade(self)
        print "Connection has been made to %s" % (SERVER)
    
    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        print "Disconnected: %s" % (reason)
    
    def signedOn(self):
        global NICK_PASS, CHANNEL
        for chan in CHANNELS:
            self.join(chan)
        if (NICK_PASS != ""):
            self.msg("NickServ", "IDENTIFY " + NICK_PASS)
        print "Signed on"

    def joined(self, channel):
        print "Joined %s" % (channel)

    def left(self, channel):
        print "Left %s" % (channel)

    def kickedFrom(self, channel, kicker, message):
        print "Kicked from %s by %s: %s" % (channel, kicker, message)
        __import__('time').sleep(5)
        if (channel in self.rejoin_chan):
            self.join(channel)

    def privmsg(self, user, channel, msg):
        hostmask = user
        nick = user.split('!', 1)[0]
        parts = msg.split(' ')
        #self.log.write("(" + channel + ") <" + nick + "> " + ' '.join(parts) + "\n")
        if (parts[0][0] == self.cmdchar):
            command = ''.join(list(parts[0])[1:])
            if (command == 'reload' and nick == self.owner):
                print "Reloading..."
                try:
                    reload(bots)
                    self.bot = bots.BrainStorm(self.owner)
                    irc.msg(channel, "Reloaded.")
                except:
                    print "Something done broke..."
                command = "reload"
            try:
                method = getattr(self.bot, ('cmd_' + command))
                #print method
                method(self, hostmask, nick, parts, channel)
            except (NameError, AttributeError) as error:
                print "Error ocurred while trying to run %s: %s" % ('cmd_' + command, error)

    def alterCollidedNick(self, nickname):
        return nickname + "_"
    
class IrcBotFactory(protocol.ClientFactory):
    protocol = IrcBot

    def __init__(self):
        pass

    def clientConnectionLost(self, connector, reason):
        print "Disconnected: %s" % (reason)
        self.protocol.log.close()
        reactor.stop()
        #connector.connect()
    
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed: %s" % (reason)
        reactor.stop()
    

if __name__ == '__main__':
    f = IrcBotFactory()
    reactor.connectTCP(SERVER, PORT, f)
    reactor.run()
