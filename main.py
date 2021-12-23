# main.py

from graphics import *
from main_window import *
from pathlib import Path
ROOT = Path(__file__).parent.absolute()

def main():
	
	for i in SERVANT_LIST:
		i.draw()

	for i in PLAYER_LIST:
		i.draw()

	NEXT_ARROW.show()

	
	longest_name = 0
	for i in SERVANT_LIST:
		longest_name = max(longest_name, i.strikethrough_length)
	main_area_width = (WIDTH - (longest_name + 220))


	welcome_screen()


	i = 0
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

				print(f"Was: i = {i}, state = {state}", end='	')
				if (NEXT_ARROW.clicked(click)):
					if state == 0:
						state += 1
						SERVANT_LIST[i].show_portrait()

					elif state == 1:
						state += 1
						SERVANT_LIST[i].confirm_name()
	
					elif state == 2:
						state = 0
						SERVANT_LIST[i].disable_name()
						SERVANT_LIST[i].hide_portrait()
						i += 1


				elif (BACK_ARROW.clicked(click)):
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

				print(f"Now: i = {i}, state = {state}")

			if i == 0:
				if state == 0:
					BACK_ARROW.hide()
				else: BACK_ARROW.show()



if __name__ == '__main__':
	main()