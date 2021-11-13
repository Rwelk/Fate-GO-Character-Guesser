# globals.py

from pathlib import Path
from graphics import *
from random import shuffle

ROOT = Path(__file__).parent.absolute()


class Servant:
	
	# functions
	def __init__(self, name, img, offset=0, total_number=20):

		# Determine where to anchor the displayed name of the servant:
		line_width = (HEIGHT - 85) / total_number
		anchor = Point((WIDTH - 200), ((line_width * offset) + 60))

		# Draw the name of the servant:
		self.name = Text(anchor, name)
		self.name.setAnchor('ne')

		# Save the servant's portrait:
		self.img = Image(Point(0, 0), ROOT / f"servant_images/{img}.png")

		# Create the line that will strike through the servant name when they are used:
		# Start by finding the length of the strikethrough.
		character_widths = {
			' ': 8,		'ō': 15,	'a': 15,	'A': 18,	'b': 15,	'B': 18,	'c': 14,	'C': 19,
			'd': 15,	'D': 19,	'e': 15,	'E': 18,	'f': 7.5,	'F': 16.66,	'g': 15,	'G': 21,
			'h': 15,	'H': 19,	'i': 6,		'I': 7.5,	'j': 6,		'J': 14,	'k': 14,	'K': 18,
			'l': 6,		'L': 15,	'm': 22,	'M': 22,	'n': 15,	'N': 19,	'o': 15,	'O': 21,
			'p': 15,	'P': 18,	'q': 15,	'Q': 21,	'r': 9,		'R': 19,	's': 14,	'S': 18,
			't': 7.5,	'T': 16.66,	'u': 15,	'U': 19,	'v': 14,	'V': 18,	'w': 19,	'W': 28,
			'x': 14,	'X': 18,	'y': 14,	'Y': 18,	'z': 14,	'Z': 16.66,
		}

		self.strikethrough_length = 0
		for i in self.name.getText():
			self.strikethrough_length += character_widths.get(i)

		# Determine the endpoints of the strikethrough, and set its width:
		self.strikethrough = Line(
			Point((anchor.x - self.strikethrough_length - 3), (anchor.y + 16)),
			Point(anchor.x + 3, (anchor.y + 16)))
		self.strikethrough.setWidth(3)
		self.strikethrough.setFill('red')

	# Method for showing the Servant's name
	def draw(self):
		self.name.draw(GW)


	# When it is the servant's turn, show their portrait.
	def show_portrait(self):
		self.img.draw(GW)


	# When the servant's turn is over, hide their portrait.
	def hide_portrait(self):
		self.img.undraw()


	# Reveal who the servant really is
	def confirm_name(self):
		self.name.setTextColor('limegreen')

	# Mark out the servant's name from the name bank so players won't reuse it.
	def disable_name(self):
		self.strikethrough.draw(GW)
		self.name.setTextColor('red')
	
	# Reset the name if the back arrow is clicked.
	def reset_name(self):
		self.name.setTextColor('black')
		self.strikethrough.undraw()


class ScoreBox:

	def __init__(self, name, base_score=0, offset=0):

		# Field for the player's name:
		self.name = Text(
			Point(WIDTH - 170, ((offset * 80) + 60)), name)
		self.name.setSize(20)
		self.name.setAnchor('nw')

		# Button for adding to the score:
		self.plus_border = Rectangle(
			Point(WIDTH - 170, ((offset * 80) + 90)), 
			Point(WIDTH - 150, ((offset * 80) + 110))
		)
		self.plus_border.setFill(color_rgb(142, 227, 142))

		self.plus = Text(
			Point(WIDTH - 160, ((offset * 80) + 100)), "+")
		self.plus.setAnchor('c')
		self.plus.setSize(16)

		# Button for subtracting from the score:
		self.minus_border = Rectangle(
			Point(WIDTH - 170, ((offset * 80) + 110)), 
			Point(WIDTH - 150, ((offset * 80) + 130))
		)
		self.minus_border.setFill(color_rgb(255, 140, 143))
		
		self.minus = Text(
			Point(WIDTH - 160, ((offset * 80) + 120)), "-")
		self.minus.setAnchor('c')
		self.minus.setSize(16)

		# Box for displaying the score:
		self.score_border = Rectangle(
			Point(WIDTH - 150, ((offset * 80) + 90)),
			Point(WIDTH - 20, ((offset * 80) + 130))
		)
		self.score_border.setFill('white')

		self.score = Text(
			Point(WIDTH - 85, ((offset * 80) + 111)), base_score)
		self.score.setAnchor('c')
		self.score.setSize(29)

	def draw(self):
		self.name.draw(GW)
		self.plus_border.draw(GW)
		self.plus.draw(GW)
		self.minus_border.draw(GW)
		self.minus.draw(GW)
		self.score_border.draw(GW)
		self.score.draw(GW)

	# Function for determining whether a click on GW is within a button for this object:
	def validate_click(self, point):
		
		if (self.plus_border.p1.x <= point.x <= self.plus_border.p2.x) and (self.plus_border.p1.y <= point.y <= self.plus_border.p2.y):
			self.add_point()
		
		elif (self.minus_border.p1.x <= point.x <= self.minus_border.p2.x) and (self.minus_border.p1.y <= point.y <= self.minus_border.p2.y):
			self.sub_point()

	# Function for adding a point to the player's score:
	def add_point(self):
		self.score.setText(int(self.score.getText()) + 1)

	# Function for taking away a point from the player's score:
	def sub_point(self):
		self.score.setText(int(self.score.getText()) - 1)

	




