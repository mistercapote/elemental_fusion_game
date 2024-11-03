from views import *
from models.element import Element
import math

WIDTH_MAX = 1280
HEIGHT_MAX = 720

CENTER_X = WIDTH_MAX // 2
CENTER_Y = HEIGHT_MAX // 2

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

def table_menu(screen):
    ROWS = 12  # Número de linhas na matriz
    COLS = 20  # Número de colunas na matriz
    SQUARE_WIDTH = WIDTH_MAX // COLS 
    SQUARE_HEIGHT = HEIGHT_MAX // ROWS

    # Elementos
    elements = Element.load_elements_from_json("data/json/element.json")
    box = []
    
    # Loop principal
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Preenche o fundo com branco
        screen.fill(BLACK)

        for element in elements:
            if element.group == None or element.atomic_number == 57 or element.atomic_number == 89:
                if element.period == 6: center_x = int(element.atomic_number-53 + 1/2) * SQUARE_WIDTH
                elif element.period == 7: center_x = int(element.atomic_number-85 + 1/2) * SQUARE_WIDTH
                center_y = int(element.period + 3 + 1/2) * SQUARE_HEIGHT
                box.append([element, element.draw_element(screen, center_x, center_y)])
            else:
                center_x = int(element.group + 1/2) * SQUARE_WIDTH
                center_y = int(element.period + 1/2) * SQUARE_HEIGHT
                box.append([element, element.draw_element(screen, center_x, center_y)])


        for [each, button] in box:
            if button.collidepoint(pygame.mouse.get_pos()):
                button = each.draw_element(screen, button.centerx, button.centery, 30)
            else:
                button = each.draw_element(screen, button.centerx, button.centery)
    

        # Atualiza a tela
        pygame.display.flip()
