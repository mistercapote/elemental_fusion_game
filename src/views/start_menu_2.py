import pygame
import sys
from views import *

def start_menu(screen):

    screen_width, screen_height = screen.get_size()

    #personagem provisório
    player_color = (0, 128, 255)
    player_width, player_height = 50, 50
    player_x = screen_width // 2
    player_y = screen_height // 2
    player_speed = 5


    running = True
    while running:
        back_button = draw_text(screen, "Back", 18*SQUARE_WIDTH, 11*SQUARE_HEIGHT)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        # Movimento pelos botões do teclado
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  #esquerda
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:  #direita
            player_x += player_speed
        if keys[pygame.K_UP]:  #cima
            player_y -= player_speed
        if keys[pygame.K_DOWN]: #baixo
            player_y += player_speed

        # impede que o personagem saia da tela
        if player_x < 0:
            player_x = 0
        if player_x > screen_width - player_width:
            player_x = screen_width - player_width
        if player_y < 0:
            player_y = 0
        if player_y > screen_height - player_height:
            player_y = screen_height - player_height

        
        screen.fill((0, 0, 0))  # Limpa a tela
        pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height)) #desenha o personagem
        pygame.display.flip()  #atualiza a tela

        
        pygame.time.Clock().tick(30)
