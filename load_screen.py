from collections import defaultdict
import threading
import const as c
import pygame
import sys
import os

import sapper
import snake
from snake import *
from classes import *
from sapper import *


def load_image(name, colorkey=None):
    fullname = os.path.join('pictures', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(LoadScreen().get_all_sprites())
        self.frames = []
        self.get_frames()
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 100

    def get_frames(self):
        for i in range(3):
            for j in range(10):
                name = 'splat' + str(i) + str(j) + '.png'
                image = load_image(name).convert_alpha()
                self.frames.append(image)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class LoadScreen:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.sprite = pygame.sprite.Sprite()
        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

    def get_all_sprites(self):
        return self.all_sprites

    def setup(self):
        self.surface = pygame.display.set_mode((c.W, c.H))
        self.paint = AnimatedSprite()
        self.all_sprites.add(self.paint)

        self.greet_text1 = Text(0, 100, 'Welcome to SPLASH!', self.font, centre=True)
        self.greet_text2 = Text(0, 150, 'Press any key to start', self.font, centre=True)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                Menu(self.surface).run()

    def update(self):
        self.paint.update()

    def run(self):
        pygame.display.set_caption('SPLASH!')
        self.setup()

        while True:
            self.surface.fill(c.BACKGROUND_COLOR)
            self.handle_events()
            self.update()
            self.all_sprites.draw(self.surface)
            self.greet_text1.draw(self.surface)
            self.greet_text2.draw(self.surface)

            self.clock.tick(c.PAINT_FPS)
            pygame.display.flip()


class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.exit = False
        self.objects = []
        self.click_handlers1 = []

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

    def setup(self):
        def snake_run():
            snake.game_loop()

        def sapper_run():
            sapper.main(20, 1)

        def cards_run():
            Cards(self.surface).run()

        self.splash_txt = Text(320, 50, 'SPLASH!!<3', self.font, False, c.NAME_COLOR)
        self.snake_btn = Button(100, 150, 'SNAKE', self.font, snake_run, False)
        self.snake_txt = Text(200, 150, 'Feed the hungry snake to earn points', self.font)
        self.sapper_btn = Button(100, c.H // 2, 'SAPPER', self.font, sapper_run, False)
        self.sapper_txt = Text(210, c.H // 2, 'See how it feels to blow up in 10 seconds', self.font)
        self.cards_btn = Button(100, 450, 'MEMO', self.font, cards_run, False)
        self.cards_txt = Text(200, 450, 'Match card with identical one (cats!!!)', self.font)

        self.click_handlers1.extend([self.snake_btn, self.sapper_btn, self.cards_btn])
        self.objects.extend([self. splash_txt, self.snake_txt, self.sapper_txt, self.cards_txt,
                            self.snake_btn, self.sapper_btn, self.cards_btn])

    def draw(self):
        for obj in self.objects:
            obj.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                for handler in self.click_handlers1:
                    handler.on_click(self.surface, event.pos)
            else:
                pass

    def run(self):
        self.setup()

        while True:
            self.surface.fill(c.BACKGROUND_COLOR)
            self.handle_events()
            self.draw()

            pygame.display.flip()


class Cards:
    def __init__(self, surface):
        self.cards = []
        self.state = Status.HAPPENING
        self.round_number = 1
        self.is_running_cards_animation = False
        self.previous_time = None
        self.showing_card_number = 0
        self.exit = False
        self.objects = defaultdict(list)
        self.click_handlers = defaultdict(list)
        self.clock = pygame.time.Clock()
        self.is_click_disabled = False
        self.pics = []
        self.row = c.ROWS_COUNT
        self.column = c.COLUMNS_COUNT
        self.surface = surface

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

    def reset(self):
        self.round_number = 1
        self.is_running_cards_animation = False
        self.previous_time = None
        self.showing_card_number = 0
        self.objects = defaultdict(list)
        self.click_handlers = defaultdict(list)
        self.cards = []
        self.setup()

    def is_game_end(self):
        return all(card.is_matched for card in self.cards)

    def run_cards_animation(self):
        if self.is_running_cards_animation:
            if self.previous_time is None:
                self.previous_time = pygame.time.get_ticks()
            current_time = pygame.time.get_ticks()
            if current_time >= self.previous_time + c.MILLISECOND_TO_SHOW_EACH_CARD:
                if self.showing_card_number >= 1:
                    self.cards[self.showing_card_number - 1].is_selected = False
                if self.showing_card_number < len(self.cards):
                    self.cards[self.showing_card_number].is_selected = True
                    self.previous_time = current_time
                self.showing_card_number += 1
            if self.showing_card_number > len(self.cards):
                self.is_running_cards_animation = False

    def setup(self):
        self.surface = pygame.display.set_mode((c.W, c.H))

        self.create_cards()
        self.create_pause_menu()
        self.create_top_bar()

    def create_cards(self):
        selected_pics = random.sample(self.pics, self.row * self.column // 2)
        selected_pics.extend(selected_pics)
        random.shuffle(selected_pics)

        for x in range(self.row):
            for y in range(self.column):
                card_rect = pygame.Rect(
                    y * c.CARD_SIZE + (c.CARD_GAP * y) + c.CARD_GAP + c.LEFT_GAP,
                    c.TOP_GAP
                    + x * c.CARD_SIZE
                    + (c.CARD_GAP * x)
                    + c.CARD_GAP,
                    c.CARD_SIZE,
                    c.CARD_SIZE,
                )
                pic = selected_pics[x * self.column + y]
                self.cards.append(Card(pic, card_rect))

        self.objects[Status.HAPPENING].extend(self.cards)
        self.click_handlers[Status.HAPPENING].extend(self.cards)

    def create_end_menu(self):
        def on_restart():
            self.reset()
            self.state = Status.HAPPENING
            self.is_running_cards_animation = True

        def on_main_menu():
            Menu(self.surface).run()

        round_to_finish_text = Text(
            0,
            0,
            "Took " + str(self.round_number) + " rounds to finish!!",
            self.font,
            True,
        )

        restart_button = Button(
            0,
            50,
            "Restart",
            self.font,
            on_restart,
            centre=True,
        )
        main_menu_button = Button(
            0,
            100,
            "Main Menu",
            self.font,
            on_main_menu,
            centre=True,
        )

        self.click_handlers[Status.END].extend([restart_button, main_menu_button])
        self.objects[Status.END].extend(
            [round_to_finish_text, restart_button, main_menu_button]
        )

    def create_top_bar(self):
        def on_pause():
            self.state = Status.PAUSED

        round_took_text = Text(
            65, 25, "Round: " + str(self.round_number), self.font, False
        )
        pause_button = Button(
            c.W - 130,
            25,
            "Pause",
            self.font,
            on_pause,
        )

        self.click_handlers[Status.HAPPENING].append(pause_button)
        self.objects[Status.HAPPENING].extend([pause_button, round_took_text])

    def update_top_bar(self):
        text = self.objects[Status.HAPPENING][-1]
        text.text_func = 'Round ' + str(self.round_number)

    def create_pause_menu(self):
        def on_resume():
            self.state = Status.HAPPENING

        def on_restart():
            self.reset()
            self.state = Status.HAPPENING
            self.is_running_cards_animation = True

        def on_main_menu():
            Menu(self.surface).run()

        resume_button = Button(
            0,
            0,
            "Resume",
            self.font,
            on_resume,
            centre=True,
        )
        restart_button = Button(
            0,
            50,
            "Restart",
            self.font,
            on_restart,
            centre=True,
        )
        main_menu_button = Button(
            0,
            100,
            "Main Menu",
            self.font,
            on_main_menu,
            centre=True,
        )

        self.click_handlers[Status.PAUSED].extend(
            [resume_button, restart_button, main_menu_button]
        )
        self.objects[Status.PAUSED].extend(
            [resume_button, restart_button, main_menu_button]
        )

    def check_two_cards_opened(self):
        if self.is_click_disabled:
            return

        opened_cards = [card for card in self.cards if card.is_selected]

        if len(opened_cards) == 2:
            card1, card2 = opened_cards
            self.round_number += 1

            if card1 == card2:
                card1.is_matched = True
                card2.is_matched = True
                card1.is_selected = False
                card2.is_selected = False
            else:
                self.is_click_disabled = pygame.time.get_ticks()

                def update_disable_click_state():
                    self.is_click_disabled = not self.is_click_disabled
                    card1.is_selected = False
                    card2.is_selected = False

                timer = threading.Timer(c.DELAY_TIME, update_disable_click_state)
                timer.start()

    def is_game_finished(self):
        return all(card.is_matched for card in self.cards)

    def update(self):
        if self.exit:
           Menu(self.surface).run()

        if self.state == Status.HAPPENING:
            self.run_cards_animation()
            self.check_two_cards_opened()
            self.update_top_bar()
            is_game_finished = self.is_game_finished()

            if is_game_finished:
                self.create_end_menu()
                self.state = Status.END

    def draw(self):
        for obj in self.objects[self.state]:
            obj.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Menu(self.surface).run()
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.is_click_disabled:
                    return

                for handler in self.click_handlers[self.state]:
                    handler.on_click(self.surface, event.pos)

    def get_pics(self):
        for name in c.FILE_NAMES:
            image = load_image(name)
            image = pygame.transform.scale(image, (c.CARD_SIZE, c.CARD_SIZE))
            pic = Picture(name, image)
            self.pics.append(pic)

    def run(self):
        self.get_pics()
        self.setup()

        while True:
            self.surface.fill(c.BACKGROUND_COLOR)
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(c.FPS)
            pygame.display.flip()


def main():
    LoadScreen().run()


if __name__ == "__main__":
    main()