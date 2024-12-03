import pygame
from views import *
from constants import *
from models.character import Character
from models.button import BackingButton

def start_menu(game):
    character = Character()
    back_button = BackingButton(game.screen, "Voltar", 18*SQUARE_WIDTH, 11*SQUARE_HEIGHT)
    
    running = True
    while running:
        game.screen.fill(BLACK)
        game.screen.blit(character.scenario, character.scenario_rect.topleft)
        back_button.draw(game.screen)
        character.walk()
        character.draw(game.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = back_button.check_click(event, running)

        
        pygame.display.flip() 