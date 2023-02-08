import pygame
import os
import random
import sys

pygame.init()
sys.setrecursionlimit(15000)
font_style = pygame.font.SysFont("comicsansms", 30)
size = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
time_seconds = 0

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        color = pygame.Color('white')
        for y in range(self.height):
            for x in range(self.width):
                coor = (x * self.cell_size + self.left,
                        y * self.cell_size + self.top, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, color, coor, 1)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def on_click(self, cell):
        pass

    def guess(self, cell):
        pass

    def get_click(self, mouse_pos, r):
        cell = self.get_cell(mouse_pos)
        if cell and r:
            return self.on_click(cell)
        if cell and not r:
            return self.guess(cell)


class Minesweeper(Board):
    def __init__(self, width, height, need):
        super().__init__(width, height)
        self.board = [[-1] * width for _ in range(height)]
        self.drawing_board = [[-1] * width for _ in range(height)]
        ter = 0
        while ter < need:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] == -1:
                self.board[y][x] = 10
                ter += 1
        self.make_field((0, 0))

    def make_field(self, cell):
        x, y = cell
        if self.board[y][x] == 10:
            self.drawing_board[y][x] = 10
        s = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                    continue
                if self.board[y + dy][x + dx] == 10:
                    s += 1
        for x1 in range(self.width):
            for y1 in range(self.height):
                s1 = 0
                if self.board[y1][x1] == -1:
                    for dy1 in range(-1, 2):
                        for dx1 in range(-1, 2):
                            if 0 <= x1 + dx1 < self.width and 0 <= y1 + dy1 < self.height:
                                if self.board[y1 + dy1][x1 + dx1] == 10:
                                    s1 += 1
                    if s1 >= 0:
                        self.board[y1][x1] = s1
        self.board[y][x] = s
        return self.board

    def guess(self, cell):
        self.drawing_board[cell[1]][cell[0]] = -5

    def check_coords(self, y, x):
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.board[y][x]:
                self.drawing_board[y][x] = self.board[y][x]
            else:
                if self.drawing_board[y][x] == -1:
                    self.open_click((x, y))
            return True
        return False

    def open_click(self, cell):
        x, y = cell
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.board[y][x] == 10:
                self.drawing_board[y][x] = 10
                return False
            s = self.board[y][x]
            self.drawing_board[y][x] = s
            if s == 0:
                self.check_coords(y + 1, x + 1)
                self.check_coords(y + 1, x - 1)
                self.check_coords(y + 1, x)
                self.check_coords(y - 1, x + 1)
                self.check_coords(y - 1, x - 1)
                self.check_coords(y - 1, x)
                self.check_coords(y, x + 1)
                self.check_coords(y, x - 1)
            return True

    def on_click(self, cell):
        return self.open_click(cell)

    def load_image(self, name):
        fullname = os.path.join(name)
        image = pygame.image.load(fullname)
        return image

    def show_all(self, screen):
        self.drawing_board = self.board
        all_sprites = pygame.sprite.Group()
        for y in range(self.height):
            for x in range(self.width):
                coor = (x * self.cell_size + self.left, y * self.cell_size + self.top,
                        self.cell_size, self.cell_size)
                coor1 = (x * self.cell_size + self.left + 2, y * self.cell_size + self.top + 2,
                         self.cell_size, self.cell_size)
                if self.drawing_board[y][x] == 10:
                    pygame.draw.rect(screen, (148, 0, 211), coor)
                    bomb_image = self.load_image('bomb.png')
                    bomb_image = pygame.transform.scale(bomb_image, (self.cell_size, self.cell_size))
                    bomb = pygame.sprite.Sprite(all_sprites)
                    bomb.image = bomb_image
                    bomb.rect = bomb.image.get_rect()
                    bomb.rect.x = coor[0]
                    bomb.rect.y = coor[1]
                    all_sprites.draw(screen)
                pygame.draw.rect(screen, pygame.Color('white'), coor, 1)
                if self.drawing_board[y][x] >= 0 and self.board[y][x] != 10:
                    font = pygame.font.Font(None, self.cell_size - 7)
                    text = font.render(str(self.board[y][x]), True, (148, 0, 211))
                    screen.blit(text, coor1)

    def render(self, screen):
        all_sprites = pygame.sprite.Group()
        color = pygame.Color((148, 0, 211))
        no = False
        for y in range(self.height):
            for x in range(self.width):
                coor = (x * self.cell_size + self.left, y * self.cell_size + self.top,
                        self.cell_size, self.cell_size)
                coor1 = (x * self.cell_size + self.left + 2, y * self.cell_size + self.top + 2,
                         self.cell_size, self.cell_size)
                if self.drawing_board[y][x] == 10:
                    pygame.draw.rect(screen, color, coor)
                    bomb_image = self.load_image('bomb.png')
                    bomb_image = pygame.transform.scale(bomb_image, (self.cell_size, self.cell_size))
                    bomb = pygame.sprite.Sprite(all_sprites)
                    bomb.image = bomb_image
                    bomb.rect = bomb.image.get_rect()
                    bomb.rect.x = coor[0]
                    bomb.rect.y = coor[1]
                    all_sprites.draw(screen)
                    no = True
                if self.drawing_board[y][x] == -5:
                    pygame.draw.rect(screen, (148, 0, 211), coor)
                pygame.draw.rect(screen, pygame.Color('white'), coor, 1)
                if self.drawing_board[y][x] >= 0 and self.board[y][x] != 10:
                    font = pygame.font.Font(None, self.cell_size - 7)
                    text = font.render(str(self.board[y][x]), True, (148, 0, 211))
                    screen.blit(text, coor1)
        if no:
            pygame.display.flip()
            return False


