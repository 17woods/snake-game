import pygame
from random import randint


# Game scale, default: 32
SIZE = 32

# Background colour, default: 110, 110, 5
BACKGROUND = (110, 110, 5)

# Window size, default: 1280, 736
WINDOW = (1280, 736)

STARTLENGTH = 3

FPS = 15


def randPosX():
    return SIZE * randint(1, WINDOW[0] / SIZE - 1)

def randPosY():
    return SIZE * randint(1, WINDOW[1] / SIZE - 1)


class Game:
    def __init__(self):
        pygame.init()
        # Sets window size
        self.surface = pygame.display.set_mode(WINDOW)
        # Sets background colour
        self.surface.fill(BACKGROUND)


if __name__ == "__main__":
    game = Game()
    game.run()