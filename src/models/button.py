import pygame
from constants import *
from abc import ABC, abstractmethod
from game import Game

class Button(ABC):
    """
    Representa um botão genérico na interface gráfica do jogo. 
    Este botão pode ser clicado, exibe um texto e muda de aparência quando o mouse passa sobre ele.
    
    Atributos:
    ----------
    text : str
        O texto a ser exibido no botão.
    xpos : int
        A posição horizontal do botão na tela.
    ypos : int
        A posição vertical do botão na tela.
    hovered : bool
        Indica se o mouse está sobre o botão.
    color : tuple
        Cor de fundo do botão. Inicialmente definida como branca.
    rect : pygame.Rect
        O retângulo de colisão do botão, usado para verificar a interação com o mouse.
    action : callable or None
        A ação que será executada ao clicar no botão. Pode ser uma função ou método. Inicialmente é None.
    """
    def __init__(self, screen: pygame.Surface, text: str, x: int, y: int, action=None):
        """
        Inicializa o botão com um texto, posição, e uma ação opcional a ser executada ao clicar.

        Parâmetros:
        -----------
        screen : pygame.Surface
            A superfície do Pygame onde o botão será desenhado.
        text : str
            O texto exibido no botão.
        x : int
            A posição horizontal do botão.
        y : int
            A posição vertical do botão.
        action : callable or None, opcional
            A ação que será executada ao clicar no botão. O padrão é None.
        """
        self.text = text
        self.xpos = x
        self.ypos = y
        self.hovered = False
        self.color = WHITE
        self.rect = self.rects(screen)
        self.action = action

    def draw(self, screen: pygame.Surface):
        """
        Desenha o botão na tela. 
        Modifica a aparência do botão se o mouse estiver sobre ele (efeito de hover).

        Parâmetros:
        -----------
        screen : pygame.Surface
            A superfície do Pygame onde o botão será desenhado.
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()): self.hovered = True
        else: self.hovered = False
        self.rects(screen)

    def rects(self, screen: pygame.Surface):
        """
        Desenha o texto no botão e retorna o retângulo de colisão.
        A cor do texto e a renderização do botão mudam dependendo do estado de hover.

        Parâmetros:
        -----------
        screen : pygame.Surface
            A superfície do Pygame onde o botão será desenhado.

        Retorna:
        --------
        pygame.Rect
            O retângulo de colisão do botão, necessário para detectar cliques.
        """
        if self.hovered: surface = FONT_BUTTON_HOVER.render(self.text, True, GRAY)
        else: surface = FONT_BUTTON.render(self.text, True, WHITE)
        rect = surface.get_rect(center=(self.xpos,self.ypos))
        screen.blit(surface, rect)
        return rect
    
    @abstractmethod
    def check_click(self):
        """
        Método abstrato que verifica se o botão foi clicado.
        Deve ser implementado nas subclasses para definir o comportamento específico ao clicar.

        Este método deve retornar uma ação a ser executada quando o botão for clicado.
        """
        pass

class OpeningButton(Button):
    """
    Um botão específico para a tela de abertura do jogo. 
    Ao ser clicado, executa uma ação personalizada e controla a mídia (como música ou sons).
    Herdado da classe Button, com um comportamento de clique especializado.

    Métodos:
    --------
    check_click : Verifica se o botão foi clicado e executa a ação associada.
    """
    def check_click(self, event: pygame.event, game: Game) -> None:
        """
        Verifica o clique no botão e executa a ação associada. 
        Controla a pausa e reinício da mídia (como música) ao clicar.

        Parâmetros:
        -----------
        event : pygame.event
            O evento de clique do mouse.
        game : Game
            A instância do jogo, usada para controlar a mídia e as ações.

        Ação:
        ------
        Se o botão for clicado, executa a ação definida em `self.action`, 
        pausando a mídia antes e reiniciando-a depois.
        """
        if self.rect.collidepoint(event.pos):
            if self.action:
                game.stop_media()
                self.action(game)
                game.start_media()
   
class CleaningButton(Button):
    """
    Um botão simples que executa uma ação quando clicado.
    Herdado da classe Button, sem controle de mídia ou efeitos visuais extras.

    Métodos:
    --------
    check_click : Verifica se o botão foi clicado e executa a ação associada.
    """
    def check_click(self, event: pygame.event):
        """
        Verifica o clique no botão e executa a ação associada.

        Parâmetros:
        -----------
        event : pygame.event
            O evento de clique do mouse.

        Ação:
        ------
        Se o botão for clicado, executa a ação definida em `self.action`.
        """
        if self.rect.collidepoint(event.pos):
            if self.action:
                self.action()
    
class BackingButton(Button):
    """
    Um botão usado para parar a música e encerrar a execução do jogo quando clicado.
    Herdado da classe Button, com um comportamento de clique específico para finalizar o jogo e parar a mídia.

    Métodos:
    --------
    check_click : Verifica se o botão foi clicado e interrompe o jogo e a música.
    """
    def check_click(self, event: pygame.event, running: bool) -> bool:
        """
        Verifica o clique no botão e, se clicado, para a música e encerra o jogo.

        Parâmetros:
        -----------
        event : pygame.event
            O evento de clique do mouse.
        running : bool
            O estado do jogo, indicando se o jogo está rodando.

        Retorna:
        --------
        bool
            Retorna o estado atualizado de execução do jogo (False para parar o jogo, True para continuar).
        
        Ação:
        ------
        Se o botão for clicado, a música é parada e o estado do jogo é alterado para `not running`, 
        ou seja, o jogo será encerrado.
        """
        if self.rect.collidepoint(event.pos):
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            return not running
        return running

class PopUpButton(Button):
    """
    Um botão que controla a exibição de pop-ups no jogo.
    Ao ser clicado, ele fecha o pop-up correspondente, baseado no rótulo fornecido.

    Métodos:
    --------
    check_click : Verifica se o botão foi clicado e fecha o pop-up associado.
    """
    def check_click(self, event: pygame.event, game: Game, label: str):
        """
        Verifica o clique no botão e fecha o pop-up correspondente com base no rótulo.

        Parâmetros:
        -----------
        event : pygame.event
            O evento de clique do mouse.
        game : Game
            A instância do jogo, usada para controlar os pop-ups.
        label : str
            O rótulo que indica qual pop-up deve ser fechado ("start" ou "table").

        Ação:
        ------
        Se o botão for clicado, remove o primeiro elemento da lista de pop-ups 
        correspondente ao rótulo fornecido ("start" ou "table").
        """
        if self.rect.collidepoint(event.pos):
            if label == "start":
                game.start_popup.pop(0)
            elif label == "table":
                game.table_popup.pop(0)