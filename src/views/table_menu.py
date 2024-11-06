from views import *
from models.draw import Card
import time

def start_box(isotopes_found):
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
            card = Card(element, left_x, top_y)
        else:
            card = Card(None, left_x, top_y)
        box.append(card)
    return box


def table_menu(screen, isotopes_found):
    box = start_box(isotopes_found)
    # a, b = 1, 1
    running = True
    while running:
        # print(b-a)
        # a = time.time()
        back_button = draw_text(screen, "Back", 2*SQUARE_WIDTH, 11*SQUARE_HEIGHT)
        xm, ym = pygame.mouse.get_pos()
        screen.fill(BLACK)
        
        #Hover
        hover_card = None
        for card in box:
            if not hover_card:
                if xm > card.xpos and xm < card.xpos + SQUARE_WIDTH and ym > card.ypos and ym < card.ypos + SQUARE_HEIGHT:
                    hover_card = card
                    continue
            if card != hover_card:
                card.draw_card(screen)
        
        if hover_card:
            hover_card.draw_card(screen, -10)
        
        if back_button.collidepoint(pygame.mouse.get_pos()):
            back_button = draw_text(screen, "Back", 2*SQUARE_WIDTH, 11*SQUARE_HEIGHT, 50, GRAY)
        else:
            back_button = draw_text(screen, "Back", 2*SQUARE_WIDTH, 11*SQUARE_HEIGHT)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False 
        # b = time.time()
        pygame.display.flip()

