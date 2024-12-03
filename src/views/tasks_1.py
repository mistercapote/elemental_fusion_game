import pygame
import json
import random
import math

WIDTH_MAX = 1280
HEIGHT_MAX = 720

# Carregar dados dos elementos e isótopos
with open('data/json/element.json', 'r') as f:
    elements_data = json.load(f)
with open('data/json/isotope.json', 'r') as f:
    isotopes_data = json.load(f)

pygame.init()
screen = pygame.display.set_mode((WIDTH_MAX, HEIGHT_MAX))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

# Definindo os níveis de energia
energy_levels = {1: 2, 2: 8, 3: 18}
ATOMIC_NUMBER_LIMIT = 10

# Função para escolher um elemento aleatório
def choose_element():
    eligible_isotopes = [iso for iso in isotopes_data if int(iso['atomic_number']) <= ATOMIC_NUMBER_LIMIT]
    isotope = random.choice(eligible_isotopes)
    element = next((elem for elem in elements_data if int(elem['atomic_number']) == isotope['atomic_number']), None)
    return element, isotope


class Particle(pygame.sprite.Sprite):
    def __init__(self, color, pos, particle_type):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (10, 10), 10)
        self.rect = self.image.get_rect(center=pos)
        self.particle_type = particle_type
        self.initial_pos = pos
        self.dragging = False

    def reset_position(self):
        self.rect.center = self.initial_pos

    def update(self, pos):
        if self.dragging:
            self.rect.center = pos


def place_particle(particle, nucleus_particles, electrons):
    """Posiciona a partícula no núcleo ou nos níveis de energia."""
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
    Desenha um cartão no estilo da tabela periódica com informações do elemento.
    
    Parâmetros:
    - screen: superfície onde o cartão será desenhado.
    - element: dicionário contendo informações do elemento (nome, símbolo, número atômico, massa).
    - xpos, ypos: posição do canto superior esquerdo do cartão.
    - width, height: dimensões do cartão.
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
    pygame.draw.rect(screen, color, rect)
    text_surface = FONT.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


# Retorna todas as particulas à posição inicial
def reset_atom(all_particles, nucleus_particles, electrons):
    nucleus_particles.empty()
    for level in electrons:
        electrons[level].empty()

    for particle in all_particles:
        particle.reset_position()


# Valida se o átomo foi montado corretamente.
def validate_atom(nucleus_particles, electrons, proton_count, neutron_count, electron_count):

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


#Exibe o resultado da validação na tela.
def display_validation_result(screen, is_valid):
    text = "Átomo Completo!" if is_valid else "Átomo Incompleto ou Inválido!"
    color = (0, 255, 0) if is_valid else (255, 0, 0)  # Verde para correto, vermelho para errado
    result_surface = FONT.render(text, True, color)
    result_rect = result_surface.get_rect(center=(WIDTH_MAX // 2, HEIGHT_MAX - 50))
    screen.blit(result_surface, result_rect)


def run_atom_builder():
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


# Variável para o estado de validação
validation_result = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
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
    clock.tick(30)

pygame.quit()




run_atom_builder()
