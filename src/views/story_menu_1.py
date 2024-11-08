import pygame
import sys
from views import *

def draw_text(screen, text, x, y, size, color):
    font = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)
    return rect

def scroll_text(game, text, speed=1, size=35, color=(255, 255, 255), back_button_color=(255, 255, 255)):
    # Posição inicial
    y_pos = game.screen.get_height()
    lines = text.splitlines()
    running = True

    imagem = pygame.image.load("assets/images/fundo_story_menu.png").convert()
    imagem = pygame.transform.scale(imagem, game.screen.get_size())
    back_button_pos = (60, 50)
    clock = pygame.time.Clock() 

    while running:
        game.screen.blit(imagem, (0, 0))

        for i, line in enumerate(lines):
            draw_text(game.screen, line, game.screen.get_width() // 2, y_pos + i * size, size, color)
        y_pos -= speed  

        if y_pos + len(lines) * size < 0:
            running = False
        draw_text(game.screen, "Back", back_button_pos[0], back_button_pos[1], 30, back_button_color)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                back_button_rect = pygame.Rect(back_button_pos[0], back_button_pos[1], 60, 30) 
                if back_button_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return

def story_menu(game):

    with open("assets/texts/story_level_1.txt", "r", encoding="utf-8") as file:
        story_text = file.read()

    pygame.mixer.music.load("assets/audio/Star Wars - Main Theme.mp3")
    pygame.mixer.music.play(-1)

    scroll_text(game, story_text, speed=2)