# main.py

from tkinter import Place
from graphics import *
from main_window import *
from pathlib import Path
ROOT = Path(__file__).parent.absolute()

def main():
	
	for i in SERVANT_LIST:
		i.draw()

	for i in PLAYER_LIST:
		i.draw()

	
	longest_name = 0
	for i in SERVANT_LIST:
		longest_name = max(longest_name, i.strikethrough_length)
	main_area_width = (WIDTH - (longest_name + 220))


	welcome_screen()

	i = -1
	state = 0
	while True:

		click = GW.getMouse()

		if click:

			# If the click is in the scoreboard area
			if click.x >= WIDTH - 170:
				for j in PLAYER_LIST:
					j.validate_click(click)
					

			# If the click is within the area for the next and back arrows:
			elif (((HEIGHT / 2) - 30) <= click.y <= ((HEIGHT / 2) + 30)):
				if ((main_area_width - 40) <= click.x <= (main_area_width - 10)):
					if state == 0:
						i += 1
						state += 1
						SERVANT_LIST[i].show_portrait()

					elif state == 1:
						state += 1
						SERVANT_LIST[i].confirm_name()

						
					elif state == 2:
						state = 0
						SERVANT_LIST[i].disable_name()
						SERVANT_LIST[i].hide_portrait()


				elif (10 <= click.x <= 40):
					if state == 0:
						i -= 1
						state = 2
						SERVANT_LIST[i].show_portrait()

					elif state == 1:
						state -= 1
						SERVANT_LIST[i].confirm_name()

						
					elif state == 2:
						state -= 1
						SERVANT_LIST[i].reset_name()
						SERVANT_LIST[i].show_portrait()








if __name__ == '__main__':
	main()