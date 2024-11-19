import pygame
from constants import *
import numpy as np

class Nucleo:
    def __init__(self): 
        self.canal1 = pygame.mixer.Channel(1)
        self.canal2 = pygame.mixer.Channel(2)
        self.speed = 0.01
        self.fusion_speed = -0.1
        self.not_fusion_speed = 0.07
        self.explosion_speed = 0.02
        self.image = pygame.image.load(f"assets/images/nucleo.webp").convert_alpha()
        self.explosion = [pygame.image.load(f"assets/images/explosion/PNG/Circle_explosion/Circle_explosion{i}.png").convert_alpha() for i in range(1, 11)]
        self.start_nucleo()

    def start_nucleo(self):
        self.reacting = [] 
        self.fusions = [] 
        self.pos = []
        self.angle = 0
        self.radius = 100
        self.frame = 0
        self.canal1.stop()
        self.canal2.stop()

    def reacting_lenght(self):
        return len(self.reacting)
    
    def reacting_append(self, ball):
        return self.reacting.append(ball)

    def update_position(self):
        def position(radius, angle):
            return [3*CENTER_X//2 + radius * np.cos(angle),
                    CENTER_Y + radius * np.sin(angle)
            ]
        self.pos = [position(self.radius, self.angle),
                  position(self.radius, self.angle+np.pi)
        ]

    def not_fusion(self):
        if self.reacting:
            self.start_nucleo()
            self.canal2.play(pygame.mixer.Sound("assets/audio/no_fusion.mp3"))
    
    def rotation_animation(self, screen):
        self.angle += self.speed
        self.update_position()
        self.reacting[0].draw(screen, *self.pos[0])
        if len(self.reacting)==2:
            self.reacting[1].draw(screen, *self.pos[1])
            if not self.canal1.get_busy():
                self.canal1.play(pygame.mixer.Sound("assets/audio/pierre_roud.mp3")) 
            if not self.fusions:
                self.fusions = [obj for obj in FUSIONS if (obj.element_a == self.reacting[0].entity and obj.element_b == self.reacting[1].entity) or (obj.element_a == self.reacting[1].entity and obj.element_b == self.reacting[0].entity)]
            
            if self.fusions: self.radius += self.fusion_speed # Velocidade de aproximação
            else: self.radius += self.not_fusion_speed # Velocidade de afastamento

    def explosion_animation(self, screen):
        self.canal1.stop()
        if not self.canal2.get_busy():
            self.canal2.play(pygame.mixer.Sound("assets/audio/fusion.mp3"))
        
        img = self.explosion[int(self.frame)]
        screen.blit(img, (3*CENTER_X//2 - img.get_width() // 2, CENTER_Y - img.get_height() // 2))
        self.frame += self.explosion_speed
        if self.frame >= 10: self.radius = 0
    
    def fusion(self, game):
        self.canal2.stop()
        a = self.reacting[0].entity
        b = self.reacting[1].entity
        game = self.recursive_fusion(game, a, b)
        self.start_nucleo()
        return game

    def controler(self, game):
        game.new_found = []
        if self.reacting:
            if self.radius > 220: self.not_fusion()   
            elif self.radius > 3: self.rotation_animation(game.screen)
            elif self.radius > 0: self.explosion_animation(game.screen)
            else: game = self.fusion(game)
        return self, game

    def recursive_fusion(self, game, a, b):
        if not self.fusions:
            self.fusions = [obj for obj in FUSIONS if (obj.element_a == a and obj.element_b == b) or (obj.element_a == b and obj.element_b == a)]
        
        if self.fusions: 
            done = 0
            for chosen_fusion in self.fusions:
                #corrigir a fusao com multiplos produtos
                if chosen_fusion in game.fusions_found:
                    done +=1
                else:
                    game.fusions_found.append(chosen_fusion)
                    game.popup.append(chosen_fusion)
                    print(chosen_fusion.get_energy())
                    for each in chosen_fusion.product:
                        if isinstance(each, Isotope) and each not in game.isotopes_found:
                            game.isotopes_found.append(each)
                            game.new_found.append(each)
                            if each.is_radioactive:
                                self.start_nucleo()
                                game = self.recursive_fusion(game, each, None)
                        elif isinstance(each, FundamentalParticle) and each not in game.particles_found:
                            game.particles_found.append(each)
                            game.new_found.append(each)
                    break
            if done == len(self.fusions):
                #mudar mensagem do Popup
                print("Todos os produtos dessa fusao ja foram descobertos")
        else:
            print(f"O elemento {a.name} decai, mas não sei ainda o q vira")
        return game
