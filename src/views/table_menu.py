from views import *
from models.draw import Card, ButtonStarting

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


def table_menu(game):
    box = start_box(game.isotopes_found)
    back_button = ButtonStarting(game.screen, "Back", 2*SQUARE_WIDTH, 11*SQUARE_HEIGHT)

    running = True
    while running:
        xm, ym = pygame.mouse.get_pos()
        game.screen.fill(BLACK)
        
        #Hover elements
        hover_card = None
        for card in box:
            if not hover_card:
                if xm > card.xpos and xm < card.xpos + SQUARE_WIDTH and ym > card.ypos and ym < card.ypos + SQUARE_HEIGHT:
                    hover_card = card
                    continue
            card.draw_card(game.screen)  
        if hover_card: hover_card.draw_card(game.screen, -10)
        
        #Hover effect
        back_button.draw(game.screen, pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = back_button.check_click(event, running)
                
        pygame.display.flip()

