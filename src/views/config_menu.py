from views import *

def config_menu(screen):
    round = True
    while round:
        screen.fill(BLACK)
        draw_text(screen, "Config", 60, 250, 100)
        
        # Botão para voltar ao menu
        botao_voltar = draw_text(screen, "Back", 350, 450)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(event.pos):
                    round = False  # Volta ao menu principal
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                round = False  # ESC também volta ao menu principal

        pygame.display.flip()