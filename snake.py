import pygame
import random


pygame.init()
white = (255, 255, 255)
violet = (148, 0, 211)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (105, 160, 201)
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()
timer = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 30)


def your_score(score, level):
    value = score_font.render("Your score: " + str(score), True, violet)
    level = score_font.render(f'Level {level}', True, violet)
    screen.blit(value, [35, 30])
    screen.blit(level, [35, 70])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.circle(screen, green, ((2 * x[0] + snake_block) // 2,
                                           (2 * x[1] + snake_block) // 2), snake_block // 2 + 1)


def message(msg, color, f=0):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3 + f])

def display_time(time_s):
    time_str = str(int(time_s * 10) / 10)
    label = font_style.render(f"Time : {time_str}", True, (148, 0, 211))
    screen.blit(label, (600, 60))


def game_loop(level=1):
    snake_block = 10
    snake_speed = 5 * level
    game_over = False
    game_close = False
    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0
    snake_list = []
    length_of_snake = 1
    foodx = round(random.randrange(30, width - snake_block - 30) / 10.0) * 10.0
    foody = round(random.randrange(30, height - snake_block - 30) / 10.0) * 10.0
    time_seconds = 0
    t = False
    time_millis = timer.tick(30)
    pygame.draw.rect(screen, 'black', (30, 30, 740, 540), width=1)
    while not game_over:
        screen.fill((105, 160, 201))
        pygame.draw.rect(screen, 'black', (30, 30, 740, 540), width=1)
        display_time(time_seconds)
        while game_close:
            screen.fill((105, 160, 201))
            pygame.draw.rect(screen, 'black', (30, 30, 740, 540), width=1)
            your_score(length_of_snake - 1, level)
            display_time(time_seconds)
            if length_of_snake - 1 == 10 and level < 3:
                message("Congrats! You completed the level!", violet)
                message("Press Q to exit or C for next level", violet, f=50)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            game_loop(level + 1)
                    if event.type == pygame.QUIT:
                        game_over = True
                        game_close = False
            elif level == 3 and length_of_snake - 1 == 10:
                message("Congrats! You wone!", green)
                message("Press Q to exit or C to restart", green, f=50)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            game_loop()
                    if event.type == pygame.QUIT:
                        game_over = True
                        game_close = False
            else:
                message("Game over :(", red)
                message("Press Q to exit or C to restart the level", red, f=50)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            game_loop(level)
                    if event.type == pygame.QUIT:
                        game_over = True
                        game_close = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                if event.key == pygame.K_q:
                    return
                if event.key == pygame.K_c:
                    return game_loop()
                time_millis = timer.tick(30)
                t = True
        if x1 > 760 or x1 < 40 or y1 > 560 or y1 < 40:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(blue)
        pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block])
        pygame.draw.rect(screen, 'black', (30, 30, 740, 540), width=1)
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True
        our_snake(snake_block, snake_list)
        your_score(length_of_snake - 1, level)
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(30, width - snake_block - 30) / 10.0) * 10.0
            foody = round(random.randrange(30, height - snake_block - 30) / 10.0) * 10.0
            length_of_snake += 1
        clock.tick(snake_speed)
        if length_of_snake - 1 == 10:
            game_close = True
        if t:
            time_millis = timer.tick(30)
            time_seconds += time_millis / 1000
        display_time(time_seconds)
        pygame.display.flip()
    #pygame.quit()