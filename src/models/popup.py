import pygame
from constants import *
from models.button import PopUpButton
from models.card import Card

class PopUp:
    """
    Classe responsável pela criação e controle dos pop-ups no jogo.
    """
    def __init__(self, fusion: Fusion, game) -> None:
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
       
    def __eq__(self, other) -> bool:
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
    
    def draw(self, screen: pygame.surface) -> None:
        """
        Desenha o pop-up na tela do jogo.

        Parâmetros:
        -----------
        screen : pygame.Surface
            A superfície do jogo onde o pop-up será desenhado.
        """

        iW = 400

        if self.fusion.description:
            palavras = self.fusion.description.split(' ')  # Divide o texto em palavras
        else:
            palavras = "Descrição ainda não exite."
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            # Verifica se a linha atual, com a próxima palavra, ultrapassa a largura máxima
            if FONT_LARGE.size(linha_atual + palavra)[0] <= iW - 10:
                linha_atual += palavra + " "
            else:
                linhas.append(linha_atual.strip())
                linha_atual = palavra + " "

        if linha_atual:  # Adiciona a última linha
            linhas.append(linha_atual.strip())

        aH = 300
        iH = aH + len(linhas)*15

        self.button = PopUpButton(screen, "OK", CENTER_X+iW//2-40, CENTER_Y-iH//2 + iH-15)
        pygame.draw.rect(screen, BLACK, (CENTER_X-200, CENTER_Y-150, iW, iH))
        pygame.draw.rect(screen, WHITE, (CENTER_X-200, CENTER_Y-150, iW, iH), 5)
        write(screen,"Novo isótopo descoberto!",  FONT_LARGE, WHITE, (CENTER_X,CENTER_Y-100))
        for i, linha in enumerate(linhas):
            write(screen, linha, FONT_INFO, WHITE, (CENTER_X,CENTER_Y-iH//2+aH-SQUARE_HEIGHT//2 + i * 15))
        write(screen, f"{self.fusion.get_energy()}", FONT_LARGE, WHITE, (CENTER_X,CENTER_Y+55))
        
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
        
        self.button.draw(screen)
