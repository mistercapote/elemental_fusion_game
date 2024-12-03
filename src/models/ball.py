import pygame
from constants import *
from abc import ABC, abstractmethod

class Ball(ABC):
    """
    Classe que representa uma bola (elemento ou partícula) no jogo.
    As bolas são interativas e podem ser arrastadas pelo jogador para realizar combinações.

    Atributos:
    ----------
    entity : object
        A entidade associada à bola, que pode ser um elemento ou uma partícula fundamental.
    drag_center : list or None
        Centro de arrasto da bola, representado como uma lista [x, y]. Inicialmente None.
    dragging : bool
        Indica se a bola está sendo arrastada pelo jogador. Inicialmente False.
    xpos : int
        Posição horizontal (x) da bola na tela.
    ypos : int
        Posição vertical (y) da bola na tela.
    """
    def __init__(self, entity):
        """
        Inicializa a bola com a entidade associada e define o estado de arrasto e posições iniciais.

        Parâmetros:
        -----------
        entity : object
            A entidade associada à bola (um elemento ou partícula).
        """
        self.entity = entity
        self.drag_center = None
        self.dragging = False
        self.xpos, self.ypos = self.position()

    def check_down(self): 
        """
        Verifica se o botão do mouse está pressionado sobre a bola.
        Se a distância do mouse ao centro da bola for menor que o raio, o arrasto é iniciado.
        """
        xm, ym = pygame.mouse.get_pos()
        #Confere se a posicao do mouse está sobre a ball
        distance = ((xm - self.xpos) ** 2 + (ym - self.ypos) ** 2) ** 0.5
        if distance < self.radius:
            self.dragging = True 
            self.drag_center = [self.xpos, self.ypos]

    def check_up(self, nucleo): 
        """
        Finaliza o arrasto da bola e verifica se ela pode ser adicionada ao núcleo.
        Se a bola estiver à direita da tela e houver espaço no núcleo, ela é adicionada.

        Parâmetros:
        -----------
        nucleo : Nucleo
            O núcleo onde as bolas são combinadas. 
            A bola será adicionada se o núcleo ainda não tiver duas bolas.

        Retorna:
        --------
        Nucleo : Retorna o núcleo atualizado.
        """
        self.dragging = False
        if self.drag_center:
            if self.drag_center[0] > CENTER_X:
                if nucleo.reacting_lenght() < 2:
                    nucleo.reacting_append(self)
                self.drag_center = None
            else:
                #é desfeito
                self.drag_center = None
                pass
        return nucleo
    
    def check_motion(self, event): 
        """
        Atualiza a posição da bola enquanto está sendo arrastada, de acordo com a posição do mouse.
        A bola é mantida dentro dos limites da tela.

        Parâmetros:
        -----------
        event : pygame.event
            Evento do Pygame contendo a posição atual do mouse.
        """
        #Atualiza a ball arrastavel para a posicao do mouse
        if self.dragging:
            new_pos = list(event.pos)
            #Lógica para colidir com os limites da tela
            new_pos[0] = max(self.radius, min(new_pos[0], WIDTH_MAX - self.radius))
            new_pos[1] = max(self.radius, min(new_pos[1], HEIGHT_MAX - self.radius))
            self.drag_center = new_pos

    @staticmethod
    def turn_ball(entity):
        """
        Converte uma entidade (elemento ou partícula) em um tipo específico de bola.

        Parâmetros:
        -----------
        entity : object
            A entidade a ser convertida (Element ou FundamentalParticle).

        Retorna:
        --------
        ElementBall ou ParticleBall : Dependendo do tipo de entidade, retorna a bola correspondente.
        """
        if isinstance(entity, Element): 
            return ElementBall(entity) 
        elif isinstance(entity, FundamentalParticle): 
            return ParticleBall(entity)

    @staticmethod
    def start_draw():
        """
        Método estático para iniciar o processo de desenhar todas as bolas na tela.
        Chama os métodos de desenho para ElementBall e ParticleBall.
        """
        ElementBall.start_draw()
        ParticleBall.start_draw()

    def draw_ball(self, screen):
        """
        Desenha a bola na tela em sua posição inicial (posição original).

        Parâmetros:
        -----------
        screen : pygame.Surface
            A superfície do Pygame onde a bola será desenhada.
        """
        self.draw(screen, self.xpos, self.ypos)

    def draw_drag_ball(self, screen):
        """
        Desenha a bola na tela na posição atual de arrasto (seguindo o mouse).

        Parâmetros:
        -----------
        screen : pygame.Surface
            A superfície do Pygame onde a bola será desenhada.
        """
        self.draw(screen, self.drag_center[0], self.drag_center[1])

    @abstractmethod
    def draw(self, screen, x, y):
        """
        Método abstrato que deve ser implementado pelas subclasses para desenhar a bola.

        Parâmetros:
        -----------
        screen : pygame.Surface
            A superfície do Pygame onde a bola será desenhada.
        x : int
            A posição horizontal da bola.
        y : int
            A posição vertical da bola.
        """
        pass

    @abstractmethod
    def position(self):
        """
        Método abstrato que deve ser implementado pelas subclasses para definir a posição inicial da bola.

        Retorna:
        --------
        tuple : Uma tupla (x, y) representando a posição inicial da bola.
        """
        pass

