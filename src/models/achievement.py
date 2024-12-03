import pygame
from constants import *
pygame.init()
def write(screen, text, font, color, center):
    render = font.render(text, True, color)
    rect = render.get_rect(center=center)
    screen.blit(render, rect)

#Tamanhos
WIDTH_MAX = 1280
HEIGHT_MAX = 720
CENTER_X = WIDTH_MAX // 2
CENTER_Y = HEIGHT_MAX // 2
SQUARE_WIDTH = WIDTH_MAX // 20
SQUARE_HEIGHT = HEIGHT_MAX // 12
ACHIE_WIDTH = WIDTH_MAX // 5
ACHIE_HEIGHT = HEIGHT_MAX // 3

#Cores
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

FONT_GIGANT = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", 90)
FONT_BUTTON_HOVER = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", 50)
FONT_BUTTON = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", 40)
FONT_STORY = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", 35)
FONT_LARGE = pygame.font.Font("assets/font/Roboto_Slab/static/RobotoSlab-Regular.ttf", 20)
FONT_SMALL= pygame.font.Font("assets/font/Roboto_Slab/static/RobotoSlab-Regular.ttf", 12)

class Achievement:
    def __init__(self, name, numbers, description, xpos, ypos, color):
        self.name = name
        self.numbers = numbers
        self.done = True
        self.description = description
        self.xpos = (xpos - 0.5) * ACHIE_WIDTH
        self.ypos = (ypos - 0.5)  * ACHIE_HEIGHT
        self.color = color
    
    def family_list(self, game):
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
    
    def draw(self):
        _, self.conquistas = self.family_list()
        historico = []

        return historico
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name = data["name"],
            numbers = data["numbers"],
            description = data["description"],
            xpos = data["xpos"],
            ypos = data["ypos"],
            color = data["color"]
        )
    
    def draw(self, screen, coef=-1):
        if not self.done:
            name_text = ""
            pygame.draw.rect(screen, GRAY, (self.xpos - coef, self.ypos - coef, ACHIE_WIDTH + 2*coef, ACHIE_HEIGHT + 2*coef))
        else:
            name_text = self.name
            pygame.draw.rect(screen, self.color, (self.xpos - coef, self.ypos - coef, ACHIE_WIDTH + 2*coef, ACHIE_HEIGHT + 2*coef)) 
        
        write(screen, name_text, FONT_LARGE, BLACK, (self.xpos+ACHIE_WIDTH//2, self.ypos+ACHIE_HEIGHT//2))
        
    