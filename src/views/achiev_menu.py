from views import *
from models.button import BackingButton

def achiev_menu(game):
    back_button = BackingButton(game.screen, "Back", 18*SQUARE_WIDTH, 11*SQUARE_HEIGHT)
        
    running = True
    while running:
        game.screen.fill(BLACK)
        xm, ym = pygame.mouse.get_pos()
        back_button.draw(game.screen)
        write(game.screen, "Conquistas", FONT_BUTTON_HOVER, WHITE, (CENTER_X, CENTER_Y // 10))
        
        #Hover elements
        hover_card = None
        for card in ACHIEVEMENT:
            if not hover_card:
                if xm > card.xpos and xm < card.xpos + SQUARE_WIDTH and ym > card.ypos and ym < card.ypos + SQUARE_HEIGHT:
                    hover_card = card
                    continue
            card.draw_card(game.screen)  
        if hover_card: hover_card.draw_card(game.screen, -10)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.table_popup: 
                    game.table_popup[0].button.check_click(event, game, "table")
                else:
                    for card in table: 
                        if isinstance(card.entity, Element):
                            if event.pos[0] > card.xpos and event.pos[0] < card.xpos + SQUARE_WIDTH and event.pos[1] > card.ypos and event.pos[1] < card.ypos + SQUARE_HEIGHT:
                                game.table_popup.append(card)
                running = back_button.check_click(event, running)
        
        if game.table_popup: 
            game.table_popup[0].draw_popup(game)
         
        pygame.display.flip()