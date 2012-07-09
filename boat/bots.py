from threading import Thread
class BrainStorm:
    def __init__(self, owner):
        self.owner = owner
        self.interval_running = False

    def cmd_reload(self, irc, hostmask, nick, parts, channel):
        print "Reload successful"

    def cmd_version(self, irc, hostmask, nick, parts, channel):
        print "Channel version request"
        irc.notice(nick, "boats.py by S_S")

    def cmd_quit(self, irc, hostmask, nick, parts, channel):
        if (nick == self.owner):
            irc.quit("FIEN THEN")
                
    def cmd_decide(self, irc, hostmask, nick, parts, channel):
        from random import choice
        var = ' '.join(parts[1:])
        var = var.split(",")
        irc.msg(channel, "Choice: " + choice(var))
    
    def reminder(self, irc, message, channel, nick, secs):
        from time import sleep
        sleep(secs)
        irc.msg(channel, "Reminder from " + nick + ": " + message)

    def cmd_remind(self, irc, hostmask, nick, parts, channel):
        secs = parts[1]
        mesg = ' '.join(parts[2:])
        Thread(target=self.reminder, args=(irc, mesg, channel, nick, secs)).start()

    def cmd_nazi(self, irc, hostmask, nick, parts, channel):
        from    random import randint
        dongus = ' '.join(parts[1:])
        sw_bg = randint(0,14) + 2
        sw_fg = randint(0,14) + 2
        tx_fg = randint(0,14) + 2
        swastika = ("" + str(sw_fg) + "," + str(sw_bg) + unichr(21325))
        swastika = swastika.encode("UTF-8")
        middlecolor = ( "" + str(tx_fg) + " ")
        irc.msg(channel, swastika + middlecolor + dongus + " " + swastika)
    
    def cmd_join(self, irc, hostmask, nick, parts, channel):
        if (nick == self.owner):
            irc.join(parts[1])
    
    def cmd_part(self, irc, hostmask, nick, parts, channel):
        if (nick == self.owner):
            irc.part(parts[1])

    def cmd_privmsg(self, irc, hostmask, nick, parts, channel):
        if (nick == self.owner):
            dest = parts[1]
            destm = ' '.join(parts[2:])
            irc.msg(dest, destm)

    def cmd_raw(self, irc, hostmask, nick, parts, channel):
       if (nick == self.owner):
           irc.sendLine(' '.join(parts[1:]))

    def cmd_zalgo(self, irc, hostmask, nick, parts, channel):
        tempf = open("/dev/urandom", "r+b")
        irc.msg(channel, tempf.readline())
        tempf.close()

    def interval(self, irc, channel, secs, userand):
        while True:
            if (self.interval_running):
                from time import sleep
                irc.msg(channel, "BEEEEEEEEEEEEEEEEP")
                sleep(secs)
            else:
                break

    def cmd_interval(self, irc, hostmask, nick, parts, channel):
        if not (self.interval_running):
            self.interval_running = True
            if (parts[2] == "random"):
                userand = True
            else:
                userand = False
            secs = int(parts[1])
            Thread(target=self.interval, args=(irc, channel, secs, userand)).start()
        else:
            irc.msg(channel, "Interval already started.")

    def cmd_interval_stop(self, irc, hostmask, nick, parts, channel):
        self.interval_running = False
        irc.msg(channel, "lolk")
    
    def cmd_kick(self, irc, hostmask, nick, parts, channel):
        if (nick == self.owner):
			irc.kick(channel, parts[1], ' '.join(parts[2:]))

    #def cmd_ban(self, irc, hostmask, nick, parts, channel):
    #    irc.mode(channel, True, "b", mask=(hostmask.split('@')[1]))

