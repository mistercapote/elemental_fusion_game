from views import *
from models.element import Element
import math

def table_menu(screen):
    box = []
    
    for element in ELEMENTS:
        if element.group == None or element.atomic_number == 57 or element.atomic_number == 89:
            if element.period == 6: left_x = int(element.atomic_number-53) * SQUARE_WIDTH
            elif element.period == 7: left_x = int(element.atomic_number-85) * SQUARE_WIDTH
            top_y = int(element.period + 3) * SQUARE_HEIGHT
        else:
            left_x = int(element.group) * SQUARE_WIDTH
            top_y = int(element.period) * SQUARE_HEIGHT
        element.draw_card(screen, left_x, top_y)
        box.append({
            "element": element,
            "x": left_x,
            "y": top_y,
            })

    # Loop principal
    running = True
    while running:
        # Preenche o fundo com branco
        screen.fill(BLACK)
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #Hover
        hover_card = None
        for card in box:
            xc, yc = card["x"], card["y"]
            xm, ym = mouse
            if xm > xc and xm < xc + SQUARE_WIDTH and ym > yc and ym < yc + SQUARE_HEIGHT:
                hover_card = card
            else:
                card["element"].draw_card(screen, card["x"], card["y"])
            if hover_card:
                hover_card["element"].draw_card(screen, hover_card["x"], hover_card["y"], -10)
            
        # Atualiza a tela
        pygame.display.flip()
