import pygame
import random
import time

pygame.font.init()


class Board:
	def __init__(self, rows=9, cols=9, height=720, width=720):
		self.rows = rows
		self.cols = cols
		self.height = height
		self.width = width
		self.tiles = [[]]
		self.empty_values = {}
		for i in range(rows):
			self.tiles.append([])
			for j in range(cols):
				self.tiles[i].append(Tile(0, i, j, (height // rows), (width // cols)))


	def initialize_board(self):
		for i in range(10):
			row = random.randint(0,8)
			col = random.randint(0,8)
			value = random.randint(1,9)
			if self.is_valid(value, (row, col)):
				self.tiles[row][col].set_number(value)

		self.solve_board()

		count = 40
		while count > 0:
			i = random.randint(0, self.rows*self.cols - 1)
			if self.tiles[i // self.cols][i % self.rows].number != 0:
				self.empty_values[(i // self.cols, i % self.rows)] = self.tiles[i // self.cols][i % self.rows].number
				self.tiles[i // self.cols][i % self.rows].set_number(0)
				self.tiles[i // self.cols][i % self.rows].set_correct(False)
				count -= 1


	def solve_board(self):
		empty = self.find_empty_cell()
		if empty == None:
			return True
		else:
			row, col = empty

		for i in range(1, 10):
			if self.is_valid(i, (row, col)):
				self.tiles[row][col].set_number(i)
				self.tiles[row][col].set_correct(True)
				self.tiles[row][col].set_temp(False)

				if self.solve_board():
					return True

			self.tiles[row][col].set_number(0)
			self.tiles[row][col].set_correct(False)

		return False


	def find_empty_cell(self):
		for i in range(self.rows):
			for j in range(self.cols):
				if self.tiles[i][j].number == 0:
					return (i, j)

		return None


	def is_valid(self, number, position):
		for i in range(self.rows):
			if self.tiles[position[0]][i].number == number and position[1] != i:
				return False
			if self.tiles[i][position[1]].number == number and position[0] != i:
				return False

		squareX = position[1] // 3
		squareY = position[0] // 3

		for i in range(squareY * 3, squareY * 3 + 3):
			for j in range(squareX * 3, squareX * 3 + 3):
				if self.tiles[i][j].number == number and [i,j] != position:
					return False

		return True

	def selected_tile(self, pos):
		col = pos[0] // (self.width // self.cols)
		row = pos[1] // (self.height // self.rows)
		if (row < 9) and (col < 9):
			return (row, col)
		else:
			return (None, None)

	def set_selected(self, tile):
		row, col = tile
		value = self.tiles[row][col].number
		for i in range(self.rows):
			for j in range(self.cols):
				if i != row or j != col:
					self.tiles[i][j].set_selected(False)
				else:
					self.tiles[i][j].set_selected(True)

				if self.tiles[i][j].number == value and value != 0:
					self.tiles[i][j].set_selected(True)

	def draw(self, window):
		gap = self.width // 9
		for i in range(self.rows + 1):
			if i % 3 == 0 and i != 0:
				thick = 4
			else:
				thick = 1
			pygame.draw.line(window, (0, 0, 0), (0, i*gap), (self.width, i * gap), thick)
			pygame.draw.line(window, (0, 0, 0), (i*gap, 0), (i*gap, self.height), thick)

		for i in range(self.rows * self.cols):
			self.tiles[i // self.cols][i % self.cols].draw(window)

	def print_board(self):
		for i in range(self.rows):
			if i % 3 == 0 and i != 0:
				print("--------------------------")
			for j in range(self.cols):
				if j % 3 == 0 and j != 0:
					print(" | ", end=" ")
				
				if j == self.cols - 1:
					print(self.tiles[i][j].number)
				else:
					print(str(self.tiles[i][j].number) + "", end=" ")


#NEW CLASS
class Tile:
	def __init__(self, number, row, col, height, width):
		self.number = number
		self.row = row
		self.col = col
		self.temp = False
		self.temp_number = None
		self.selected = False
		self.correct = True
		self.height = height
		self.width = width

	def set_number(self, number):
		self.number = number

	def set_temp(self, temp):
		self.temp = temp

	def set_temp_number(self, number):
		self.temp_number = number

	def set_correct(self, correct):
		self.correct = correct

	def set_selected(self, selected):
		self.selected = selected

	def draw(self, window):
		font = pygame.font.SysFont("comicsans", 40)
		y = self.row * self.height
		x = self.col * self.width
		if self.correct:
			text = font.render(str(self.number), 1, (0,0,0))
			window.blit(text, (x + self.width // 2 - text.get_width() // 2, y + self.height // 2 - text.get_height() // 2))
		elif self.temp and self.temp_number != None:
			text = font.render(str(self.temp_number), 1, (128,128,128))
			window.blit(text, (x + 5, y + 5))

		if self.selected:
			if not self.correct:
				pygame.draw.rect(window, (255,0,0), (x,y,self.width,self.height), 3)
			else:
				pygame.draw.rect(window, (0,0,255), (x,y,self.width,self.height), 3)

def format_time(secs):
    sec = secs%60
    minute = secs//60

    compound = " " + str(minute) + ":" + str(sec)
    return compound

def main():
	board = Board()
	board.initialize_board()

	window = pygame.display.set_mode((board.width, board.height + 50))
	pygame.display.set_caption("Sudoko")
	start = time.time()
	run = True
	won = False
	lost = False
	key_pressed = None
	row, col = 0,0
	wrong = 0

	def redraw_window(window, board, wrong, won, timeElap):
		window.fill((255,255,255))
		board.draw(window)
		font = pygame.font.SysFont("comicsans", 40)
		text = font.render('X', 1, (255,0,0))
		timeText = font.render("Time: " + format_time(timeElap), 1, (0,0,0))
		window.blit(timeText, (board.width - 150, board.height + 5))
		for i in range(wrong):
			if (window.get_width() - (i * text.get_width())) > text.get_width():
				window.blit(text, (5 + i * text.get_width(), board.height + 5))
		if won:
			font = pygame.font.SysFont("comicsans", 100)
			text = font.render('YOU WON!', 1, (128,128,0))
			window.blit(text, (window.get_width() // 2 - text.get_width() // 2, window.get_height() // 2 - text.get_height() // 2))
		if lost:
			font = pygame.font.SysFont("comicsans", 100)
			text = font.render('YOU LOST!', 1, (255,0,0))
			window.blit(text, (window.get_width() // 2 - text.get_width() // 2, window.get_height() // 2 - text.get_height() // 2))
						
	while run:
		if not won:
			play_time = round(time.time() - start)
		if lost:
			time.sleep(3)
			run = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					key_pressed = 1
				if event.key == pygame.K_2:
					key_pressed = 2
				if event.key == pygame.K_3:
					key_pressed = 3
				if event.key == pygame.K_4:
					key_pressed = 4
				if event.key == pygame.K_5:
					key_pressed = 5
				if event.key == pygame.K_6:
					key_pressed = 6
				if event.key == pygame.K_7:
					key_pressed = 7
				if event.key == pygame.K_8:
					key_pressed = 8
				if event.key == pygame.K_9:
					key_pressed = 9
				if event.key == pygame.K_s:
					board.solve_board()
					won = True
				if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
					if board.tiles[row][col].selected and not board.tiles[row][col].correct:
						if board.empty_values[(row,col)] == board.tiles[row][col].temp_number:
							board.tiles[row][col].set_number(board.tiles[row][col].temp_number)
							board.tiles[row][col].set_correct(True)
							board.tiles[row][col].set_temp(False)
							board.empty_values.pop((row,col))
							if len(board.empty_values) == 0:
								won = True
							else:
								board.set_selected((row, col))
						else:
							board.tiles[row][col].set_temp(False)
							board.tiles[row][col].set_number(0)
							wrong += 1

			if event.type == pygame.MOUSEBUTTONDOWN:
				x,y = pygame.mouse.get_pos()
				row, col = board.selected_tile((x,y))
				board.set_selected((row, col))

			if row != None and col != None:
				if board.tiles[row][col].selected and key_pressed != None:
					board.tiles[row][col].set_temp(True)
					board.tiles[row][col].set_temp_number(key_pressed)

			if wrong >= 10:
				lost = True
			key_pressed = None

		redraw_window(window, board, wrong, won, play_time)
		pygame.display.update()


main()