import pygame
import moviepy.editor as mp
import sys
from constants import *
import numpy as np

class Game:
    def __init__(self):
        self.title = "KILL THAT STAR"
        self.current_phase = 1
        self.screen = pygame.display.set_mode((WIDTH_MAX, HEIGHT_MAX))
        self.caption = "Elemental Fusion Game"
        self.video = "assets/videos/video_opening.mp4"
        self.music = "assets/audio/audio_opening.mp3"
        self.story_text = "assets/texts/story_level_1.txt"
        self.story_image = "assets/images/fundo_story_menu.png"
        self.story_music = "assets/audio/Star Wars - Main Theme.mp3"
        self.clock = pygame.time.Clock()
        self.isotopes_found = [ISOTOPES[0]]
        self.particles_found = [PARTICLES[0], PARTICLES[2]]
        self.fusions_found = []

    def update_for_level_2(self):
        self.title = "PARTICLE ACCELERATOR"
        self.current_phase = 2
        self.video = "assets/videos/video_opening_2.mp4"
        self.music = "assets/audio/audio_opening.mp3"

    def draw_title(self):
        font = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", 90)
        surface = font.render(self.title, True, WHITE)
        rect = surface.get_rect(center=(CENTER_X, 2*HEIGHT_MAX//9))
        self.screen.blit(surface, rect)
        return rect
    
    def start_media(self):
        video_clip = mp.VideoFileClip(self.video)
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(-1)
        return video_clip
    
    def stop_media(self, video_clip):
        video_clip.close()
        pygame.mixer.music.stop()
    
    @staticmethod
    def quit(game=None):
        pygame.quit()
        sys.exit()

    def updateVideoFrame(self, video_clip):
        current_time = video_clip.reader.pos / video_clip.fps
        if current_time >= video_clip.duration: 
            current_time = 0 
        frame = video_clip.get_frame(current_time)
        self.screen.blit(pygame.surfarray.make_surface(frame.swapaxes(0, 1)), (0, 0))
        self.clock.tick(video_clip.fps)

    def get_story_image(self):
        return pygame.transform.scale(pygame.image.load(self.story_image).convert(), [WIDTH_MAX, HEIGHT_MAX])
    
    def get_story_text(self):
        with open(self.story_text, "r", encoding="utf-8") as file:
            return file.read()
    
class Nucleo:
    def __init__(self): 
        self.start_nucleo()

    def start_nucleo(self):
        self.reacting = [] 
        self.pos = []
        self.angle = 0
        self.radius = 100

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
        found = []
        if self.reacting:
            self.update_position()
            self.reacting[0].draw_nucleo_ball(game.screen, *self.pos[0])
            if len(self.reacting)==2:
                self.reacting[1].draw_nucleo_ball(game.screen, *self.pos[1])
                if self.radius > 0:
                    self.radius -= 0.5
                else:
                    a = self.reacting[0].entity
                    b = self.reacting[1].entity
                    game, found = self.recursive_fusion(game, found, a, b)
                    self.start_nucleo()
        return self, game, found
                    

    def recursive_fusion(self, game, found, a, b):
        fusions = [obj for obj in FUSIONS if (obj.element_a == a and obj.element_b == b) or (obj.element_a == b and obj.element_b == a)]
        if fusions: 
            chosen_fusion = fusions[np.random.randint(0, len(fusions))]
            if chosen_fusion not in game.fusions_found:
                game.fusions_found.append(chosen_fusion.product)
                print(chosen_fusion.get_energy())
                for each in chosen_fusion.product:
                    if isinstance(each, Isotope) and each not in game.isotopes_found:
                        game.isotopes_found.append(each)
                        found.append(each)
                        #pop-up
                        if each.is_radioactive:
                            game, found = self.recursive_fusion(game, found, each, None)
                    elif isinstance(each, FundamentalParticle) and each not in game.particles_found:
                        game.particles_found.append(each)
                        found.append(each)
            else:
                print(f"Fusão já ocorreu")
        else:
            print(f"Fusão para {a.name} e algo mais não existe")
        return game, found

class Achievement:
    pass
        

