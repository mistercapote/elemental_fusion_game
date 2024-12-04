import pygame
from models.fusion import Element

pygame.init()
def write(screen : pygame.Surface, text : str, font : pygame.font.Font, color : tuple[int, int, int], center : tuple[int, int]) -> None:
    """
    Desenha o texto na tela.

    Parâmetros:
    -----------
    screen: Superfície onde o texto será desenhado.
    text: O texto a ser desenhado.
    font: A fonte usada para desenhar o texto.
    color: A cor do texto.
    center: O centro da posição onde o texto será desenhado.
    """
    render = font.render(text, True, color)
    rect = render.get_rect(center=center)
    screen.blit(render, rect)
    
WIDTH_MAX = 1280
HEIGHT_MAX = 720
ACHIE_WIDTH = WIDTH_MAX // 5
ACHIE_HEIGHT = HEIGHT_MAX // 3
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
FONT_LARGE = pygame.font.Font("assets/font/Roboto_Slab/static/RobotoSlab-Regular.ttf", 20)

class Achievement:
    """
    Representa uma conquista do jogo, com nome, descrição e os elementos desbloqueados.
    """
    def __init__(self, name: str, numbers: list, description: str, xpos: int, ypos: int, color: tuple[int, int, int]) -> None:
        """
        Inicializa uma conquista.

        Parâmetros:
        -----------
        - name: Nome da conquista.
        - numbers: Conjunto de números atômicos dos elementos relacionados à conquista.
        - description: Descrição da conquista.
        - xpos: Posição horizontal da conquista na tela.
        - ypos: Posição vertical da conquista na tela.
        - color: Cor da conquista.
        """
        self.name = name
        self.numbers = set(numbers)
        self.unlocked_elements = set()
        self.done = False
        self.description = description
        self.xpos = (xpos - 0.5) * ACHIE_WIDTH
        self.ypos = (ypos - 0.5)  * ACHIE_HEIGHT
        self.color = color
    
    def unlocked(self):
        """
        Verifica se a conquista foi desbloqueada.
        """
        if self.numbers == self.unlocked_elements:
            self.done = True

    def add_element(self, element : Element) -> None:
        """
        Adiciona um elemento à lista de elementos desbloqueados.

        Parâmetros:
        -----------
        - element: O elemento que foi desbloqueado.
        """
        if element.atomic_number in self.numbers:
            self.unlocked_elements.add(element.atomic_number)
            self.unlocked()
    
    def draw(self, screen: pygame.Surface, coef=-1):
        """
        Desenha a conquista na tela.

        Parâmetros:
        -----------
        - screen: Superfície onde a conquista será desenhada.
        - coef: Coeficiente para ajustar a margem da conquista, padrão é -1.
        """
        if not self.done:
            name_text = f"{len(self.unlocked_elements)}/{len(self.numbers)}"
            pygame.draw.rect(screen, GRAY, (self.xpos - coef, self.ypos - coef, ACHIE_WIDTH + 2*coef, ACHIE_HEIGHT + 2*coef))
        else:
            name_text = self.name
            pygame.draw.rect(screen, self.color, (self.xpos - coef, self.ypos - coef, ACHIE_WIDTH + 2*coef, ACHIE_HEIGHT + 2*coef)) 
        
        write(screen, name_text, FONT_LARGE, BLACK, (self.xpos+ACHIE_WIDTH//2, self.ypos+ACHIE_HEIGHT//2))
        
    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria uma conquista a partir de um dicionário.

        Parâmetros:
        -----------
        - data: Dicionário contendo os dados da conquista.

        Retorna:
        --------
        - Um objeto Achievement.
        """
        return cls(
            name = data["name"],
            numbers = data["numbers"],
            description = data["description"],
            xpos = data["xpos"],
            ypos = data["ypos"],
            color = data["color"]
        )
    