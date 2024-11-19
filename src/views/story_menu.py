import pygame
from constants import *
from models.button import BackingButton

def story_menu(game):
    lines, image = game.start_story()
    back_button = BackingButton(game.screen, "Back", 80, 50)
    ypos = HEIGHT_MAX
    size = 35
    speed = 0.08

    running = True
    while running:
        game.screen.blit(image, (0, 0))
        ypos -= speed

        #Desenha cada linha
        for i, line in enumerate(lines):
            write(game.screen, line, FONT_STORY, WHITE, (CENTER_X, ypos + i * size))
            
        #Quando acaba de subir o texto, volta para a tela principal
        if ypos + len(lines) * size < 0: running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = back_button.check_click(event, running)

        #Hover effect
        back_button.draw(game.screen)

        pygame.display.flip()
        