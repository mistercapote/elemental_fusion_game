import pygame
import moviepy.editor as mp
import sys
from constants import *
from models.card import Card
from views import achiev_menu, start_menu_1, start_menu_2, story_menu, table_menu
from models.button import OpeningButton, BackingButton

class Game:
    def __init__(self):
        """
        Inicializa a instância do jogo, configurando os recursos necessários e a interface gráfica.

        Este método configura os parâmetros iniciais do jogo, incluindo a inicialização do Pygame, a criação da 
        janela do jogo, e o carregamento de arquivos como música, vídeo e textos da história. Ele também configura 
        os dados relacionados aos elementos do jogo, como os isótopos, partículas e fusões encontrados.

        Atributos:
        ----------
        title : str
            O título do jogo.

        current_phase : int
            A fase atual do jogo.

        screen : pygame.Surface
            A superfície onde o jogo será renderizado.

        caption : str
            O título da janela do jogo.

        video : str
            O caminho para o arquivo de vídeo de abertura.

        music : str
            O caminho para o arquivo de áudio de abertura.

        story_text : str
            O caminho para o arquivo de texto da história.

        story_image : str
            O caminho para a imagem de fundo da história.

        story_music : str
            O caminho para a música de fundo da história.

        clock : pygame.time.Clock
            O relógio que controla a taxa de quadros do jogo.

        isotopes_found : list
            Lista dos isótopos encontrados no jogo.

        particles_found : list
            Lista das partículas encontradas no jogo.

        fusions_found : list
            Lista das fusões descobertas.

        new_found : list
            Lista de novos elementos descobertos.

        start_popup : list
            Lista de pop-ups de início.

        table_popup : list
            Lista de pop-ups da tabela.

        barr : Barr
            Instância da classe Barr que gerencia a energia do jogo.

        start_media() : None
            Método chamado para iniciar o vídeo e música de introdução do jogo.
    """
        pygame.init()
        pygame.mixer.init() 
        self.title = "KILL THAT STAR"
        self.current_phase = 1
        self.screen = pygame.display.set_mode((WIDTH_MAX, HEIGHT_MAX))
        self.caption = pygame.display.set_caption("Elemental Fusion Game")
        self.video = "assets/videos/video_opening.mp4"
        self.music = "assets/audio/audio_opening.mp3"
        self.story_text = "assets/texts/story_level_1.txt"
        self.story_image = "assets/images/fundo_story_menu.png"
        self.story_music = "assets/audio/simple-relaxing-guitar-loop-60828_lofi.mp3"
        self.start_button = OpeningButton(self.screen, "Jogar", CENTER_X, CENTER_Y - 70, start_menu_1.start_menu)
        self.story_button = OpeningButton(self.screen, "História", CENTER_X, CENTER_Y, story_menu.story_menu)
        self.table_button = OpeningButton(self.screen, "Tabela Periódica", CENTER_X, CENTER_Y + 70, table_menu.table_menu)
        self.settings_button = OpeningButton(self.screen, "Conquistas", CENTER_X, CENTER_Y + 140, achiev_menu.achiev_menu)
        self.exit_button = OpeningButton(self.screen, "Sair", CENTER_X, CENTER_Y + 210, self.quit)
        self.clock = pygame.time.Clock()
        self.particles_found = [PARTICLES[0], PARTICLES[2]]
        self.isotopes_found = ISOTOPES
        self.fusions_found = []
        self.new_found = []
        self.start_popup = []
        self.table_popup = []
        self.bar = Bar()
        self.iron = ISOTOPES[552]
        self.start_media()
        
    def update_partial(self):
        """
        Atualiza o as mídias para uma tela parcial.
        """
        self.video = "assets/videos/supernova.mp4"
        self.music = "assets/audio/supernova.mp3"
        self.start_media()

    def update_for_level_2(self):
        """
        Atualiza o jogo para o nível 2, alterando o título, a fase atual, 
        o vídeo e a música de abertura, e inicia a mídia associada.
        """
        self.title = "PARTICLE ACCELERATOR"
        self.current_phase = 2
        self.video = "assets/videos/video_opening_2.mp4"
        self.music = "assets/audio/audio_opening.mp3"
        self.story_text = "assets/texts/story_level_2.txt"
        self.start_button = OpeningButton(self.screen, "Jogar", CENTER_X, CENTER_Y - 70, start_menu_2.start_menu)
        self.start_media()

    def draw_button(self):
        self.start_button.draw(self.screen)
        self.story_button.draw(self.screen)
        self.table_button.draw(self.screen)
        self.settings_button.draw(self.screen)
        self.exit_button.draw(self.screen)

    def check_button(self, event):
        self.start_button.check_click(event, self)
        self.story_button.check_click(event, self)
        self.table_button.check_click(event, self)
        self.settings_button.check_click(event, self)
        self.exit_button.check_click(event, self)

    def draw_title(self):
        """
        Desenha o título do jogo na tela.
        """
        write(self.screen, self.title, FONT_GIGANT, WHITE, (CENTER_X, 2*HEIGHT_MAX//9))
    
    def start_media(self):
        """
        Inicia a reprodução do vídeo de abertura e a música de fundo.
        """
        self.video_clip = mp.VideoFileClip(self.video)
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(-1)
    
    def stop_media(self):
        """
        Para a reprodução do vídeo e da música de fundo.
        """
        self.video_clip.close()
        pygame.mixer.music.stop()
    
    @staticmethod
    def quit(game=None):
        """
        Encerra o jogo e fecha a janela do pygame.

        Parâmetros:
        -----------
        game : Game, opcional
            O objeto do jogo. Não é necessário fornecer, mas pode ser passado caso queira encerrar o jogo de forma controlada.
        """
        pygame.quit()
        sys.exit()

    def updateVideoFrame(self):
        """
        Atualiza o quadro de vídeo atual, exibindo o próximo frame do vídeo de abertura.
        """
        current_time = self.video_clip.reader.pos / self.video_clip.fps
        if current_time >= self.video_clip.duration: 
            current_time = 0 
        frame = self.video_clip.get_frame(current_time)
        self.screen.blit(pygame.surfarray.make_surface(frame.swapaxes(0, 1)), (0, 0))
        self.clock.tick(self.video_clip.fps)

    def start_story(self):
        """
        Inicia a exibição da história do jogo, carregando o texto, a imagem de fundo e a música.
        """
        with open(self.story_text, "r", encoding="utf-8") as file: 
            lines =  file.read().splitlines()
        image = pygame.transform.scale(pygame.image.load(self.story_image).convert(), [WIDTH_MAX, HEIGHT_MAX])
        pygame.mixer.music.load(self.story_music)
        pygame.mixer.music.play(-1)
        return lines, image
    
    def start_table(self):
        """
        Cria e retorna a tabela periódica do jogo, com os elementos e suas respectivas informações.
        """
        table = []
        for element in ELEMENTS:
            if element.group == None or element.atomic_number == 57 or element.atomic_number == 89:
                if element.period == 6: left_x = int(element.atomic_number-53) * SQUARE_WIDTH
                elif element.period == 7: left_x = int(element.atomic_number-85) * SQUARE_WIDTH
                top_y = int(element.period + 3) * SQUARE_HEIGHT
            else:
                left_x = int(element.group) * SQUARE_WIDTH
                top_y = int(element.period) * SQUARE_HEIGHT
            if list(filter(lambda x: x.atomic_number == element.atomic_number, self.isotopes_found)):
                card = Card(element, left_x, top_y)
            else:
                card = Card(None, left_x, top_y)
            table.append(card)
        return table
    
    def checkend(self, running):
        if self.current_phase == 1 and self.bar.width_current >= 200 and self.iron in self.isotopes_found:
            
            self.stop_media()
            self.update_partial()

            backingbutton = BackingButton(self.screen, "Bora!", CENTER_X, 3*CENTER_Y//2)
            texto = (
                    "Parabéns! Com a energia necessária, o Fe-56 foi fundido, e esse processo levou a estrela a colapsar!"
                    " Agora você está em um reator nuclear e deve resolver as tarefas!"
                )
            
            palavras = texto.split(' ')  # Divide o texto em palavras
            linhas = []
            linha_atual = ""

            for palavra in palavras:
                # Verifica se a linha atual, com a próxima palavra, ultrapassa a largura máxima
                if FONT_BUTTON.size(linha_atual + palavra)[0] <= WIDTH_MAX:
                    linha_atual += palavra + " "
                else:
                    linhas.append(linha_atual.strip())
                    linha_atual = palavra + " "

            if linha_atual:  # Adiciona a última linha
                linhas.append(linha_atual.strip())

            running2 = True
            while running2:
                self.screen.fill(BLACK)

                self.updateVideoFrame() #Atualizar video de fundo
                backingbutton.draw(self.screen)
                
                for i, linha in enumerate(linhas):
                    write(self.screen, linha, FONT_STORY, WHITE, (CENTER_X, CENTER_Y - 150 + i * 35))
                    
                # Eventos
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        running2 = backingbutton.check_click(event, running2)
                        running = running2
                pygame.display.flip()

            self.isotopes_found.extend(list(map(lambda x: [i for i in ISOTOPES if i.name_isotope == x][0], SUPERNOVA)))
            self.update_for_level_2()
        return running

class Bar:
    """
    Classe que representa uma barra de progresso, usada para indicar o avanço em uma determinada fase do jogo.    
    """
    def __init__(self):
        """
        Inicializa a instância da barra de progresso.

        Atributos:
        ----------
        height : int
            A altura da barra de progresso.
        width_max : int
            A largura máxima da barra de progresso.
        width_current : int
            A largura atual da barra de progresso, que aumenta à medida que o progresso avança.
        pos_x : int
            A posição X da barra na tela.
        pos_y : int
            A posição Y da barra na tela.
        """
        self.height = 50
        self.width_max = 200
        self.width_current = 0
        self.pos_x = CENTER_X // 2 - 100
        self.pos_y = CENTER_Y // 9 - 25

    def draw(self, screen, increase : int):
        """
        Desenha a barra de progresso na tela e aumenta seu tamanho de acordo com o progresso.

        Parâmetros:
        -----------
        screen : pygame.Surface
            A superfície do jogo onde a barra será desenhada.
        increase : int
            O valor que será adicionado à largura atual da barra de progresso.
        """
        increase = 3*increase
        if self.width_current + int(increase) >= 0:
            if self.width_current + int(increase) < self.width_max:
                self.width_current += int(increase)
            else:
                self.width_current = 200

        if self.width_current > 5:
            pygame.draw.rect(screen, YELLOW, (self.pos_x, self.pos_y, self.width_current, self.height), 0, -1, 10, 10, 10, 10)
        pygame.draw.rect(screen, WHITE, (self.pos_x, self.pos_y, self.width_max, self.height), 3, -1, 10, 10, 10, 10)

        
