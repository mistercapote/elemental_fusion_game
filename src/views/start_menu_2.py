import pygame
from views import *
from constants import *
from models.character import Character, doors
from models.button import BackingButton

def start_menu(game):
    character = Character()
    back_button = BackingButton(game.screen, "Voltar", 18*SQUARE_WIDTH, 11*SQUARE_HEIGHT)

    running = True
    while running:
        game.screen.fill(BLACK)
        game.screen.blit(character.scenario, character.scenario_rect.topleft)

        character.walk()
        character.draw(game.screen)

        for button in doors:
            button.check_collision(pygame.Rect(character.xpos, character.ypos, character.width, character.height))

        for button in doors:
            button.draw(game.screen)

        back_button.draw(game.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = back_button.check_click(event, running)

                for button in doors:
                    if button.visible and button.rect.collidepoint(event.pos):
                        button.click()

        pygame.display.flip()

    