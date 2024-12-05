import pygame
import json
import random
import math
from constants import *
from models.button import BackingButton

# Carregar dados dos elementos e isótopos
with open('data/json/element.json', 'r',encoding="utf-8") as f:
    elements_data = json.load(f)
with open('data/json/isotope.json', 'r',encoding="utf-8") as f:
    isotopes_data = json.load(f)

pygame.init()
screen = pygame.display.set_mode((WIDTH_MAX, HEIGHT_MAX))
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 36)

# Definindo os níveis de energia
energy_levels = {1: 2, 2: 8, 3: 18}
ATOMIC_NUMBER_LIMIT = 10


def choose_element():
    """
    Função para escolher um elemento aleatório com base nos isótopos disponíveis, 
    limitando os elementos ao número atômico especificado por `ATOMIC_NUMBER_LIMIT`.
    
    Retorna:
    --------
    element : dict
        O elemento correspondente ao isótopo escolhido.
    
    isotope : dict
        O isótopo escolhido aleatoriamente.
    """
    eligible_isotopes = [iso for iso in isotopes_data if int(iso['atomic_number']) <= ATOMIC_NUMBER_LIMIT]
    isotope = random.choice(eligible_isotopes)
    element = next((elem for elem in elements_data if int(elem['atomic_number']) == isotope['atomic_number']), None)
    return element, isotope


class Particle(pygame.sprite.Sprite):
    """
    Representa uma partícula no jogo. A partícula é representada como um círculo colorido,
    e pode ser movida e arrastada pela tela.
    """
    def __init__(self, color, pos, particle_type):
        """
        Inicializa uma nova instância de partícula com um determinado tipo, cor e posição inicial.
        
        Parâmetros:
        -----------
        color : tuple
            A cor da partícula.
        
        pos : tuple
            A posição inicial da partícula.
        
        particle_type : str
            O tipo da partícula.
        """
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (10, 10), 10)
        self.rect = self.image.get_rect(center=pos)
        self.particle_type = particle_type
        self.initial_pos = pos
        self.dragging = False

    def reset_position(self):
        """
        Reseta a posição da partícula para a sua posição inicial, permitindo que ela volte à sua posição de origem após ser arrastada.
        """
        self.rect.center = self.initial_pos

    def update(self, pos):
        """
        Atualiza a posição da partícula para a nova posição, caso esteja sendo arrastada.
    
        Parâmetros:
        -----------
        pos : tuple
            A nova posição para a partícula.
        """
        if self.dragging:
            self.rect.center = pos


