import pygame
from constants import *
import numpy as np

class Nucleo:
    def __init__(self): 
        self.canal1 = pygame.mixer.Channel(1)
        self.canal2 = pygame.mixer.Channel(2)
        self.start_nucleo()
        self.explosion = [pygame.image.load(f"assets/images/explosion/PNG/Circle_explosion/Circle_explosion{i}.png") for i in range(1, 11)]

    def start_nucleo(self):
        self.reacting = [] 
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
    
    def controler(self, game):
        game.new_found = []
        if self.reacting:
            self.update_position()
            self.reacting[0].draw(game.screen, *self.pos[0])
            if len(self.reacting)==2:
                self.reacting[1].draw(game.screen, *self.pos[1])
                if self.radius > 5:
                    if not self.canal1.get_busy():
                        self.canal1.play(pygame.mixer.Sound("assets/audio/pierre_roud.mp3"))
                    self.radius -= 0.3
                elif self.radius > 0:
                    self.canal1.stop()
                    if not self.canal2.get_busy():
                        self.canal2.play(pygame.mixer.Sound("assets/audio/fusion.mp3"))
                    img = self.explosion[self.frame // 15]
                    game.screen.blit(img, (3*CENTER_X//2 - img.get_width() // 2, CENTER_Y - img.get_height() // 2))
                    self.frame += 1
                    if self.frame == 150:
                        self.radius = 0
                else:
                    self.canal2.stop()
                    a = self.reacting[0].entity
                    b = self.reacting[1].entity
                    game = self.recursive_fusion(game, a, b)
                    self.start_nucleo()
        return self, game
                    

    def recursive_fusion(self, game, a, b):
        fusions = [obj for obj in FUSIONS if (obj.element_a == a and obj.element_b == b) or (obj.element_a == b and obj.element_b == a)]
        if fusions: 
            done = 0
            for chosen_fusion in fusions:
                if chosen_fusion in game.fusions_found:
                    done +=1
                    continue
                else:
                    game.fusions_found.append(chosen_fusion.product)
                    game.popup.append(chosen_fusion)
                    print(chosen_fusion.get_energy())
                    for each in chosen_fusion.product:
                        if isinstance(each, Isotope) and each not in game.isotopes_found:
                            game.isotopes_found.append(each)
                            game.new_found.append(each)
                            if each.is_radioactive:
                                game = self.recursive_fusion(game, each, None)
                        elif isinstance(each, FundamentalParticle) and each not in game.particles_found:
                            game.particles_found.append(each)
                            game.new_found.append(each)
                    break
            if done == len(fusions):
                print("Fusao já ocorreu")
        else:
            print(f"Fusão para {a.name} e algo mais não existe")
        return game
