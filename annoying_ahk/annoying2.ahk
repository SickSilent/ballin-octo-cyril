;Moves around the screen randomly each 10 seconds or when clicked
maxx := 0
maxy := 0
randx := 0
randy := 0

#SingleInstance

onMessage(0x201, "WM_DOWN")

SysGet, maxy, 79
SysGet, maxx, 78 
maxx += 10
maxy -= 50

spawn() {
	global maxx, maxy, randx, randy
	Random, randy, 0, %maxy%
	Random, randx, 0, %maxx%
	Gui, new
	Gui, Add, Text,, 10 bucks says you can't click on me
	Gui, add, Text,, LOLZ
	Gui, +AlwaysOnTop 
	Gui, show, Y%randy% X%randx%, GUYS
	sleep, 10000
	Gui, Destroy
}
	
WM_DOWN() {
	global maxx, maxy, randx, randy
	IfWinExist GUYS
	{
		Random, randy, 0, %maxy%
		Random, randx, 0, %maxx%
		WinMove, %randx%, %randy%
	}
}

Loop {
	IfWinNotExist, GUYS
	{
		spawn()
	}
}

