import pygame
from pygame.locals import *
from time import sleep
from random import randint
from config import BACKGROUND, GRID, FPS, SIZE, STARTLENGTH, W_SIZE, W_X, W_Y


def rand_x() -> int:
    return SIZE * randint(1, W_SIZE[0] / SIZE - 2)


def rand_y() -> int:
    return SIZE * randint(1, W_SIZE[1] / SIZE - 2)


def resource(name):
    return pygame.transform.scale(pygame.image.load(
        f'resources/{name}.png').convert_alpha(), GRID)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake')
        # Sets window size
        self.surface = pygame.display.set_mode((W_X, W_Y + 48), SRCALPHA)
        # Sets background colour
        self.surface.fill(BACKGROUND)

        self.snake = Snake(self.surface)
        self.mouse = Mouse(self.surface)
        self.wall = Wall(self.surface)

        self.highscore = 0

    def score(self):
        return self.snake.length - STARTLENGTH

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.score()}', True, (0, 0, 0))
        highscore = font.render(f'High Score: {self.highscore}', True, (0, 0, 0))
        self.surface.blit(score, (12, W_Y + 6))
        self.surface.blit(highscore, (W_X - 200, W_Y + 6))

    def reset(self):
        self.snake = Snake(self.surface)

    def play(self):
        self.snake.slither()
        self.wall.draw()

        if self.snake.hit_mouse(self.mouse):
            self.mouse.move(self.snake)
            self.snake.inc_len()

        if self.snake.hit_wall() or self.snake.hit_self():
            self.highscore = max(self.highscore, self.score())
            raise Exception('Game Over')

        self.mouse.draw()
        self.display_score()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # Enter or Space to pause
                    if event.key in (K_RETURN, K_SPACE):
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
                self.game_over()
                pause = True
                self.reset()

            sleep(1/FPS)

    def game_over(self):
        final_score = self.snake.length - STARTLENGTH
        self.surface.fill(BACKGROUND)
        font = pygame.font.SysFont("arial", 30)

        line1 = font.render('Game Over!', True, (0,0,0))
        line2 = font.render(f'Your score: {final_score}', True, (0,0,0))
        line3 = font.render('Press enter to play again...', True, (0,0,0))

        self.surface.blit(line1, (200, 240))
        self.surface.blit(line2, (200, 275))
        self.surface.blit(line3, (200, 320))

        pygame.display.flip()


class Snake:
    def __init__(self, surface):
        self.surface = surface
        self.length = STARTLENGTH

        self.x = [W_SIZE[0] / SIZE // 2 * SIZE] * self.length
        self.y = [W_SIZE[1] / SIZE // 2 * SIZE] * self.length

        self.xyd = ['R'] * STARTLENGTH

        self.direction = 'R'
        self.turn_points = []

        self.body_v = resource('body')
        self.body_h = pygame.transform.rotate(self.body_v, 90)

        self.head_u = resource('head')
        self.head_d = pygame.transform.rotate(self.head_u, 180)
        self.head_l = pygame.transform.rotate(self.head_u, 90)
        self.head_r = pygame.transform.rotate(self.head_u, -90)

        self.tail_u = resource('tail')
        self.tail_d = pygame.transform.rotate(self.tail_u, 180)
        self.tail_l = pygame.transform.rotate(self.tail_u, 90)
        self.tail_r = pygame.transform.rotate(self.tail_u, -90)

        self.turn_dl = resource('turn')
        self.turn_dr = pygame.transform.rotate(self.turn_dl, 90)
        self.turn_ul = pygame.transform.rotate(self.turn_dl, -90)
        self.turn_ur = pygame.transform.rotate(self.turn_dl, 180)

    def turns(self):
        self.turn_points.append((self.x[0], self.y[0]))

    def inc_len(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
        self.xyd.append(-1)

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

    def move(self, next_dir):
        match next_dir:
            case 'U' if self.xyd[0] != 'D':
                self.direction = 'U'
            case 'D' if self.xyd[0] != 'U':
                self.direction = 'D'
            case 'L' if self.xyd[0] != 'R':
                self.direction = 'L'
            case 'R' if self.xyd[0] != 'L':
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

        for i, tu in enumerate(self.turn_points):
            if (tu[0] in self.x and tu[1] not in self.y)\
                or (tu[1] in self.y and tu[0] not in self.x)\
                or (tu[0] not in self.x and tu[1] not in self.y):
                self.turn_points.pop(i)

        self.xyd.pop(-1)
        self.xyd.insert(0, self.direction)

        self.draw()

    def hit_mouse(self, mouse) -> bool:
        return self.x[0] == mouse.x and self.y[0] == mouse.y

    def hit_wall(self) -> bool:
        return self.x[0] not in range(SIZE, W_SIZE[0] - SIZE) or\
            self.y[0] not in range(SIZE, W_SIZE[1] - SIZE)

    def hit_self(self) -> bool:
        return any(self.x[0] == self.x[i] and self.y[0] == self.y[i]\
            for i in range(3, self.length))


class Mouse:
    def __init__(self, surface):
        self.surface = surface
        self.image = resource('mouse')

        self.x = rand_x()
        self.y = rand_y()

        self.counter = 0

    def draw(self):
        # Flips every 7 frames
        if self.counter % 7 == 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.surface.blit(self.image, (self.x, self.y))
        self.counter += 1

    def move(self, snake: Snake):
        snk_coords = list(zip(snake.x, snake.y))
        while (self.x, self.y) in snk_coords:
            self.x = rand_x()
            self.y = rand_y()


class Wall:
    def __init__(self, surface):
        self.image = resource('wall')
        self.surface = surface

        self.coords_wall = []
        for q in range(W_SIZE[0] // SIZE):
            self.coords_wall.append((q * SIZE, 0))
            self.coords_wall.append((q * SIZE, W_SIZE[1] - SIZE))
            self.coords_wall.append((0, q * SIZE))
            self.coords_wall.append((W_SIZE[0] - SIZE, q * SIZE))

    def draw(self):
        for coords in self.coords_wall:
            self.surface.blit(self.image, coords)


if __name__ == '__main__':
    game = Game()
    game.run()
