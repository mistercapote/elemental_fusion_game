from views import *
from models.button import BackingButton

def achiev_menu(game):
    back_button = BackingButton(game.screen, "Voltar", 18*SQUARE_WIDTH, 11*SQUARE_HEIGHT)
    if game.current_phase == 1:
            iso = game.isotopes_found
    else:
        iso = game.isotopes_found + list(map(lambda x: [i for i in ISOTOPES if i.name_isotope == x][0], SUPERNOVA))

    for each in (iso):
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
                running = back_button.check_click(event, running)
        
         
        pygame.display.flip()
