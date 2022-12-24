import pygame
import time
from pygame.locals import *
from random import randint
from pathlib import Path
from config import BACKGROUND, FPS, SIZE, STARTLENGTH, WINDOW


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
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # Enter or Space to pause
                    if event.key == K_RETURN or event.key == K_SPACE:
                        pause = not pause
                    # Esc or X button (on the window) to quit
                    if event.key == K_ESCAPE:
                        running = False

                    if not pause:
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
                if not pause:
                    self.play()

            except Exception as e:
                print(e)
                pause = True

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

        self.head_u = self.head
        self.head_d = pygame.transform.rotate(self.head, 180)
        self.head_l = pygame.transform.rotate(self.head, 90)
        self.head_r = pygame.transform.rotate(self.head, -90)

        self.tail_u = self.tail
        self.tail_d = pygame.transform.rotate(self.tail, 180)
        self.tail_l = pygame.transform.rotate(self.tail, 90)
        self.tail_r = pygame.transform.rotate(self.tail, -90)

        self.turn_dl = self.turn
        self.turn_dr = pygame.transform.rotate(self.turn, 90)
        self.turn_ul = pygame.transform.rotate(self.turn, -90)
        self.turn_ur = pygame.transform.rotate(self.turn, 180)


    def turns(self):
        self.turnPoints.append((self.x[0], self.y[0]))
        print(self.xyd)


    def incLength(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


    def draw(self):
        self.surface.fill(BACKGROUND)

        # Render head
        coords_head = (self.x[0], self.y[0])
        match self.xyd[0]:
            case 'U':
                self.surface.blit(self.head_u, coords_head)
            case 'D':
                self.surface.blit(self.head_d, coords_head)
            case 'L':
                self.surface.blit(self.head_l, coords_head)
            case 'R':
                self.surface.blit(self.head_r, coords_head)

        # Render body
        for i in range(1, self.length - 1):
            coords = (self.x[i], self.y[i])
            match self.xyd[i]:
                # Straight body
                case 'U' | 'D' if self.xyd[i - 1] in ['U', 'D']:
                    self.surface.blit(self.body_v, coords)
                case 'L' | 'R' if self.xyd[i - 1] in ['L', 'R']:
                    self.surface.blit(self.body_h, coords)

                # Turning body
                case 'R' if self.xyd[i - 1] == 'U':
                    self.surface.blit(self.turn_ul, coords)
                case 'D' if self.xyd[i - 1] == 'L':
                    self.surface.blit(self.turn_ul, coords)

                case 'L' if self.xyd[i - 1] == 'U':
                    self.surface.blit(self.turn_ur, coords)
                case 'D' if self.xyd[i - 1] == 'R':
                    self.surface.blit(self.turn_ur, coords)

                case 'U' if self.xyd[i - 1] == 'L':
                    self.surface.blit(self.turn_dl, coords)
                case 'R' if self.xyd[i - 1] == 'D':
                    self.surface.blit(self.turn_dl, coords)

                case 'U' if self.xyd[i - 1] == 'R':
                    self.surface.blit(self.turn_dr, coords)
                case 'L' if self.xyd[i - 1] == 'D':
                    self.surface.blit(self.turn_dr, coords)

        # Render tail
        coords_tail = (self.x[-1], self.y[-1])
        match self.xyd[-2]:
            case 'U':
                self.surface.blit(self.tail_u, coords_tail)
            case 'D':
                self.surface.blit(self.tail_d, coords_tail)
            case 'L':
                self.surface.blit(self.tail_l, coords_tail)
            case 'R':
                self.surface.blit(self.tail_r, coords_tail)

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
