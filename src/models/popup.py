import pygame
from constants import *
from models.button import PopUpButton
from models.card import Card

class PopUp:
    """
    Classe responsável pela criação e controle dos pop-ups no jogo.
    """
    def __init__(self, fusion, game):
        """
        Inicializa a instância do pop-up.

        Parâmetros:
        -----------
        fusion : Fusion
            A fusão associada ao pop-up, representando a reação que gerou o novo isótopo.
        
        game : Game
            A instância do jogo, necessária para acessar informações como a tela e os botões.
        """
        self.fusion = fusion
        self.button = PopUpButton(game.screen, "OK", CENTER_X+150, CENTER_Y+120)

    def __eq__(self, other):
        """
        Compara a instância atual com outra instância de PopUp.

        Parâmetros:
        -----------
        other : PopUp
            Outra instância da classe PopUp para comparação.

        Retorna:
        --------
        bool
            Retorna True se as fusões forem iguais, False caso contrário.
        """
        if not isinstance(other, PopUp): return False
        return self.fusion == other.fusion
    
    def draw(self, screen):
        """
        Desenha o pop-up na tela do jogo.

        Parâmetros:
        -----------
        screen : pygame.Surface
            A superfície do jogo onde o pop-up será desenhado.
        """
        pygame.draw.rect(screen, BLACK, (CENTER_X-200, CENTER_Y-150, 400, 300))
        pygame.draw.rect(screen, WHITE, (CENTER_X-200, CENTER_Y-150, 400, 300), 5)
        write(screen,"Novo isótopo descoberto!",  FONT_LARGE, WHITE, (CENTER_X,CENTER_Y-100))
        #lembrar de variar a mensagem

        hover_card = None
        i  = -len(self.fusion.product) * (SQUARE_WIDTH+5) // 2
        for card in self.fusion.product:
            card = Card(card, CENTER_X+i, CENTER_Y-60)
            i += SQUARE_WIDTH+5
            if not hover_card:
                xm, ym = pygame.mouse.get_pos()
                if xm > card.xpos and xm < card.xpos + SQUARE_WIDTH and ym > card.ypos and ym < card.ypos + SQUARE_HEIGHT:
                    hover_card = card
                    continue
            card.draw_card(screen)
        if hover_card: hover_card.draw_card(screen, -10)
        
        write(screen, f"{self.fusion.get_energy()}", FONT_LARGE, WHITE, (CENTER_X,CENTER_Y+55))
        write(screen, "Mensagem sobre esta reação", FONT_LARGE, WHITE, (CENTER_X,CENTER_Y+75))
        self.button.draw(screen)