def message(msg, color, x=10, y=10):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [x, y])


def your_score(level):
    level = font_style.render(f'Level {level}', True, (148, 0, 211))
    screen.blit(level, [10, 460])

def display_time(time_s):
    time_str = str(int(time_s * 10) / 10)
    label = font_style.render(f"Time : {time_str}", True, (148, 0, 211))
    screen.blit(label, (600, 60))

def main(need, level=1, w=10, h=15):
    global time_seconds
    board = Minesweeper(w, h, need)
    running = True
    close = False
    lose = False
    win = False
    time_millis = clock.tick(30)
    time_seconds = 0
    while running:
        screen.fill((105, 160, 201))
        # display_time(time_seconds)
        while close:
            screen.fill((105, 160, 201))
            your_score(level)
            board.show_all(screen)
            display_time(time_seconds)
            if lose:
                message("Game over :(", (148, 0, 211), x=450, y=10)
                message("Press Q to exit or C to restart the level", (148, 0, 211), x=10, y=500)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            running = False
                            close = False
                        if event.key == pygame.K_c:
                            running = False
                            main(need, level)
                            break
                    if event.type == pygame.QUIT:
                        close = False
                        running = False
            if win:
                if level < 3:
                    message("Congrats! You completed the level!", (148, 0, 211), x=450, y=10)
                    message("Press Q to exit or C for next level", (148, 0, 211), x=10, y=500)
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                running = False
                                close = False
                            if event.key == pygame.K_c:
                                running = False
                                main(need + 10, level + 1)
                        if event.type == pygame.QUIT:
                            close = False
                            running = False
                elif level == 3:
                    message("Congrats! You wone!", (148, 0, 211), x=450, y=10)
                    message("Press Q to exit or C for bonus level", (148, 0, 211), x=10, y=500)
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                running = False
                                close = False
                            if event.key == pygame.K_c:
                                running = False
                                main(50, level + 1, 15, 15)
                        if event.type == pygame.QUIT:
                            close = False
                else:
                    message("Congrats! You wone!", (148, 0, 211), x=450, y=10)
                    message("Press Q to exit or C to restart", (148, 0, 211), x=10, y=500)
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                running = False
                                close = False
                            if event.key == pygame.K_c:
                                running = False
                                main(20)
                        if event.type == pygame.QUIT:
                            close = False
                            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    close = False
                if event.key == pygame.K_c:
                    return main(need, level, w, h)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos, 1)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                board.get_click(event.pos, 0)
        if running is False:
            break
        your_score(level)
        a = board.render(screen)
        if a is False:
            close = True
            lose = True
        if sum(list(i.count(-5) for i in board.drawing_board)) == need and \
                sum(list(i.count(-1) for i in board.drawing_board)) == 0:
            close = True
            win = True
        display_time(time_seconds)
        time_millis = clock.tick(30)
        time_seconds += time_millis / 1000
        pygame.display.flip()
    #pygame.quit()
