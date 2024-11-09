import pygame
import sys
from views import *
from constants import *
from models.draw import ButtonStarting

def draw_text(screen, text, x, y, size, color):
    font = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)
    return rect

def story_menu(game):
    lines = game.get_story_text().splitlines()
    imagem = game.get_story_image()
    pygame.mixer.music.load(game.story_music)
    pygame.mixer.music.play(-1)

    size = 35
    ypos = HEIGHT_MAX

    running = True
    back_button = ButtonStarting(game.screen, "Back", 80, 50)
    
    while running:
        game.screen.blit(imagem, (0, 0))
        ypos -= 2

        #Desenha cada linha
        for i, line in enumerate(lines):
            draw_text(game.screen, line, CENTER_X, ypos + i * size, size, WHITE)

        #Quando acaba de subir o texto, volta para a tela principal
        if ypos + len(lines) * size < 0: running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = back_button.check_click(event, running)
                pygame.mixer.music.stop()

        #Hover effect
        back_button.draw(game.screen, pygame.mouse.get_pos())
        
        pygame.display.flip()
        