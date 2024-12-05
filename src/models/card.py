import pygame
from constants import *
from models.button import PopUpButton
import math

class Card:
    """
    Classe que representa um cartão no jogo, que pode conter informações sobre um elemento ou isótopo. 
    A classe gerencia a exibição de informações sobre elementos químicos e seus isótopos em uma interface gráfica.

    Atributos:
        entity: O objeto que representa o elemento ou isótopo associado ao cartão.
        xpos: A posição horizontal do cartão na tela.
        ypos: A posição vertical do cartão na tela.
        button: Botão associado ao cartão para ações (como fechar pop-ups).
        isotopes: Lista de isótopos associados ao elemento, se o cartão for de um elemento.
    """
    def __init__(self, entity: Element | None, x: int, y: int) -> None:
        """
        Inicializa o cartão com a entidade (elemento ou isótopo), 
        suas coordenadas e a configuração do botão e isótopos, se aplicável.

        Parâmetros:
        ---------
        entity : Element | None
            A entidade associada ao cartão (um elemento ou isótopo).
        x : int
            A posição horizontal do cartão na tela.
        y : int
            A posição vertical do cartão na tela.
        """
        self.entity = entity
        self.xpos = x
        self.ypos = y
        self.button = None
        if isinstance(entity, Element):
            self.isotopes = [obj for obj in ISOTOPES if (obj.atomic_number == entity.atomic_number)]
        else: self.isotopes = None

    def draw_card(self, screen: pygame.surface, coef=1) -> None:
        """
        Desenha o cartão na tela, exibindo as informações do elemento ou isótopo associado.

        Parâmetros:
        ---------
        screen : pygame.Surface
            A superfície onde o cartão será desenhado.
        coef : int, opcional
            Um fator de ajuste para o desenho, por padrão é 1.
        
        Retorna:
        --------
        None
        """
        coordenates = [(self.xpos+coef,self.ypos+coef), 
                       (self.xpos+SQUARE_WIDTH-coef, self.ypos+coef), 
                       (self.xpos+SQUARE_WIDTH-coef, self.ypos+SQUARE_HEIGHT-coef), 
                       (self.xpos+coef, self.ypos+SQUARE_HEIGHT-coef)]
        
        coordenates2 = [(self.xpos+coef-1,self.ypos+coef-1), 
                       (self.xpos+SQUARE_WIDTH-coef+1, self.ypos+coef-1), 
                       (self.xpos+SQUARE_WIDTH-coef+1, self.ypos+SQUARE_HEIGHT-coef+1), 
                       (self.xpos+coef-1, self.ypos+SQUARE_HEIGHT-coef+1)]
        
        if not self.entity:
            name_text, symbol_text = "", "?"
            pygame.draw.polygon(screen, GRAY, coordenates) 
        else:
            name_text, symbol_text = self.entity.name, self.entity.symbol
            pygame.draw.polygon(screen, self.entity.color, coordenates) 
        pygame.draw.polygon(screen, BLACK, coordenates2, 1)
        
        if coef != 1: write(screen, name_text, FONT_SMALL, BLACK, (self.xpos+SQUARE_WIDTH//2, self.ypos+7*SQUARE_HEIGHT//8-coef))
        write(screen, symbol_text, FONT_LARGE, BLACK, (self.xpos+SQUARE_WIDTH//2, self.ypos+SQUARE_HEIGHT//2))
        
        if isinstance(self.entity, Element):
            write(screen, f"{self.entity.atomic_number}", FONT_SMALL, BLACK, (self.xpos+SQUARE_WIDTH//8+coef, self.ypos+SQUARE_HEIGHT//8+coef))
            if isinstance(self.entity, Isotope):
                write(screen, f"{self.entity.mass_number}", FONT_SMALL, BLACK, (self.xpos+7*SQUARE_WIDTH//8-coef, self.ypos+SQUARE_HEIGHT//8+coef))

    def draw_popup(self, game) -> None:
        """
        Exibe um pop-up com os isótopos de um elemento, mostrando os cartões dos isótopos descobertos.

        Parâmetros:
        ---------
        game : Game
            O objeto do jogo onde o pop-up será desenhado.

        Retorna:
        --------
        None
        """
        iW = (SQUARE_WIDTH * min(12, len(self.isotopes)+2))
        
        if self.isotopes[0].description:
            palavras = self.isotopes[0].description.split(' ')  # Divide o texto em palavras
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

        aH = (SQUARE_HEIGHT * math.ceil(len(self.isotopes)/10 + 2))
        iH = aH + len(linhas)*15
        pygame.draw.rect(game.screen, BLACK, (CENTER_X-iW//2, CENTER_Y-iH//2, iW, iH))
        pygame.draw.rect(game.screen, WHITE, (CENTER_X-iW//2, CENTER_Y-iH//2, iW, iH), 5)
        write(game.screen, f"Isotopos do {self.isotopes[0].name}", FONT_LARGE, WHITE, (CENTER_X,CENTER_Y-(iH-SQUARE_HEIGHT)//2))
        
        for i, linha in enumerate(linhas):
            write(game.screen, linha, FONT_INFO, WHITE, (CENTER_X,CENTER_Y-iH//2+aH-SQUARE_HEIGHT//2 + i * 15))
        

        www = CENTER_X-iW//2 + SQUARE_WIDTH
        hhh = CENTER_Y-iH//2 + SQUARE_HEIGHT

        hover_card = None
        contador = 0
        for isotope in self.isotopes:
            if isotope in game.isotopes_found: 
                card = Card(isotope, www, hhh)
            else: 
                card = Card(None, www, hhh)
            
            contador +=1
            if contador % 10 == 0: 
                www = CENTER_X-iW//2 + SQUARE_WIDTH
                hhh += SQUARE_HEIGHT
            else:
                www += SQUARE_WIDTH

            if not hover_card:
                xm, ym = pygame.mouse.get_pos()
                if xm > card.xpos and xm < card.xpos + SQUARE_WIDTH and ym > card.ypos and ym < card.ypos + SQUARE_HEIGHT:
                    hover_card = card
                    continue
            card.draw_card(game.screen)
        if hover_card: hover_card.draw_card(game.screen, -10)

        if not self.button:
            self.button = PopUpButton(game.screen, "OK", CENTER_X+iW//2-40, CENTER_Y-iH//2 + iH-30)
        self.button.draw(game.screen)

