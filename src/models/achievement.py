import pygame
from constants import *
from models.fusion import Element

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
        self.numbers = set(numbers)
        self.unlocked_elements = set()
        self.done = False
        self.description = description
        self.xpos = (xpos - 0.5) * ACHIE_WIDTH
        self.ypos = (ypos - 0.5)  * ACHIE_HEIGHT
        self.color = color
    
    def unlocked(self):
        if self.numbers == self.unlocked_elements:
            self.done = True

    def add_element(self, element : Element):
        if element.atomic_number in self.numbers:
            self.unlocked_elements.add(element.atomic_number)
            self.unlocked()
    
    def draw(self, screen, coef=-1):
        if not self.done:
            name_text = f"{len(self.unlocked_elements)}/{len(self.numbers)}"
            pygame.draw.rect(screen, GRAY, (self.xpos - coef, self.ypos - coef, ACHIE_WIDTH + 2*coef, ACHIE_HEIGHT + 2*coef))
        else:
            name_text = self.name
            pygame.draw.rect(screen, self.color, (self.xpos - coef, self.ypos - coef, ACHIE_WIDTH + 2*coef, ACHIE_HEIGHT + 2*coef)) 
        
        write(screen, name_text, FONT_LARGE, BLACK, (self.xpos+ACHIE_WIDTH//2, self.ypos+ACHIE_HEIGHT//2))
        
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
    