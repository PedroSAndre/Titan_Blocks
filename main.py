#####################################################main.py############################################################
# Encoding: UTF-8

# Main file of the Game
# Contains main loop and makes all the references to the main class Game

# Author:

# Pedro Silva André
########################################################################################################################

# Modules Import
import pygame

# Import from other project scripts
from game import Game


def main():
    # Starting program procedures
    game = Game()

    # Reading config
    game.get_config()

    # Starting pygame
    game.start()

    last_drop = pygame.time.get_ticks()  # Sets the clock
    while game.running:
        if game.new_piece:
            game.update_score()
            game.insert_piece()
            game.new_piece = False
            if not game.running:
                break

        game.draw_board()  # Draws everything needed on the screen

        for event in pygame.event.get():  # All the events of the Game
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_piece(1, 0)
                elif event.key == pygame.K_SPACE:
                    game.rotate_piece()
                elif event.key == pygame.K_DOWN:
                    game.move_down()  # Checks to see if there is a collision and a new Piece needs to be introduced
                    last_drop = pygame.time.get_ticks()

        if (pygame.time.get_ticks() - last_drop) > game.interval:
            game.move_down()  # Checks to see if there is a collision and a new Piece needs to be introduced
            last_drop = pygame.time.get_ticks()

    game.write_results()  # Writes results
    del game


if __name__ == "__main__":
    main()