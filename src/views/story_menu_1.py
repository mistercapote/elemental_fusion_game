from views import *

def story_menu(screen):
    running = True
    while running:
        back_button = draw_text(screen, "Back", 18*SQUARE_WIDTH, 11*SQUARE_HEIGHT)
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False 
        if back_button.collidepoint(pygame.mouse.get_pos()):
            back_button = draw_text(screen, "Back", 18*SQUARE_WIDTH, 11*SQUARE_HEIGHT, 50, GRAY)
        else:
            back_button = draw_text(screen, "Back", 18*SQUARE_WIDTH, 11*SQUARE_HEIGHT)
    
        pygame.display.flip()