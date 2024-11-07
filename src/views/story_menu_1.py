import pygame
import sys
from views import *

def scroll_text(screen, text, speed=1, size=35, color=(255, 255, 255), back_button_color=(255, 255, 255)):
    # Posição inicial
    y_pos = screen.get_height()
    lines = text.splitlines()
    running = True

    imagem = pygame.image.load("C:/Users/raphy/elemental_fusion_game/assets/images/fundo_story_menu.png").convert()
    imagem = pygame.transform.scale(imagem, screen.get_size())
    back_button_pos = (60, 50)
    clock = pygame.time.Clock() 

    while running:

        screen.blit(imagem, (0, 0))

        for i, line in enumerate(lines):
            draw_text(screen, line, screen.get_width() // 2, y_pos + i * size, size, color)

        y_pos -= speed  

        if y_pos + len(lines) * size < 0:
            running = False

        draw_text(screen, "Back", back_button_pos[0], back_button_pos[1], 30, back_button_color)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                back_button_rect = pygame.Rect(back_button_pos[0], back_button_pos[1], 60, 30) 
                if back_button_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return

def story_menu(screen):

    with open("C:/Users/raphy/elemental_fusion_game/assets/texts/story_level_1.txt", "r", encoding="utf-8") as file:
        story_text = file.read()

    pygame.mixer.music.load("C:/Users/raphy/elemental_fusion_game/assets/audio/Star Wars - Main Theme.mp3")
    pygame.mixer.music.play(-1)

    scroll_text(screen, story_text, speed=2)