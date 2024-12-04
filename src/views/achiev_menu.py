from views import *
from models.button import BackingButton

def achiev_menu(game):
    back_button = BackingButton(game.screen, "Voltar", 18*SQUARE_WIDTH, 11*SQUARE_HEIGHT)
    for each in game.isotopes_found:
        for achiev in ACHIEVEMENTS: 
            achiev.add_element(each) 
                            
    running = True
    while running:
        game.screen.fill(BLACK)
        xm, ym = pygame.mouse.get_pos()
        back_button.draw(game.screen)
        write(game.screen, "Conquistas", FONT_BUTTON_HOVER, WHITE, (CENTER_X, CENTER_Y // 6))
        
        #Hover elements
        hover_achiev = None
        for achiev in ACHIEVEMENTS:
            if not hover_achiev:
                if xm > achiev.xpos and xm < achiev.xpos + ACHIE_WIDTH and ym > achiev.ypos and ym < achiev.ypos + ACHIE_HEIGHT:
                    hover_achiev = achiev
                    continue
            achiev.draw(game.screen)  
        if hover_achiev: hover_achiev.draw(game.screen, 20)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if game.table_popup: 
                #     game.table_popup[0].button.check_click(event, game, "achiev")
                # else:
                #     for achiev in ACHIEVEMENTS: 
                #         if achiev.done == True:
                #             if event.pos[0] > achiev.xpos and event.pos[0] < achiev.xpos + SQUARE_WIDTH and event.pos[1] > achiev.ypos and event.pos[1] < achiev.ypos + SQUARE_HEIGHT:
                #                 game.table_popup.append(achiev)
                running = back_button.check_click(event, running)
        
        # if game.achiev_popup: 
        #     game.table_popup[0].draw_popup(game)
         
        pygame.display.flip()
