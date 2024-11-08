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
        self.story_music ="assets/audio/Star Wars - Main Theme.mp3"
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
    

# class Video:
#     def __init__(self):
#         self.path = 
#         self.clip = 
#         self.fps =



class Nucleo:
    def __init__(self): 
        self.elements = []
        self.pos1 = None
        self.pos2 = None
        self.angle = 0
        self.radius = 100

    def start_nucleo(self):
        self.elements = [] 
        self.angle = 0
        self.radius = 100

    def update_position(self):
        def position(radius, angle):
            return [3*CENTER_X//2 + radius * np.cos(angle),
                    CENTER_Y + radius * np.sin(angle)
            ]
        self.pos1 = position(self.radius, self.angle)
        self.pos2 = position(self.radius, self.angle+np.pi)
        
    