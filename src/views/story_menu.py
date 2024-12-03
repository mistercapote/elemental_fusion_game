import pygame
from constants import *
from models.button import BackingButton

def story_menu(game):
    """
    Exibe o menu de história do jogo.

    Parâmetros:
    -----------
    game : Game
        Objeto principal do jogo que gerencia o estado e as ações do jogo.

    Descrição:
    -----------
    Essa função exibe a introdução ou história inicial do jogo. A tela é preenchida com uma imagem de fundo e as linhas de texto são desenhadas uma a uma, movendo-se de baixo para cima. O usuário pode avançar para a tela principal clicando no botão "Back". 
    Caso o texto tenha terminado de subir, o menu retorna automaticamente para a tela principal.

    O botão "Back" permite ao usuário sair do menu e retornar à tela anterior. Ao clicar no botão ou ao terminar a animação de texto, o menu é fechado e o jogo volta ao estado anterior.
    """
    lines, image = game.start_story()
    back_button = BackingButton(game.screen, "Back", 80, 50)
    ypos = HEIGHT_MAX
    size = 35
    speed = 0.15

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
        