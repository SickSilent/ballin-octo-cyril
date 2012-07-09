;Moves mouse, clicks, or types random characters at random intervals
char := 0
choice := 0


Loop
{
	
	Random, sleeptime, 5, 30
	;sleeptime := sleeptime 1000
	Sleep, %sleeptime%
	Random, choice, 1, 3
	
	if (choice = 3) {
		Random, char, 47, 123
		SendInput, % chr(char)
	} 
	if (choice = 2) {
		Random, mousex, -10, 10
		Random, mousey, -10, 10
		MouseMove, %mousex%, %mousey%, 3, R
		if (mousex < 2 and mousex > -2) and (mousey < 2 and mousey > -2)
			MouseClick
	}
	
	sleeptime := 0
	choice := 0
}