#####################################################Game.py############################################################
# Encoding: UTF-8

# Class with all the Game variables and functions
# The official board is 10x20, so this values cannot be changed

# Author:

# Pedro Silva André
########################################################################################################################

# Modules Import

# Import from other project scripts
# Modules Import
import pygame

from general_functions import check_pair_in_list, create_matrix
# Import from other project scripts
from piece import Piece


class Game:
    def __init__(self):
        # All variables necessary for the Game
        self.level = 1
        self.points = 0
        self.interval = 1000  # Interval in seconds between drops
        self.interval_drop = 0.8

        self.points_to_new_level = 1000
        self.points_per_line_cleared = 200

        self.window = None  # Needs to wait for window to be created in main loop
        self.window_width = None
        self.window_height = None
        self.square_side = None
        self.window_title = 'Titan Blocks'
        self.background_color = [255, 255, 255]  # white background color
        self.grid_color = [169, 169, 169]  # grid lines color
        self.squares_color = [255, 0, 0]

        self.board = create_matrix()
        self.current_piece = None
        self.new_piece = True

        self.running = True  # Variable for the main Game loop

    # Function to read or create the config file for the Game (window width)
    def get_config(self):
        try:
            file = open('config.txt', 'r')
            for i in file.readlines():
                i = i.split(':')
                if 'Window_width' in i[0]:
                    self.window_width = int(i[1])
        except Exception as e:
            if isinstance(e, ValueError) or isinstance(e, IOError):
                print('It was not possible to read the config file\nGoing back to default values')
                try:
                    file = open('config.txt', 'w')
                    file.write('Window_width (px): 300')
                    self.window_width = 300
                except IOError:
                    print('Fatal error creating config file\nPlease verify that you have read and write permissions')
                    exit(0)

    # Function to create the playing window
    def start(self):
        pygame.mixer.init()
        pygame.init()
        pygame.key.set_repeat(200, 50)  # Sets keys to repeat

        self.square_side = int(self.window_width / 10)
        self.window_height = 21 * self.square_side

        self.window = pygame.display.set_mode([self.window_width, self.window_height])
        pygame.display.set_caption(self.window_title)

    # Function to draw grid and update the score
    def draw_grid(self):
        for i in range(1, 21):
            for j in range(10):
                pygame.draw.rect(self.window, self.grid_color,
                                 pygame.Rect(j * self.square_side, i * self.square_side, self.square_side,
                                             self.square_side), 1)

        font = pygame.font.SysFont(None, 30)
        img = font.render('Level ' + str(self.level), True, [0, 0, 0])
        self.window.blit(img, (0, 0))
        img = font.render(str(self.points) + ' Points', True, [0, 0, 0])
        self.window.blit(img, (self.square_side * 4, 0))

    # Function used to draw all the elements in the board
    def draw_board(self):
        self.window.fill(self.background_color)

        i = self.square_side
        for k in self.board:
            j = 0
            for l in k:
                if l == 1:
                    pygame.draw.rect(self.window, self.squares_color,
                                     pygame.Rect(j, i, self.square_side, self.square_side))
                j = j + self.square_side
            i = i + self.square_side

        self.draw_grid()
        pygame.display.update()  # update the display

    # Inserts a Piece into the board
    def insert_piece(self):
        self.current_piece = Piece(5, 0)
        self.running = not self.current_piece.place(self.board)

    # Removes the Piece, moves it and places it on the board
    def move_piece(self, x, y):
        self.current_piece.remove(self.board)
        self.current_piece.x += x
        self.current_piece.y += y
        self.current_piece.place(self.board)

    # Rotates the Piece
    def rotate_piece(self):
        self.current_piece.remove(self.board)
        if self.current_piece.rotation != 3:
            self.current_piece.rotation += 1
        else:
            self.current_piece.rotation = 0
        self.current_piece.place(self.board)

    # Function used to check if the play with the current Piece is over; otherwise the Piece goes down
    def move_down(self):
        i = self.current_piece.get_x()
        j = self.current_piece.get_y()
        for k in range(4):
            if j[k] == 19:
                self.new_piece = True
                self.current_piece = None
            else:
                if self.board[j[k] + 1][i[k]] == 1 and not check_pair_in_list(i, j, i[k], j[k] + 1, 4):
                    self.new_piece = True
                    if j[0] == 0 or j[1] == 0 or j[2] == 0 or j[3] == 0:
                        self.current_piece = None
                        self.running = False  # Ends the Game

        if not self.new_piece:
            self.move_piece(0, 1)

    # Updates the board and the score
    def update_score(self):
        l = 0
        for i in self.board:
            if i == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]:
                self.points += self.points_per_line_cleared
                if self.points % self.points_to_new_level == 0:
                    self.level += 1
                    self.interval = int(self.interval * self.interval_drop)
                for k in range(l):
                    self.board[l - k] = self.board[l - k - 1]
                self.board[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0]  # Weird behaviour observed with a for loop, may be the causa of bugs that may
                # appear
            l += 1

    # Writes the results and ends pygame
    def write_results(self):
        pygame.quit()
        lines = ['*****Results of the Game by chronological order*****\n']
        try:
            file = open("results.txt", "r")
            for i in file.readlines():
                if i != '*****Results of the Game by chronological order*****\n':
                    lines.append(i)
            file.close()
        except IOError:
            pass

        name = input('Introduce your name: ')
        lines.append(name + ': ' + str(self.points) + ' Points\n')

        try:
            file = open("results.txt", "w")
            for i in lines:
                file.write(i)
            file.close()
        except IOError:
            print('Error creating results file\nPlease verify that you have read and write permissions')