;Fills screen with popups. Side effect of making DWM and the process hog resources
currx = 0
curry = 0
maxx = 50
maxy = 10

SysGet, maxy, 79
SysGet, maxx, 78

maxx -= 50
maxy -= 10

While curry < maxy
{
	curry += 4
	currx = 0

	While currx < maxx
	{
		Gui, new
		Gui, +AlwaysOnTop
		Gui, add, Text,, HEY EVERYBODY I'M WATCHING GAY PORNO
		Gui, show, y%curry% x%currx%, GUYS
		currx += 2
	}
}