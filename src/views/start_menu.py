from views import *

def start_menu(screen):
    round = True
    while round:
        screen.fill(BLACK)
        draw_text(screen, "Jogo em execução...", 250, 250)
        
        # Botão para voltar ao menu
        back_button = draw_text(screen, "Back", 350, 450)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    round = False  # Volta ao menu principal
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                round = False  # ESC também volta ao menu principal

        pygame.display.flip()