import pygame
import time
from pygame.locals import *
from random import randint
from pathlib import Path


# Game scale, default: 32
SIZE = 32

# Background colour, default: 110, 110, 5
BACKGROUND = (250, 225, 170)

# Window size, default: 1280, 736
WINDOW = (1280, 736)

STARTLENGTH = 9

FPS = 12


def randPosX():
    return SIZE * randint(1, WINDOW[0] / SIZE - 1)

def randPosY():
    return SIZE * randint(1, WINDOW[1] / SIZE - 1)


class Game:
    def __init__(self):
        pygame.init()
        # Sets window size
        self.surface = pygame.display.set_mode(WINDOW, SRCALPHA)
        # Sets background colour
        self.surface.fill(BACKGROUND)

        self.snake = Snake(self.surface, STARTLENGTH)
        self.snake.draw()


    def reset(self):
        self.snake.length = STARTLENGTH
        self.snake.x[0] = randPosX()
        self.snake.y[0] = randPosY()


    def play(self):
        self.snake.slither()
        pygame.display.flip()


    def run(self):
        running = True
        stop = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # Enter or Space to pause
                    if event.key == K_RETURN or event.key == K_SPACE:
                        stop = not stop
                    # Esc or X button (on the window) to quit
                    if event.key == K_ESCAPE:
                        running = False

                    if not stop:
                        if event.key in (K_w, K_UP):
                            self.snake.turns()
                            self.snake.move('U')
                        if event.key in (K_s, K_DOWN):
                            self.snake.turns()
                            self.snake.move('D')
                        if event.key in (K_a, K_LEFT):
                            self.snake.turns()
                            self.snake.move('L')
                        if event.key in (K_d, K_RIGHT):
                            self.snake.turns()
                            self.snake.move('R')

                    
                if event.type == QUIT:
                    running = False

            try:
                if not stop:
                    self.play()

            except Exception as e:
                print(e)
                stop = True

            time.sleep(1/FPS)


class Snake:
    def __init__(self, surface, length):
        self.surface = surface
        self.length = length

        self.x = [randPosX()] * length
        self.y = [randPosY()] * length

        self.xyd = ['R'] * STARTLENGTH

        self.direction = 'R'
        self.turnPoints = []

        sprite_dir = 'resources'
        sprites = Path(sprite_dir).glob('*')
        for spr in sprites:
            setattr(self, spr.stem, pygame.transform.scale(pygame.image.load(
                spr).convert_alpha(), (SIZE, SIZE)))

        self.body_v = self.body
        self.body_h = pygame.transform.rotate(self.body, 90)


    def turns(self):
        self.turnPoints.append((self.x[0], self.y[0]))
        print(self.xyd)


    def incLength(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


    def draw(self):
        self.surface.fill(BACKGROUND)
        self.surface.blit(self.head, (self.x[0], self.y[0]))

        for i in range(1, self.length - 1):
            if (self.x[i], self.y[i]) in self.turnPoints:
                self.surface.blit(self.turn, (self.x[i], self.y[i]))
            else:

                self.surface.blit(self.body, (self.x[i], self.y[i]))

        self.surface.blit(self.tail, (self.x[-1], self.y[-1]))

        pygame.display.flip()


    def move(self, dir):
        match dir:
            case 'U' if self.direction != 'D':
                self.direction = 'U'
            case 'D' if self.direction != 'U':
                self.direction = 'D'
            case 'L' if self.direction != 'R':
                self.direction = 'L'
            case 'R' if self.direction != 'L':
                self.direction = 'R'


    def slither(self):
        for i in range(self.length - 1, 0 , -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]


        match self.direction:
            case 'U':
                self.y[0] -= SIZE
            case 'D':
                self.y[0] += SIZE
            case 'L':
                self.x[0] -= SIZE
            case 'R':
                self.x[0] += SIZE

        for i, tu in enumerate(self.turnPoints):
            if (tu[0] in self.x and tu[1] not in self.y)\
                or (tu[1] in self.y and tu[0] not in self.x)\
                or (tu[0] not in self.x and tu[1] not in self.y):
                self.turnPoints.pop(i)

        self.xyd.pop(-1)
        self.xyd.insert(0, self.direction)

        self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
