import pygame
import moviepy.editor as mp
import sys
from constants import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init() 
        self.title = "KILL THAT STAR"
        self.current_phase = 1
        self.screen = pygame.display.set_mode((WIDTH_MAX, HEIGHT_MAX))
        self.caption = pygame.display.set_caption("Elemental Fusion Game")
        self.video = "assets/videos/video_opening.mp4"
        self.music = "assets/audio/audio_opening.mp3"
        self.story_text = "assets/texts/story_level_1.txt"
        self.story_image = "assets/images/fundo_story_menu.png"
        self.story_music = "assets/audio/Star Wars - Main Theme.mp3"
        self.clock = pygame.time.Clock()
        self.isotopes_found = [ISOTOPES[0]]
        self.particles_found = [PARTICLES[0], PARTICLES[2]]
        self.fusions_found = []
        self.new_found = []
        self.popup = []
        self.start_media()
        

    def update_for_level_2(self):
        self.title = "PARTICLE ACCELERATOR"
        self.current_phase = 2
        self.video = "assets/videos/video_opening_2.mp4"
        self.music = "assets/audio/audio_opening.mp3"
        self.start_media()

    def draw_title(self):
        surface = FONT_GIGANT.render(self.title, True, WHITE)
        rect = surface.get_rect(center=(CENTER_X, 2*HEIGHT_MAX//9))
        self.screen.blit(surface, rect)
        return rect
    
    def start_media(self):
        self.video_clip = mp.VideoFileClip(self.video)
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(-1)
    
    def stop_media(self):
        self.video_clip.close()
        pygame.mixer.music.stop()
    
    @staticmethod
    def quit(game=None):
        pygame.quit()
        sys.exit()

    def updateVideoFrame(self):
        current_time = self.video_clip.reader.pos / self.video_clip.fps
        if current_time >= self.video_clip.duration: 
            current_time = 0 
        frame = self.video_clip.get_frame(current_time)
        self.screen.blit(pygame.surfarray.make_surface(frame.swapaxes(0, 1)), (0, 0))
        self.clock.tick(self.video_clip.fps)

    def get_story_image(self):
        return pygame.transform.scale(pygame.image.load(self.story_image).convert(), [WIDTH_MAX, HEIGHT_MAX])
    
    def get_story_text(self):
        with open(self.story_text, "r", encoding="utf-8") as file:
            return file.read()
    