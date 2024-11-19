import pygame
from constants import *
from abc import ABC, abstractmethod

class Button(ABC):
    def __init__(self, screen, text, x, y, action=None):
        self.text = text
        self.xpos = x
        self.ypos = y
        self.hovered = False
        self.color = WHITE
        self.rect = self.rects(screen)
        self.action = action

    def draw(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()): self.hovered = True
        else: self.hovered = False
        self.rects(screen)

    def rects(self, screen):
        if self.hovered: surface = FONT_BUTTON_HOVER.render(self.text, True, GRAY)
        else: surface = FONT_BUTTON.render(self.text, True, WHITE)
        rect = surface.get_rect(center=(self.xpos,self.ypos))
        screen.blit(surface, rect)
        return rect
    
    @abstractmethod
    def check_click(self):
        pass

class OpeningButton(Button):
    def check_click(self, event, game):
        if self.rect.collidepoint(event.pos):
            if self.action:
                game.stop_media()
                self.action(game)
                game.start_media()
        return
   
class CleaningButton(Button):
    def check_click(self, event):
        if self.rect.collidepoint(event.pos):
            if self.action:
                self.action()
    
class BackingButton(Button):
    def check_click(self, event, running):
        if self.rect.collidepoint(event.pos):
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            return not running
        return running

class PopUpButton(Button):
    def check_click(self, event, game, label):
        if self.rect.collidepoint(event.pos):
            if label == "start":
                game.start_popup.pop(0)
            elif label == "table":
                game.table_popup.pop(0)
        return game
 