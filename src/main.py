import pygame
from constants import *
from models.game import Game

def main(game : Game):
    game.update_for_level_2()
    #Loop principal
    running = True
    while running:
        game.screen.fill(BLACK) #Limpar tela
        game.updateVideoFrame() #Atualizar video de fundo
        game.draw_title() #Escrever titulo
        game.draw_button() #Desenhar botoes
        
        #Para cada evento detectado
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                game.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.check_button(event)

        pygame.display.flip()

if __name__ == "__main__":
    main(Game())