def place_particle(particle, nucleus_particles, electrons):
    """
    Posiciona a partícula no núcleo ou nos níveis de energia, dependendo de seu tipo.

    A partícula pode ser um próton, nêutron ou elétron. Prótons e nêutrons são posicionados no núcleo,
    enquanto elétrons são posicionados nos níveis de energia. A função leva em consideração a capacidade
    dos níveis de energia e posiciona as partículas adequadamente.

    Parâmetros:
    -----------
    particle : Particle
        A partícula a ser posicionada.
    nucleus_particles : pygame.sprite.Group
        O grupo de partículas no núcleo.
    electrons : dict
        Um dicionário que contém os elétrons posicionados nos níveis de energia. A chave é o nível de energia,
        e o valor é um conjunto de partículas (elétrons) nesse nível.
    """
    if particle.particle_type in ['proton', 'neutron']:
        # Posiciona prótons e nêutrons no núcleo
        if nucleus_rect.collidepoint(particle.rect.center):
            nucleus_particles.add(particle)
        else:
            particle.reset_position()
    elif particle.particle_type == 'electron':
        placed = False
        for level in sorted(energy_levels.keys()):
            if len(electrons[level]) < energy_levels[level]:
                
                # Calcula a posição do elétron no raio do nível
                angle = (360 / energy_levels[level]) * len(electrons[level])  # Ângulo em graus
                angle_rad = math.radians(angle)  # Converte para radianos
                radius = (level_rects[level].width // 2)  # Raio do nível de energia
                center_x, center_y = nucleus_rect.center

                # Calcula a posição do elétron na circunferência
                new_x = center_x + radius * math.cos(angle_rad)
                new_y = center_y + radius * math.sin(angle_rad)
                particle.rect.center = (new_x, new_y)

                # Adiciona o elétron ao nível
                electrons[level].add(particle)
                placed = True
                break

        if not placed:
            particle.reset_position()



def draw_element_card(screen, element, xpos, ypos, width=250, height=300):
    """
    Este cartão exibe o número atômico, símbolo, nome e massa atômica do elemento. O layout segue
    o formato de uma célula da tabela periódica. O cartão é desenhado em uma área específica da tela.

    Parâmetros:
    -----------
    screen : pygame.Surface
        A superfície onde o cartão será desenhado.
    element : dict
        Dicionário contendo informações do elemento, como nome, símbolo, número atômico e massa.
    xpos : int
        Posição X do canto superior esquerdo do cartão.
    ypos : int
        Posição Y do canto superior esquerdo do cartão.
    width : int, opcional
        A largura do cartão. O valor padrão é 250.
    height : int, opcional
        A altura do cartão. O valor padrão é 300.
    """
    num_font = pygame.font.Font(None, 45)

    pygame.draw.rect(screen, (200, 200, 200), (xpos, ypos, width, height))  # Fundo cinza
    pygame.draw.rect(screen, BLACK, (xpos, ypos, width, height), 2)

    # Número atômico
    atomic_number_text = num_font.render(f"{element['atomic_number']}", True, BLACK)
    screen.blit(atomic_number_text, (xpos + 10, ypos + 10))

    # Massa atômica
    mass_number_text = num_font.render(f"{isotope['mass_number']}", True, BLACK)
    mass_rect = mass_number_text.get_rect(topright=(xpos + width - 10, ypos + 10))
    screen.blit(mass_number_text, mass_rect)

    # Símbolo
    symbol_font = pygame.font.Font(None, 100)
    symbol_text = symbol_font.render(element['symbol'], True, BLACK)
    symbol_rect = symbol_text.get_rect(center=(xpos + width // 2, ypos + height // 2 - 20))
    screen.blit(symbol_text, symbol_rect)

    # Nome do elemento
    name_text = num_font.render(element['name'], True, BLACK)
    name_rect = name_text.get_rect(center=(xpos + width // 2, ypos + height - 40))
    screen.blit(name_text, name_rect)



def draw_button(screen, rect, text, color, text_color):
    """
    A função desenha um botão retangular com uma cor de fundo e um texto centralizado. O botão é desenhado
    na posição especificada pelo retângulo (rect), e o texto é renderizado com a cor fornecida.

    Parâmetros:
    -----------
    screen : pygame.Surface
        A superfície onde o botão será desenhado.
    rect : pygame.Rect
        O retângulo que define a posição e o tamanho do botão.
    text : str
        O texto a ser exibido no botão.
    color : tuple
        A cor de fundo do botão, no formato RGB (ex: (255, 0, 0) para vermelho).
    text_color : tuple
        A cor do texto, no formato RGB (ex: (255, 255, 255) para branco).
    """
    pygame.draw.rect(screen, color, rect)
    text_surface = FONT_LARGE.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def reset_atom(all_particles, nucleus_particles, electrons):
    """
    Esta função limpa as partículas do núcleo e dos níveis de energia, e então as reposiciona em seus
    locais iniciais.

    Parâmetros:
    -----------
    all_particles : pygame.sprite.Group
        O grupo de todas as partículas do jogo.
    nucleus_particles : pygame.sprite.Group
        O grupo de partículas que estão posicionadas no núcleo.
    electrons : dict
        Dicionário que contém os elétrons posicionados nos níveis de energia, com os níveis de energia como
        chaves e os conjuntos de partículas (elétrons) como valores.
    """
    nucleus_particles.empty()
    for level in electrons:
        electrons[level].empty()

    for particle in all_particles:
        particle.reset_position()


def validate_atom(nucleus_particles, electrons, proton_count, neutron_count, electron_count):
    """
    A função valida a construção do átomo, verificando se o número de prótons e nêutrons no núcleo está
    correto, e se a quantidade de elétrons nos níveis de energia está de acordo com as especificações do átomo.

    Parâmetros:
    -----------
    nucleus_particles : pygame.sprite.Group
        O grupo de partículas no núcleo do átomo.
    electrons : dict
        Dicionário que contém os elétrons nos níveis de energia, com os níveis como chaves e as partículas como valores.
    proton_count : int
        O número esperado de prótons no núcleo.
    neutron_count : int
        O número esperado de nêutrons no núcleo.
    electron_count : int
        O número esperado de elétrons no átomo.

    Retorna:
    --------
    bool
        Retorna True se o átomo for válido (número correto de prótons, nêutrons e elétrons), 
        caso contrário, retorna False.
    """
    # Contar prótons e nêutrons no núcleo
    nucleus_protons = sum(1 for particle in nucleus_particles if particle.particle_type == 'proton')
    nucleus_neutrons = sum(1 for particle in nucleus_particles if particle.particle_type == 'neutron')

    # Contar elétrons nos níveis de energia
    total_electrons = sum(len(electrons[level]) for level in electrons)

    # Validar núcleo
    nucleus_valid = nucleus_protons == proton_count and nucleus_neutrons == neutron_count

    # Validar elétrons
    electrons_valid = total_electrons == electron_count and all(
        len(electrons[level]) <= energy_levels[level] for level in energy_levels
    )

    return nucleus_valid and electrons_valid


def display_validation_result(screen, is_valid):
    """
    A função exibe uma mensagem na tela indicando se o átomo foi montado corretamente ou não. 
    A cor do texto é verde se o átomo for válido e vermelha se for inválido.

    Parâmetros:
    -----------
    screen : pygame.Surface
        A superfície onde o resultado da validação será exibido.
    is_valid : bool
        Indicador de validade do átomo. True se o átomo for válido, False caso contrário.
    """
    text = "Átomo Completo!" if is_valid else "Átomo Incompleto ou Inválido!"
    color = (0, 255, 0) if is_valid else (255, 0, 0)  # Verde para correto, vermelho para errado
    result_surface = FONT.render(text, True, color)
    result_rect = result_surface.get_rect(center=(WIDTH_MAX // 2, HEIGHT_MAX - 50))
    screen.blit(result_surface, result_rect)


def run_atom_builder():
    """
    A função inicia a criação de um átomo com base em um elemento e isótopo aleatórios. Ela cria as partículas 
    necessárias (prótons, nêutrons e elétrons) e organiza suas posições na tela, com a definição de retângulos 
    para o núcleo e os níveis de energia. Também cria os botões de reiniciar e verificar.

    Retorna:
    --------
    tuple
        Retorna uma tupla contendo as seguintes variáveis:
        - element : dict
            O elemento selecionado aleatoriamente.
        - isotope : dict
            O isótopo selecionado aleatoriamente.
        - proton_count : int
            O número de prótons do elemento.
        - neutron_count : int
            O número de nêutrons do isótopo.
        - electron_count : int
            O número de elétrons do átomo.
        - all_particles : pygame.sprite.Group
            Grupo contendo todas as partículas criadas (prótons, nêutrons e elétrons).
        - nucleus_particles : pygame.sprite.Group
            Grupo contendo as partículas que estarão no núcleo (prótons e nêutrons).
        - electrons : dict
            Dicionário com grupos de partículas elétrons para cada nível de energia.
        - reset_button_rect : pygame.Rect
            Retângulo que define a área do botão de reset.
        - verify_button_rect : pygame.Rect
            Retângulo que define a área do botão de verificação.
    """
    element, isotope = choose_element()
    proton_count = int(element['atomic_number'])
    neutron_count = int(isotope['mass_number']) - proton_count
    electron_count = proton_count

    # quantidade de particulas na tela
    TOTAL_PARTICLES = 18

    global nucleus_rect, level_rects
    nucleus_rect = pygame.Rect(316 - 50, HEIGHT_MAX // 2 - 50, 100, 100)

    level_rects = {
        1: pygame.Rect(316 - 100, HEIGHT_MAX // 2 - 100, 200, 200),
        2: pygame.Rect(316 - 150, HEIGHT_MAX // 2 - 150, 300, 300),
        3: pygame.Rect(316 - 200, HEIGHT_MAX // 2 - 200, 400, 400),
    }

    all_particles = pygame.sprite.Group()
    nucleus_particles = pygame.sprite.Group()
    electrons = {level: pygame.sprite.Group() for level in energy_levels.keys()}
    colors = {'proton': (255, 0, 0), 'neutron': (128, 128, 128), 'electron': (0, 0, 255)}

   # Criando partículas do tipo próton
    for i in range(TOTAL_PARTICLES):
        all_particles.add(Particle(colors['proton'], (100 + (i % 6) * 22, 600 + (i // 6) * 22), 'proton'))

    # Criando partículas do tipo nêutron
    for i in range(TOTAL_PARTICLES):
        all_particles.add(Particle(colors['neutron'], (250 + (i % 6) * 22, 600 + (i // 6) * 22), 'neutron'))

    # Criando partículas do tipo elétron
    for i in range(TOTAL_PARTICLES):
        all_particles.add(Particle(colors['electron'], (400 + (i % 6) * 22, 600 + (i // 6) * 22), 'electron'))


    reset_button_rect = pygame.Rect(WIDTH_MAX - 200, 20, 150, 50)
    verify_button_rect = pygame.Rect(WIDTH_MAX - 200, 90, 150, 50)

    return element, isotope, proton_count, neutron_count, electron_count, all_particles, nucleus_particles, electrons, reset_button_rect, verify_button_rect


element, isotope, proton_count, neutron_count, electron_count, all_particles, nucleus_particles, electrons, reset_button_rect, verify_button_rect = run_atom_builder()

def start_task(game):
    back_button = BackingButton(game.screen, "Voltar", 18*SQUARE_WIDTH, 11*SQUARE_HEIGHT)
    back_button.draw(game.screen)
    
    # Variável para o estado de validação
    validation_result = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = back_button.check_click(event, running)
                if reset_button_rect.collidepoint(event.pos):
                    reset_atom(all_particles, nucleus_particles, electrons)
                    validation_result = None  # Limpar o estado da validação
                elif verify_button_rect.collidepoint(event.pos):
                    # Quando o jogador clicar no botão "Verificar", realiza a validação
                    validation_result = validate_atom(nucleus_particles, electrons, proton_count, neutron_count, electron_count)
                for particle in all_particles:
                    if particle.rect.collidepoint(event.pos):
                        particle.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for particle in all_particles:
                    if particle.dragging:
                        particle.dragging = False
                        place_particle(particle, nucleus_particles, electrons)

        # Atualizar as partículas
        all_particles.update(pygame.mouse.get_pos())
        screen.fill(BLACK)
        back_button.draw(game.screen)
        
        # Exibir titulo
        title = pygame.font.Font(None, 50).render(f"Monte o átomo de {element['name']} ({element['symbol']})", True, WHITE)
        screen.blit(title, (30, 55))

        # Desenhar o núcleo e os níveis de energia
        pygame.draw.circle(screen, WHITE, nucleus_rect.center, nucleus_rect.width // 2, 2)
        for level, rect in level_rects.items():
            pygame.draw.circle(screen, WHITE, nucleus_rect.center, rect.width // 2, 1)

        # Exibir o cartão com informações do elemento
        draw_element_card(screen, element, xpos=WIDTH_MAX - 500, ypos=HEIGHT_MAX // 2 - 125)


        # Desenhar os botões
        draw_button(screen, reset_button_rect, "Reset", (200, 200, 200), BLACK)
        draw_button(screen, verify_button_rect, "Verificar", (200, 200, 200), BLACK)

        
        all_particles.draw(screen)

        # Verifica resultado da validação
        if validation_result is not None:
            display_validation_result(screen, validation_result)

        pygame.display.flip()




