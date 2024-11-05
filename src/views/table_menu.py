from views import *
from models.element import Element
import math

def table_menu(screen, isotopes_found):
    box = []
    for element in ELEMENTS:
        if element.group == None or element.atomic_number == 57 or element.atomic_number == 89:
            if element.period == 6: left_x = int(element.atomic_number-53) * SQUARE_WIDTH
            elif element.period == 7: left_x = int(element.atomic_number-85) * SQUARE_WIDTH
            top_y = int(element.period + 3) * SQUARE_HEIGHT
        else:
            left_x = int(element.group) * SQUARE_WIDTH
            top_y = int(element.period) * SQUARE_HEIGHT
        if list(filter(lambda x: x.atomic_number == element.atomic_number, isotopes_found)):
            in_found = True
            element.draw_card(screen, left_x, top_y)
        else:
            in_found = False
            Element.draw_card(None, screen, left_x, top_y)

        box.append({
            "element": element,
            "x": left_x,
            "y": top_y,
            "in": in_found
            })

    # Loop principal
    running = True
    while running:
        # Preenche o fundo com branco
        back_button = draw_text(screen, "Back", 2*SQUARE_WIDTH, 11*SQUARE_HEIGHT)
        screen.fill(BLACK)
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False 

        #Hover
        hover_card = None
        for card in box:
            xc, yc = card["x"], card["y"]
            xm, ym = mouse
            if xm > xc and xm < xc + SQUARE_WIDTH and ym > yc and ym < yc + SQUARE_HEIGHT:
                hover_card = card
            else:
                if card["in"]: card["element"].draw_card(screen, card["x"], card["y"])
                else: Element.draw_card(None, screen, card["x"], card["y"])
            if hover_card:
                if hover_card["in"]: hover_card["element"].draw_card(screen, hover_card["x"], hover_card["y"], -10)
                else: Element.draw_card(None, screen, hover_card["x"], hover_card["y"], -10)
        
        if back_button.collidepoint(pygame.mouse.get_pos()):
            back_button = draw_text(screen, "Back", 2*SQUARE_WIDTH, 11*SQUARE_HEIGHT, 50, GRAY)
        else:
            back_button = draw_text(screen, "Back", 2*SQUARE_WIDTH, 11*SQUARE_HEIGHT)
        
        # Atualiza a tela
        pygame.display.flip()

