import pygame
from constants import *
import numpy as np

class Nucleo:
    """
    Classe que gerencia a física e animação do núcleo, incluindo fusões e explosões.
    Também controla a interação com o som e o estado de fusão dos elementos.
    """
    def __init__(self) -> None: 
        """
        Inicializa o núcleo, incluindo as variáveis de controle de som, animação e estado.
        Carrega as imagens de fundo e as animações de explosão.
        """
        self.canal1 = pygame.mixer.Channel(1)
        self.canal2 = pygame.mixer.Channel(2)
        self.speed = 0.01
        self.fusion_speed = -0.1
        self.not_fusion_speed = 0.07
        self.explosion_speed = 0.02
        self.increase = 0
        self.image = pygame.image.load(f"assets/images/nucleo.webp").convert_alpha()
        self.explosion = [pygame.image.load(f"assets/images/explosion/PNG/Circle_explosion/Circle_explosion{i}.png").convert_alpha() for i in range(1, 11)]
        self.start_nucleo()

    def start_nucleo(self) -> None:
        """
        Reinicia as variáveis associadas ao núcleo, como a lista de elementos reagentes e as variáveis de animação.
        """
        self.reacting = []  # Elementos que estão reagindo
        self.fusions = []   # Fusões possíveis entre elementos
        self.pos = []       # Posições dos elementos reagentes
        self.angle = 0      # Ângulo de rotação dos elementos
        self.radius = 100   # Raio da área de reação
        self.frame = 0      # Controle do quadro da animação de explosão
        self.canal1.stop()
        self.canal2.stop()

    def reacting_lenght(self) -> int:
        """
        Retorna a quantidade de elementos que estão reagindo no núcleo.

        Retorna:
        --------
        int: O número de elementos em reação no núcleo.
        """
        return len(self.reacting)
    
    def reacting_append(self, ball) -> None:
        """
        Adiciona um novo elemento à lista de reações.

        Parâmetros:
        -----------
        ball: Ball - O elemento que será adicionado à lista de reações.
        """
        self.reacting.append(ball)

    def update_position(self):
        """
        Atualiza a posição dos elementos em reação com base no ângulo e raio.
        """
        def position(radius : float , angle : float) -> list:
            """
            Calcula a posição com base no raio e ângulo.

            Parâmetros:
            -----------
            radius: float - O raio da posição.
            angle: float - O ângulo de rotação.

            Retorna:
            --------
            list: A posição calculada com base no raio e ângulo.
            """
            return [3*CENTER_X//2 + radius * np.cos(angle),
                    CENTER_Y + radius * np.sin(angle)
            ]
        self.pos = [position(self.radius, self.angle),
                  position(self.radius, self.angle+np.pi)
        ]

    def not_fusion(self) -> None:
        """
        Executa a lógica quando não há fusão entre os elementos reagindo.
        """
        if self.reacting:
            self.start_nucleo()
            self.canal2.play(pygame.mixer.Sound("assets/audio/no_fusion.mp3"))
    
    def rotation_animation(self, screen : pygame.Surface) -> None:
        """
        Executa a animação de rotação dos elementos em reação.

        Parâmetros:
        -----------
        screen: pygame.Surface - A tela onde a animação será desenhada.
        """
        self.angle += self.speed
        self.update_position()
        self.reacting[0].draw(screen, *self.pos[0])
        if len(self.reacting)==2:
            self.reacting[1].draw(screen, *self.pos[1])
            if not self.canal1.get_busy():
                self.canal1.play(pygame.mixer.Sound("assets/audio/pierre_roud.mp3")) 
            if not self.fusions:
                self.fusions = [obj for obj in FUSIONS if (obj.element_a == self.reacting[0].entity and obj.element_b == self.reacting[1].entity) or (obj.element_a == self.reacting[1].entity and obj.element_b == self.reacting[0].entity)]
            if self.fusions: self.radius += self.fusion_speed # Velocidade de aproximação
            else: self.radius += self.not_fusion_speed # Velocidade de afastamento

    def explosion_animation(self, screen : pygame.Surface) -> None:
        """
        Executa a animação de explosão quando a fusão é bem-sucedida.

        Parâmetros:
        -----------
        screen: pygame.Surface - A tela onde a animação será desenhada.
        """
        self.canal1.stop()
        if not self.canal2.get_busy():
            self.canal2.play(pygame.mixer.Sound("assets/audio/fusion.mp3"))
        
        img = self.explosion[int(self.frame)]
        screen.blit(img, (3*CENTER_X//2 - img.get_width() // 2, CENTER_Y - img.get_height() // 2))
        self.frame += self.explosion_speed
        if self.frame >= 10: self.radius = 0
    
    def fusion(self, game) -> None:
        """
        Realiza a fusão dos dois elementos reagindo e chama o processo recursivo de fusão.

        Parâmetros:
        -----------
        game: Game - O objeto do jogo que gerencia o estado da fusão.
        """
        self.canal2.stop()
        a = self.reacting[0].entity
        b = self.reacting[1].entity
        game = self.recursive_fusion(game, a, b)
        self.start_nucleo()

    def controler(self, game) -> None:
        """
        Controla o processo de fusão ou explosão de acordo com o estado dos elementos.

        Parâmetros:
        -----------
        game: Game - O objeto do jogo que gerencia o estado da fusão.
        """
        game.new_found = []
        if self.reacting:
            if self.radius > 220: self.not_fusion()   
            elif self.radius > 3: self.rotation_animation(game.screen)
            elif self.radius > 0: self.explosion_animation(game.screen)
            else: game = self.fusion(game)

    def recursive_fusion(self, game, a: Element, b: Element):
        """
        Realiza a fusão recursiva dos elementos, verificando se o produto já foi descoberto.

        Parâmetros:
        -----------
        game: Game - O objeto do jogo que gerencia o estado da fusão.
        a: Element - O primeiro elemento da fusão.
        b: Element - O segundo elemento da fusão.

        Retorna:
        --------
        game: Game - O objeto do jogo após a fusão.
        """
        if not self.fusions:
            self.fusions = [obj for obj in FUSIONS if (obj.element_a == a and obj.element_b == b) or (obj.element_a == b and obj.element_b == a)]
        
        if self.fusions: 
            done = 0
            for chosen_fusion in self.fusions:
                #corrigir a fusao com multiplos produtos
                if chosen_fusion not in game.fusions_found:
                    game.fusions_found.append(chosen_fusion)
                    game.start_popup.append(chosen_fusion)
                    for each in chosen_fusion.product:
                        if isinstance(each, Isotope) and each not in game.isotopes_found:
                            game.isotopes_found.append(each)
                            game.new_found.append(each)
                            self.increase = chosen_fusion.get_energy()
                            if each.is_radioactive:
                                self.start_nucleo()
                                self.recursive_fusion(game, each, None)
                        elif isinstance(each, FundamentalParticle) and each not in game.particles_found:
                            game.particles_found.append(each)
                            game.new_found.append(each)
                    break
            if done == len(self.fusions):
                #mudar mensagem do Popup
                print("Todos os produtos dessa fusao ja foram descobertos")
        else:
            print(f"O elemento {a.name} decai, mas não sei ainda o q vira")