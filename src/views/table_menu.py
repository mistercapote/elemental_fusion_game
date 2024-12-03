from views import *
from models.card import Card
from models.button import BackingButton

def table_menu(game):
    """
    Função responsável pela exibição do menu da tabela periódica no jogo.

    Esta função desenha a tabela periódica, permitindo ao jogador interagir com os elementos da tabela.
    O jogador pode clicar nos elementos da tabela para visualizar suas informações e acessar mais detalhes.
    A função também exibe um botão de "voltar" para retornar ao menu anterior.

    Parâmetros:
    -----------
    game : Game
        O objeto do jogo, contendo todas as informações e estados necessários para renderizar o menu e interagir com o jogador.
        
    Retorna:
    --------
    Não retorna nenhum valor.
    """
    table = game.start_table()
    back_button = BackingButton(game.screen, "Back", 2*SQUARE_WIDTH, 11*SQUARE_HEIGHT)
    running = True
    while running:
        xm, ym = pygame.mouse.get_pos()
        game.screen.fill(BLACK)
        back_button.draw(game.screen)
        
        #Hover elements
        hover_card = None
        for card in table:
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
