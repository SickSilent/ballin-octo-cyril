;Grows slowly until the whole screen is taken up. Side effect of not being able to do anything until the screen is filled.
#SingleInstance

maxx := 0
maxy := 0
currx := 0
curry := 0

SysGet, maxy, 79
SysGet, maxx, 78 

Gui, new
Gui, add, Text, Center, IMMA TAKE YOUR WHOLE SCREEN
Gui, +AlwaysOnTop
Gui, show, W1 H1, OHAI

while (maxx > currx) 
{
	curry += 1
	currx += 1
	if (curry > maxy)
		curry -= 1
	
	Gui, show, W%currx% H%curry% Center, OHAI
	sleep, 75
}