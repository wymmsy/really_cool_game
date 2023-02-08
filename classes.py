from dataclasses import dataclass
from pygame import surface
import pygame
import const as c
from enum import Enum


class Card:
    def __init__(self, picture, rect):
        self.picture = picture
        self.rect = rect
        self.is_matched = False
        self.is_selected = False
        self.is_showing = False

    def __eq__(self, other):
        return self.picture == other.picture

    def draw(self, surface):
        if self.is_matched or self.is_showing or self.is_selected:
            surface.fill(c.WHITE_COLOR, self.rect)
            surface.blit(self.picture.image, self.rect)
        else:
            surface.fill(c.BACK_CARD_COLOR, self.rect)

    def on_click(self, _surface, pos):
        if self.is_matched:
            return

        if self.rect.collidepoint(pos) and not self.is_selected:
            self.is_selected = True


@dataclass
class Picture:
    name: str
    image: pygame.Surface


class Text:
    def __init__(self, x, y, text_func, font, centre=False, color=c.TEXT_COLOR):
        self.pos = x, y
        self.centre = centre
        self.font = font
        self.text_func = text_func
        self.color = color

    def draw(self, surface):
        if self.centre:
            center = surface.get_rect().center
            text_surface = self.font.render(self.text_func, True, self.color)
            pos = text_surface.get_rect(center=center)
            pos.x += self.pos[0]
            pos.y += self.pos[1]
            surface.blit(text_surface, pos)
        else:
            text_surface = self.font.render(self.text_func, True, self.color)
            surface.blit(text_surface, self.pos)

    def rect(self, surface):
        text_surface = self.font.render(self.text_func, True, self.color)
        if self.centre:
            center = surface.get_rect().center
            pos = text_surface.get_rect(center=center)
        else:
            pos = text_surface.get_rect()
        pos.x += self.pos[0]
        pos.y += self.pos[1]
        return pos


class Button:
    def __init__(self, x, y, text_func, font, do_click=lambda x: None,
                 centre=False, btn_color=c.BTN_COLOR, text_color=c.TEXT_COLOR):
        self.do_click = do_click
        self.text = Text(x, y, text_func, font, centre, text_color)
        self.btn_color = btn_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.btn_color, self.text.rect(surface))
        self.text.draw(surface)

    def on_click(self, surface, pos):
        if self.text.rect(surface).collidepoint(pos):
            self.do_click()


class Status(Enum):
    MAIN_MENU = 1
    HAPPENING = 2
    PAUSED = 3
    END = 4