class ElementBall(Ball):
    """
    Representa uma bola específica para elementos (Element) no jogo.
    Herda a funcionalidade básica da classe abstrata Ball, com características
    específicas para desenhar e posicionar elementos da tabela periódica.

    Atributos:
    ----------
    (Herdados de Ball)
    entity : Element
        A entidade associada à bola, que neste caso é um elemento da tabela periódica.
    drag_center : list or None
        Centro de arrasto da bola, representado como uma lista [x, y]. Inicialmente None.
    dragging : bool
        Indica se a bola está sendo arrastada pelo jogador. Inicialmente False.
    xpos : int
        Posição horizontal (x) da bola na tela.
    ypos : int
        Posição vertical (y) da bola na tela.
    """

    @staticmethod
    def start_draw():
        """
        Inicializa os parâmetros estáticos para desenhar as bolas de elementos.
        Define a largura, altura e o raio das bolas, assim como o controle para a quebra de linha
        ao desenhar múltiplas bolas na tela.
        """
        ElementBall.www = WIDTH_MAX//20
        ElementBall.hhh = HEIGHT_MAX//3
        ElementBall.line_break = 0
        ElementBall.radius = 25
    
    def position(self):
        """
        Define a posição inicial da bola no grid da tabela periódica.
        A cada 9 elementos, inicia uma nova linha e redefine a posição horizontal.

        Retorna:
        --------
        tuple : (x, y) representando a posição inicial da bola.
        """
        if ElementBall.line_break % 9 == 0:
            ElementBall.www = WIDTH_MAX//20
            ElementBall.hhh += HEIGHT_MAX//12
        else:
            ElementBall.www += WIDTH_MAX//20
        ElementBall.line_break +=1
        return ElementBall.www, ElementBall.hhh

    def draw(self, screen, x, y):
        """
        Desenha a bola do elemento na tela como um círculo colorido.
        Dentro do círculo, desenha o número de massa e o símbolo do elemento.

        Parâmetros:
        -----------
        screen : pygame.Surface
            A superfície do Pygame onde a bola será desenhada.
        x : int
            A posição horizontal da bola.
        y : int
            A posição vertical da bola.
        """
        pygame.draw.circle(screen, self.entity.color, (x, y), self.radius)
        write(screen, f"{self.entity.mass_number}", FONT_SMALL, BLACK, (x-self.radius//2, y-self.radius//3))
        write(screen, self.entity.symbol, FONT_LARGE, BLACK, (x,y))
    
class ParticleBall(Ball):
    """
    Representa uma bola específica para partículas fundamentais no jogo.
    Herda a funcionalidade básica da classe abstrata Ball, com características
    específicas para desenhar e posicionar partículas fundamentais.

    Atributos:
    ----------
    (Herdados de Ball)
    entity : FundamentalParticle
        A entidade associada à bola, que neste caso é uma partícula fundamental.
    drag_center : list or None
        Centro de arrasto da bola, representado como uma lista [x, y]. Inicialmente None.
    dragging : bool
        Indica se a bola está sendo arrastada pelo jogador. Inicialmente False.
    xpos : int
        Posição horizontal (x) da bola na tela.
    ypos : int
        Posição vertical (y) da bola na tela.
    """

    @staticmethod
    def start_draw():
        """
        Inicializa os parâmetros estáticos para desenhar as bolas de partículas fundamentais.
        Define a largura, altura e o raio das bolas, assim como o controle para a quebra de linha
        ao desenhar múltiplas partículas na tela.
        """
        ParticleBall.www = WIDTH_MAX//20
        ParticleBall.hhh = HEIGHT_MAX//6
        ParticleBall.line_break = 0
        ParticleBall.radius = 15

    def position(self):
        """
        Define a posição inicial da bola no grid de partículas fundamentais.
        A cada 9 partículas, inicia uma nova linha e redefine a posição horizontal.

        Retorna:
        --------
        tuple : (x, y) representando a posição inicial da bola.
        """
        if ParticleBall.line_break % 9 == 0:
            ParticleBall.www = WIDTH_MAX//20
            ParticleBall.hhh += HEIGHT_MAX//12
        else: 
            ParticleBall.www += WIDTH_MAX//20
        ParticleBall.line_break +=1
        return ParticleBall.www, ParticleBall.hhh

    def draw(self, screen, x, y):
        """
        Desenha a bola da partícula na tela como um círculo colorido.
        Dentro do círculo, desenha o símbolo da partícula fundamental.

        Parâmetros:
        -----------
        screen : pygame.Surface
            A superfície do Pygame onde a bola será desenhada.
        x : int
            A posição horizontal da bola.
        y : int
            A posição vertical da bola.
        """
        pygame.draw.circle(screen, self.entity.color, (x, y), self.radius)
        write(screen, self.entity.symbol, FONT_SMALL, BLACK, (x,y))

