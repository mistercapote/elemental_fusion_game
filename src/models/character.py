import pygame
import numpy as np
from constants import *

class Character:
    def __init__(self):
        self.color = (0, 128, 255)
        self.width = 50
        self.height = 50
        self.xpos = CENTER_X//2
        self.ypos = CENTER_Y//2
        self.speed = 1
        self.scenario = pygame.transform.scale(pygame.image.load("assets/images/acelerador_de_particulas_sprite.png").convert_alpha(), [WIDTH_MAX,HEIGHT_MAX])
        self.scenario_rect = self.scenario.get_rect(topleft=(0, 0))

    def collision(self, vector):
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
        pygame.draw.rect(screen, self.color, (self.xpos, self.ypos, self.width, self.height))
        