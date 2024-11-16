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
        surface = FONT_GIGANT.render(self.title, True, WHITE)
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
            self.reacting[0].draw(game.screen, *self.pos[0])
            if len(self.reacting)==2:
                self.reacting[1].draw(game.screen, *self.pos[1])
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
    def __init__(self):
        self.gasnobre = [2, 10, 18, 36, 54, 86, 118]
        self.metalalcalino = [3, 11, 19, 37, 55, 87]
        self.metalalcalinoterroso = [4, 12, 20, 38, 56, 88]
        self.metaltransicaoexterna = [21, 22, 23, 24,25,26, 27, 28, 29, 30,
                                      39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
                                      72, 73, 74, 75, 76, 77, 78, 79, 80,
                                      104, 105, 106, 107, 108, 109, 110, 111, 112]
        self.metalpostransicao = [13, 31, 49, 50, 81, 82,83, 84, 85, 113, 114, 115, 116, 117]
        self.metaltransicaointerna = [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,
                                      89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103]
        self.semimetal = [5, 14, 32, 33, 51, 52]
        self.ametal = [6, 7, 8, 9, 15, 16, 17, 34, 35, 53]
        self.conquistas = []
        #self.possíveis_conquistas = ["Gases nobres", "Metais alcalinos", "Metais alcalino terrosos", "Metais de transição externa", "Metais pós-transição", "Metais de transição interna", "Semimetais", "Ametais"]


    def family_list(self, game : Game):
        conquista_atual = None

        for each in game.isotopes_found:
            if each.atomic_number in self.gasnobre:
                self.gasnobre.remove(each.atomic_number)
                if not self.gasnobre:
                    conquista_atual = "Gases nobres"
                    self.conquistas.append("Gases nobres")
            elif each.atomic_number in self.metalalcalino:
                self.metalalcalino.remove(each.atomic_number)
                if not self.metalalcalino:
                    conquista_atual = "Metais alcalinos"
                    self.conquistas.append("Metais alcalinos")
            elif each.atomic_number in self.metalalcalinoterroso:
                self.metalalcalinoterroso.remove(each.atomic_number)
                if not self.metalalcalinoterroso:
                    conquista_atual = "Metais alcalino terrosos"
                    self.conquistas.append("Metais alcalino terrosos")
            elif each.atomic_number in self.metaltransicaoexterna:
                self.metaltransicaoexterna.remove(each.atomic_number)
                if not self.metaltransicaoexterna:
                    conquista_atual = "Metais de transição externa"
                    self.conquistas.append("Metais de transição externa")
            elif each.atomic_number in self.metalpostransicao:
                self.metalpostransicao.remove(each.atomic_number)
                if not self.metalpostransicao:
                    conquista_atual = "Metais pós-transição"
                    self.conquistas.append("Metais pós-transição")
            elif each.atomic_number in self.metaltransicaointerna:
                self.metaltransicaointerna.remove(each.atomic_number)
                if not self.metaltransicaointerna:
                    conquista_atual = "Metais de transição interna"
                    self.conquistas.append("Metais de transição interna")
            elif each.atomic_number in self.semimetal:
                self.semimetal.remove(each.atomic_number)
                if not self.semimetal:
                    conquista_atual = "Semimetais"
                    self.conquistas.append("Semimetais")
            elif each.atomic_number in self.ametal:
                self.ametal.remove(each.atomic_number)
                if not self.ametal:
                    conquista_atual = "Ametais"
                    self.conquistas.append("Ametais")

        return conquista_atual, self.conquistas
    
    def recently_achievement(self):
         conquista_atual, _ = self.family_list()

         return f"Parabens! Você desbloqueou todos os {conquista_atual}"
    
    def list_achievements(self):
        _, self.conquistas = self.family_list()
        historico = []

        if "Gases nobres" in self.conquistas:
            historico.append("Gases Nobres: Elementos estáveis e pouco reativos com configuração eletrônica completa.")

        if "Metais alcalinos" in self.conquistas:
            historico.append("Metais Alcalinos: Metais altamente reativos encontrados no grupo 1 da tabela periódica.")

        if "Metais alcalino terrosos" in self.conquistas:
            historico.append("Metais Alcalino-Terrosos: Metais do grupo 2, menos reativos que os alcalinos, usados em ligas e reações químicas.")

        if "Metais de transição externa" in self.conquistas:
            historico.append("Metais de Transição Externa: Metais do bloco d com alta condutividade e diversas propriedades químicas.")

        if "Metais pós-transição" in self.conquistas:
            historico.append("Metais Pós-Transição: Metais macios com baixa reatividade encontrados abaixo dos metais de transição.")

        if "Metais de transição interna" in self.conquistas:
            historico.append("Metais de Transição Interna: Elementos das séries dos lantanídeos e actinídeos, com orbitais f parcialmente preenchidos.")

        if "Semimetais" in self.conquistas:
            historico.append("Semimetais: Elementos com propriedades intermediárias entre metais e não metais.")

        if "Ametais" in self.conquistas:
            historico.append("Ametais: Elementos não metálicos com tendência a ganhar elétrons e formar compostos covalentes.")

        return historico
    