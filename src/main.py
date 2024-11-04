import pygame
import sys
import pandas as pd
import numpy as np
import moviepy.editor as mp
from utils import draw_text
from constants import *
from views import story_menu, config_menu, start_menu, table_menu

def iniciar():
    video_clip = mp.VideoFileClip("assets/videos/video_opening.mp4")
    pygame.mixer.music.load("assets/audio/audio_opening.mp3")
    pygame.mixer.music.play(-1)
    return video_clip

#Initialization
pygame.init()
pygame.mixer.init() 
screen = pygame.display.set_mode((WIDTH_MAX, HEIGHT_MAX))
pygame.display.set_caption("Kill that star!")
clock = pygame.time.Clock()
video_clip = iniciar()

#Loop 
running = True
while running:
    #Define buttons
    play_button = draw_text(screen, "Start", CENTER_X, CENTER_Y - 70)
    story_button = draw_text(screen, "Story", CENTER_X, CENTER_Y)
    table_button = draw_text(screen, "Periodic Table", CENTER_X, CENTER_Y + 70)
    config_button = draw_text(screen, "Settings", CENTER_X, CENTER_Y + 140)
    exit_button = draw_text(screen, "Exit", CENTER_X, CENTER_Y + 210)
    
    #Clean display
    screen.fill(BLACK)

    #Update videoframe
    current_time = video_clip.reader.pos / video_clip.fps
    if current_time >= video_clip.duration: current_time = 0 
    frame = video_clip.get_frame(current_time)
    screen.blit(pygame.surfarray.make_surface(frame.swapaxes(0, 1)), (0, 0))
    clock.tick(video_clip.fps)

    #Title
    draw_text(screen, "KILL THAT STAR", CENTER_X, 160, 100)
    
    #Get mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            video_clip.close()
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos):
                pygame.mixer.music.stop()
                video_clip.close()
                start_menu.start_menu(screen)
                video_clip = iniciar()
            elif story_button.collidepoint(event.pos):
                pygame.mixer.music.stop()
                video_clip.close()
                story_menu.story_menu(screen)
                video_clip = iniciar()
            elif table_button.collidepoint(event.pos):
                pygame.mixer.music.stop()
                video_clip.close()
                table_menu.table_menu(screen)
                video_clip = iniciar()
            elif config_button.collidepoint(event.pos):
                pygame.mixer.music.stop()
                video_clip.close()
                config_menu.config_menu(screen)
                video_clip = iniciar()
            elif exit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    #Hover effect
    if play_button.collidepoint(pygame.mouse.get_pos()):
        play_button = draw_text(screen, "Start", CENTER_X, CENTER_Y - 70, 50, GRAY)
    else:
        play_button = draw_text(screen, "Start", CENTER_X, CENTER_Y - 70)
    if story_button.collidepoint(pygame.mouse.get_pos()):
        story_button = draw_text(screen, "Story", CENTER_X, CENTER_Y, 50, GRAY)
    else:
        story_button = draw_text(screen, "Story", CENTER_X, CENTER_Y)
    if table_button.collidepoint(pygame.mouse.get_pos()):
        table_button = draw_text(screen, "Periodic Table", CENTER_X, CENTER_Y + 70, 50, GRAY)
    else:
        table_button = draw_text(screen, "Periodic Table", CENTER_X, CENTER_Y + 70)
    if config_button.collidepoint(pygame.mouse.get_pos()):
        config_button = draw_text(screen, "Settings", CENTER_X, CENTER_Y + 140, 50, GRAY)
    else:
        config_button = draw_text(screen, "Settings", CENTER_X, CENTER_Y + 140)
    if exit_button.collidepoint(pygame.mouse.get_pos()):
        exit_button = draw_text(screen, "Exit", CENTER_X, CENTER_Y + 210, 50, GRAY)
    else:
        exit_button = draw_text(screen, "Exit", CENTER_X, CENTER_Y + 210)
    
    pygame.display.flip()





