import pygame
from constants import *
from models.draw import ButtonOpening
from models.game import Game
from views import start_menu_1, start_menu_2, story_menu_1, story_menu_2, table_menu, settings_menu

#Inicialização
pygame.init()
pygame.mixer.init() 
game = Game()
# game.update_for_level_2()
pygame.display.set_caption(game.caption)
video_clip = game.start_media()

#Definindo os botões da tela inicial
if game.current_phase == 1: start_button = ButtonOpening(game.screen, "Start", CENTER_X, CENTER_Y - 70, start_menu_1.start_menu)
else: start_button = ButtonOpening(game.screen, "Start", CENTER_X, CENTER_Y - 70, start_menu_2.start_menu)
story_button = ButtonOpening(game.screen, "Story", CENTER_X, CENTER_Y, story_menu_1.story_menu)
table_button = ButtonOpening(game.screen, "Periodic Table", CENTER_X, CENTER_Y + 70, table_menu.table_menu)
settings_button = ButtonOpening(game.screen, "Settings", CENTER_X, CENTER_Y + 140, settings_menu.settings_menu)
exit_button = ButtonOpening(game.screen, "Exit", CENTER_X, CENTER_Y + 210, game.quit)

#Loop princial
running = True
while running:
    game.screen.fill(BLACK) #Limpar tela
    game.updateVideoFrame(video_clip) #Atualizar video de fundo
    game.draw_title() #Escrever titulo

    #Para cada evento detectado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Ao clicar em cada botão
            game, video_clip = start_button.check_click(event, game, video_clip)
            _, video_clip = story_button.check_click(event, game, video_clip)
            _, video_clip = table_button.check_click(event, game, video_clip)
            _, video_clip = settings_button.check_click(event, game, video_clip)
            exit_button.check_click(event, game, video_clip)

    #Hover effect
    start_button.draw(game.screen, pygame.mouse.get_pos())
    story_button.draw(game.screen, pygame.mouse.get_pos())
    table_button.draw(game.screen, pygame.mouse.get_pos())
    settings_button.draw(game.screen, pygame.mouse.get_pos())
    exit_button.draw(game.screen, pygame.mouse.get_pos())

    pygame.display.flip()




