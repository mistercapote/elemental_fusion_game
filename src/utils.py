import pygame
from constants import *
import math

def draw_text(screen, text, x, y, size=40, color=WHITE):
    font = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", size)
    surface = font.render(text, True, color)
    rect_text = surface.get_rect(center=(x,y))
    screen.blit(surface, rect_text)
    return rect_text

def nucleo_pos(angle, radius):
    x = 3*CENTER_X//2 + radius * math.cos(angle)
    y = CENTER_Y + radius * math.sin(angle)
    return [x,y]