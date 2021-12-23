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

				# If NEXT_ARROW is clicked:
				if (NEXT_ARROW.clicked(click)):
					
					# If the state is 0, advance the state and show the portrait for the Servant.
					if state == 0:
						state += 1
						SERVANT_LIST[i].show_portrait()

					# If the state is 1, advance the state again and show the Servant's name.
					elif state == 1:
						state += 1
						SERVANT_LIST[i].confirm_name()

					# If the state is 2, return to state 0.
					# Then, hide the Servant's portrait and strike out their name.
					# Finally, increment i by 1 to move on to the next Servant.
					elif state == 2:
						state = 0
						SERVANT_LIST[i].hide_portrait()
						SERVANT_LIST[i].disable_name()
						i += 1


				# Else if BACK_ARROW is clicked:
				elif (BACK_ARROW.clicked(click)):

					# If the state is 0, return the state back to 2 and decrement i to return to the
					# 	previous Servant.
					# Then, show their portrait and rehighlight their name.
					if state == 0:
						state = 2
						i -= 1
						SERVANT_LIST[i].show_portrait()
						SERVANT_LIST[i].confirm_name()

					# If the state is 2, skip state 1 and go directly to state 0.
					# Then, hide the Servant's portrait and reset the their name to its default state.
					elif state == 2:
						state = 0
						SERVANT_LIST[i].hide_portrait()
						SERVANT_LIST[i].reset_name()


			# If i is 0, we are on the first Servant.
			if i == 0:

				# Additionally, if the state is 0, the game hasn't started, and BACK_ARROW should therefore
				# 	be disabled. Otherwise, show BACK_ARROW.
				BACK_ARROW.hide() if state == 0 else BACK_ARROW.show()


if __name__ == '__main__':
	main()