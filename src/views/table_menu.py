from views import *
from models.element import Element
import math

def table_menu(screen):
    

    # Elementos
    
    box = []
    
    # Loop principal
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Preenche o fundo com branco
        screen.fill(BLACK)
        mouse = pygame.mouse.get_pos()

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

        def is_hovered(card, mouse):
            
            return 
            
        # Desenhar círculos e aplicar o efeito de hover
        for card in box:
            xc, yc = card["x"], card["y"]
            xm, ym = mouse
            if xm > xc and xm < xc + SQUARE_WIDTH and ym > yc and ym < yc + SQUARE_HEIGHT:
                card["element"].draw_card(screen, card["x"], card["y"], -10)
            else:
                card["element"].draw_card(screen, card["x"], card["y"])


        # Atualiza a tela
        pygame.display.flip()
