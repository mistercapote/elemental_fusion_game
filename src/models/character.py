import pygame
import numpy as np
from constants import *

class Character:
    """
    Representa o personagem que se move dentro do cenário do jogo.
    O personagem é controlado pelo jogador e pode se mover de acordo com as teclas de direção.
    
    Atributos:
    ----------
    color : tuple
        Cor do personagem (azul por padrão).
    width : int
        Largura do personagem.
    height : int
        Altura do personagem.
    xpos : int
        Posição X do personagem no cenário.
    ypos : int
        Posição Y do personagem no cenário.
    speed : int
        Velocidade de movimento do personagem.
    scenario : pygame.Surface
        Imagem do cenário onde o personagem se move, escalada para o tamanho da tela.
    scenario_rect : pygame.Rect
        Retângulo que define a área de colisão do cenário.

    Métodos:
    --------
    collision : Verifica se o personagem colide com o cenário.
    walk : Controla o movimento do personagem de acordo com as teclas pressionadas.
    draw : Desenha o personagem na tela.
    """
    def __init__(self):
        """
        Inicializa um novo personagem com atributos padrão, como cor, tamanho, 
        posição inicial e velocidade. Carrega também a imagem do cenário.
        """
        self.color = (0, 128, 255)
        self.width = 50
        self.height = 50
        self.xpos = CENTER_X//2
        self.ypos = CENTER_Y//2
        self.speed = 1
        self.scenario = pygame.transform.scale(pygame.image.load("assets/images/acelerador_de_particulas_sprite.png").convert_alpha(), [WIDTH_MAX,HEIGHT_MAX])
        self.scenario_rect = self.scenario.get_rect(topleft=(0, 0))

    def collision(self, vector):
        """
        Verifica se o personagem colide com o cenário.

        Parâmetros:
        -----------
        vector : list
            O vetor de movimento, representando a direção desejada.

        Retorna:
        --------
        bool
            Retorna `True` se houver colisão com o cenário, caso contrário, retorna `False`.
        
        Ação:
        ------
        Verifica os cantos do personagem na nova posição para detectar colisões com cores específicas do cenário.
        """
        for corner in [(vector[0], vector[1]), 
                       (vector[0] + self.width - 1, vector[1]),  
                       (vector[0], vector[1] + self.height - 1), 
                       (vector[0] + self.width - 1, vector[1] + self.height - 1)
            ]:

            if self.scenario_rect.collidepoint(corner):
                relative_x = int(corner[0] - self.scenario_rect.x)
                relative_y = int(corner[1] - self.scenario_rect.y)
                pixel_color = self.scenario.get_at((relative_x, relative_y))[:3]  # Ignorar o canal alfa
                if pixel_color in [(210, 211, 213), (169, 171, 174), (139, 140, 143), (96, 96, 98)]:
                    return True
        return False
    
    def walk(self):
        """
        Controla o movimento do personagem de acordo com as teclas pressionadas.

        Ação:
        ------
        Verifica as teclas pressionadas (setas ou W, A, S, D) para atualizar a posição do personagem.
        Se houver movimento, normaliza o vetor de direção e atualiza a posição, garantindo que o personagem 
        não saia da tela. Verifica também se há colisões antes de mover o personagem.
        """
        #Capturar sentido do movimento
        keys = pygame.key.get_pressed()
        vector = np.array([0, 0])
        if keys[pygame.K_LEFT]: vector[0] -= 1
        if keys[pygame.K_RIGHT]: vector[0] += 1
        if keys[pygame.K_UP]: vector[1] -= 1
        if keys[pygame.K_DOWN]: vector[1] += 1

        # Normalizar o vetor, se houver movimento
        norma = np.linalg.norm(vector)
        if norma > 0: vector = (vector / norma) * self.speed

        # Atualizar posição, impedindo que saia da tela
        vector[0] = min(max(self.xpos + vector[0], 0), WIDTH_MAX - self.width)
        vector[1] = min(max(self.ypos + vector[1], 0), HEIGHT_MAX - self.height)

        # Se não houve colisão, mova o personagem
        if not self.collision(vector):
            self.xpos, self.ypos = int(vector[0]), int(vector[1])

    def draw(self, screen):
        """
        Desenha o personagem na tela.

        Parâmetros:
        -----------
        screen : pygame.Surface
            A superfície (tela) onde o personagem será desenhado.

        Ação:
        ------
        Desenha um retângulo representando o personagem na tela, na posição atual.
        """
        pygame.draw.rect(screen, self.color, (self.xpos, self.ypos, self.width, self.height))
        