def create_canvas(x, y):

	# Create the GraphWin
	gw = GraphWin("Guess the Fate/Grand Order Character!", x, y)


	# Create the Name Bank
	# Title
	name_bank = Text(Point(x - 200, 0), "Name Bank")
	name_bank.setSize(30)
	name_bank.setAnchor('ne')
	name_bank.draw(gw)
	
	# Underline Title
	name_bank_underline = Line(Point(x - 406, 41), Point(x - 200, 41))
	name_bank_underline.setWidth(4)
	name_bank_underline.draw(gw)

	# Fill out Servants
	servant_list = generate_servant_list()


	# Create the Score Board
	# Title
	score_board = Text(Point((x - 170), 0), "Scores")
	score_board.setSize(30)
	score_board.setAnchor('nw')
	score_board.draw(gw)
	
	# Underline Title
	score_board_underline = Line(Point((x - 170), 41), Point(x - 45, 41))
	score_board_underline.setWidth(4)
	score_board_underline.draw(gw)
	
	# Fill out Players
	player_list = generate_player_list()


	# Determine how much space the main area takes up:
	longest_name = 0
	for i in servant_list:
		longest_name = max(longest_name, i.strikethrough_length)
	main_area_width = (x - (longest_name + 220))

	
	# Create the App Title and underline it.
	title = Text(Point((main_area_width / 2), 0), "Who am I?")
	title.setSize(30)
	title.setAnchor('n')
	title.draw(gw)
	
	title_underline = Line(Point(((main_area_width / 2) - 95), 41), Point(((main_area_width / 2) + 95), 41))
	title_underline.setWidth(4)
	title_underline.draw(gw)

	gui_background = Rectangle(
		Point(main_area_width, 0),
		Point(x, y)
	)
	gui_background.setFill('lightgray')
	gui_background.setOutline('')
	gui_background.draw(gw)
	gui_background.lower(name_bank)


	# Use image as the background for the main area.
	main_area_background = Image(Point((main_area_width / 2), (((y - 60) / 2) + 60)), ROOT / 'background.png')
	main_area_background.draw(gw)
	main_area_background.lower()

	for i in servant_list:
		i.img.anchor = main_area_background.anchor

	# Create the forward and back arrows to progress through the game:
	back_arrow = Polygon(
		Point(10, (HEIGHT / 2)),
		Point(40, ((HEIGHT / 2) - 30)),
		Point(40, ((HEIGHT / 2) + 30)),
	)
	back_arrow.setFill('ghostwhite')
	back_arrow.setWidth(2)
	back_arrow.draw(gw)

	next_arrow = Polygon(
		Point((main_area_width - 10), (HEIGHT / 2)),
		Point((main_area_width - 40), ((HEIGHT / 2) - 30)),
		Point((main_area_width - 40), ((HEIGHT / 2) + 30)),
	)
	next_arrow.setFill('ghostwhite')
	next_arrow.setWidth(2)
	next_arrow.draw(gw)

	# Return the GraphWin
	return gw, servant_list, player_list


# Function for reading from a file
#   file is the name of the file to be read
def read_file(file):
	with open(ROOT / file, encoding="utf8") as f:
		lines = f.readlines()

	for i in range(len(lines)):
		lines[i] = lines[i].replace("\n", "").split(",")

	return lines[1:]


# Function for creating all the Servant objects in the Name Bank
#   file is the file where the servants and the image associated with them are stored, which by default is 
#       'servants.txt'
def generate_servant_list(file='servants.txt', randomize=False):

	contents = read_file(file)

	arr = [None for i in range(len(contents))]

	for i in range(len(contents)):
		arr[int(contents[i][2])] = Servant(contents[i][0], contents[i][1], i, len(contents))

	if randomize: shuffle(arr)

	return arr


# Function for creating all the Scorebox objects in the scoring area
#   file is the file where the names of the players are stored, which by default is 'players.txt'
def generate_player_list(file='players.txt'):
	
	arr = read_file(file)

	for i in range(len(arr)):
		try:
			arr[i] = ScoreBox(arr[i][0], arr[i][1], i)
		except IndexError:
			arr[i] = ScoreBox(arr[i][0], 0, i)

	return arr


def welcome_screen():
	screen = Rectangle(Point(0, 0), Point(WIDTH, HEIGHT))
	screen.setFill('ghostwhite')
	screen.draw(GW)

	text1 = Text(Point((WIDTH / 2), ((HEIGHT / 2) - 20)), "Welcome to the Fate/Grand Order Character Guesser")
	text1.setJustification('center')
	text1.setAnchor('c')
	text1.setSize(30)
	text1.draw(GW)

	text2 = Text(Point((WIDTH / 2), ((HEIGHT / 2) + 20)), "Click anywhere to continue...")
	text2.setJustification('center')
	text2.setAnchor('c')
	text2.setSize(15)
	text2.draw(GW)

	GW.getMouse()

	text1.undraw()
	text2.undraw()
	screen.undraw()


WIDTH = 1300
HEIGHT = 775
GW, SERVANT_LIST, PLAYER_LIST = create_canvas(WIDTH, HEIGHT)


if __name__ == '__main__':
	print('Running globals.py')


	GW.getMouse()