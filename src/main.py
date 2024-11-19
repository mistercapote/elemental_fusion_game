import pygame
from constants import *
from models.button import OpeningButton
from models.game import Game
from views import start_menu_1, start_menu_2, story_menu, table_menu, settings_menu

#Inicialização
game = Game()
game.update_for_level_2()

#Definindo os botões da tela inicial
if game.current_phase == 1: start_button = OpeningButton(game.screen, "Start", CENTER_X, CENTER_Y - 70, start_menu_1.start_menu)
else: start_button = OpeningButton(game.screen, "Start", CENTER_X, CENTER_Y - 70, start_menu_2.start_menu)
story_button = OpeningButton(game.screen, "Story", CENTER_X, CENTER_Y, story_menu.story_menu)
table_button = OpeningButton(game.screen, "Periodic Table", CENTER_X, CENTER_Y + 70, table_menu.table_menu)
settings_button = OpeningButton(game.screen, "Settings", CENTER_X, CENTER_Y + 140, settings_menu.settings_menu)
exit_button = OpeningButton(game.screen, "Exit", CENTER_X, CENTER_Y + 210, game.quit)

#Loop princial
running = True
while running:
    game.screen.fill(BLACK) #Limpar tela
    game.updateVideoFrame() #Atualizar video de fundo
    game.draw_title() #Escrever titulo

    #Para cada evento detectado
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            game.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Ao clicar em cada botão
            start_button.check_click(event, game)
            story_button.check_click(event, game)
            table_button.check_click(event, game)
            settings_button.check_click(event, game)
            exit_button.check_click(event, game)

    #Hover effect
    start_button.draw(game.screen)
    story_button.draw(game.screen)
    table_button.draw(game.screen)
    settings_button.draw(game.screen)
    exit_button.draw(game.screen)

    pygame.display.flip()