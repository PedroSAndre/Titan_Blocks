#####################################################Piece.py###########################################################
# Encoding: UTF-8

# Class to represent a Piece on a board and all it's rotations and movements
# Also, here all collisions are detected and handled

# Author:

# Pedro Silva André
########################################################################################################################

# Modules Import
import random as rand


class Piece:
    def __init__(self, x, y):
        self.piece = rand.randint(0, 6)  # generates a random Piece
        self.rotation = 0
        self.x = x
        self.y = y
        self.oldx = None
        self.oldy = None
        self.oldrotation = None
        self.relatives = [[0, 0], [0, 0], [0, 0]]  # other squares of the Piece

    def neighbour(self):
        if self.piece == 0:
            self.relatives = [[1, 0], [-1, 0], [-2, 0]]
        if self.piece == 1:
            self.relatives = [[1, 0], [0, 1], [0, 2]]
        if self.piece == 2:
            self.relatives = [[-1, 0], [0, 1], [0, 2]]
        if self.piece == 3:
            self.relatives = [[-1, 0], [-1, 1], [0, 1]]
        if self.piece == 4:
            self.relatives = [[1, 0], [0, 1], [-1, 1]]
        if self.piece == 5:
            self.relatives = [[0, 1], [1, 0], [-1, 0]]
        if self.piece == 6:
            self.relatives = [[-1, 0], [0, 1], [1, 1]]

    # Gets all the x of the Piece
    def get_x(self):
        list1 = [self.x]
        for i in self.relatives:
            list1.append(i[0] + self.x)

        return list1

    # Gets all the y from the Piece
    def get_y(self):
        list1 = [self.y]
        for i in self.relatives:
            list1.append(i[1] + self.y)

        return list1

    # Rotates the Piece
    def do_rotation(self):
        if self.rotation == 1 or self.rotation == 3:
            for i in self.relatives:
                j = i[0]
                i[0] = i[1]
                i[1] = j
        if self.rotation == 1 or self.rotation == 2:
            for i in self.relatives:
                i[0] = -i[0]
        if self.rotation == 2 or self.rotation == 3:
            for i in self.relatives:
                i[1] = -i[1]

    # Self-explanatory
    def refresh(self):
        self.neighbour()
        self.do_rotation()

    # Puts a Piece on the board
    def place(self, matrix):
        self.refresh()
        self.move_in_bounds()
        gameover = self.check_colisions_with_pieces(matrix)
        matrix[self.y][self.x] = 1
        for i in self.relatives:
            matrix[i[1] + self.y][i[0] + self.x] = 1
        return gameover

    # Removes the Piece from the board
    def remove(self, matrix):
        self.oldx = self.x
        self.oldy = self.y  # This is done so that the last position is never lost
        self.oldrotation = self.rotation
        matrix[self.y][self.x] = 0
        for i in self.relatives:
            matrix[i[1] + self.y][i[0] + self.x] = 0

    # Makes sure the Piece stays in bounds
    def move_in_bounds(self):
        self.change_coordinates_x()
        self.change_coordinates_y()

    # Doesn't allow the Piece to move if it collides with another already on the board
    def check_colisions_with_pieces(self, matrix):
        listx = self.get_x()
        listy = self.get_y()
        gameover = False
        for i in range(4):
            if matrix[listy[i]][listx[i]] == 1:
                if self.oldx is None and self.oldy is None and self.oldrotation is None:
                    gameover = True
                    return gameover
                else:
                    self.x = self.oldx
                    self.y = self.oldy
                    self.rotation = self.oldrotation
                    self.refresh()
                    return gameover

    def change_coordinates_x(self):  # for some reason a general function for x and y didn't work
        done = False
        while not done:
            units_to_move = 0
            done = True
            if self.x < 0:
                units_to_move = -1 * self.x
            elif self.x >= 10:
                units_to_move = 10 - 1 - self.x
            else:
                for i in self.relatives:
                    if (i[0] + self.x) < 0:
                        units_to_move = -(i[0] + self.x)
                    elif (i[0] + self.x) >= 10:
                        units_to_move = 10 - 1 - (i[0] + self.x)

            if units_to_move != 0:
                self.x = self.x + units_to_move
                done = False

    def change_coordinates_y(self):  # for some reason a general function for y and y didn't work
        done = False
        while not done:
            units_to_move = 0
            done = True
            if self.y < 0:
                units_to_move = -1 * self.y
            elif self.y >= 20:
                units_to_move = 20 - 1 - self.y
            else:
                for i in self.relatives:
                    if (i[1] + self.y) < 0:
                        units_to_move = -(i[1] + self.y)
                    elif (i[1] + self.y) >= 20:
                        units_to_move = 20 - 1 - (i[1] + self.y)

            if units_to_move != 0:
                self.y = self.y + units_to_move
                done = False