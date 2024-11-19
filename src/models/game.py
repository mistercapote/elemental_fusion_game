import pygame
import moviepy.editor as mp
import sys
from constants import *
from models.card import Card

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
        self.start_popup = []
        self.table_popup = []
        self.start_media()
        
    def update_for_level_2(self):
        self.title = "PARTICLE ACCELERATOR"
        self.current_phase = 2
        self.video = "assets/videos/video_opening_2.mp4"
        self.music = "assets/audio/audio_opening.mp3"
        self.start_media()

    def draw_title(self):
        write(self.screen, self.title, FONT_GIGANT, WHITE, (CENTER_X, 2*HEIGHT_MAX//9))
    
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

    def start_story(self):
        with open(self.story_text, "r", encoding="utf-8") as file: 
            lines =  file.read().splitlines()
        image = pygame.transform.scale(pygame.image.load(self.story_image).convert(), [WIDTH_MAX, HEIGHT_MAX])
        pygame.mixer.music.load(self.story_music)
        pygame.mixer.music.play(-1)
        return lines, image
    
    def start_table(self):
        table = []
        for element in ELEMENTS:
            if element.group == None or element.atomic_number == 57 or element.atomic_number == 89:
                if element.period == 6: left_x = int(element.atomic_number-53) * SQUARE_WIDTH
                elif element.period == 7: left_x = int(element.atomic_number-85) * SQUARE_WIDTH
                top_y = int(element.period + 3) * SQUARE_HEIGHT
            else:
                left_x = int(element.group) * SQUARE_WIDTH
                top_y = int(element.period) * SQUARE_HEIGHT
            if list(filter(lambda x: x.atomic_number == element.atomic_number, self.isotopes_found)):
                card = Card(element, left_x, top_y)
            else:
                card = Card(None, left_x, top_y)
            table.append(card)
        return table


    