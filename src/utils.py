import pygame
from constants import *

def draw_text(screen, text, x, y, size=40, color=WHITE):
    font = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", size)
    surface = font.render(text, True, color)
    rect_text = surface.get_rect(center=(x,y))
    screen.blit(surface, rect_text)
    return rect_text
