from views import *
from models.fusion import *
from models.button import BackingButton, CleaningButton
from models.ball import Ball
from models.popup import PopUp
from models.nucleo import Nucleo
from models.game import Game

def start_menu(game : Game):
    running = True
    nucleo = Nucleo()
    Ball.start_draw()
    found = list(map(Ball.turn_ball, game.isotopes_found + game.particles_found))
    back_button = BackingButton(game.screen, "Voltar", CENTER_X-120, HEIGHT_MAX-50)
    clean_button = CleaningButton(game.screen, "Limpar", CENTER_X+120, HEIGHT_MAX-50, nucleo.not_fusion)
    popup = None
    drag_ball = None

    while running:
        game.screen.fill(BLACK)
        game.screen.blit(nucleo.image, (3*CENTER_X//2 - nucleo.image.get_width() // 2, CENTER_Y - nucleo.image.get_height() // 2))
        write(game.screen, "Partículas", FONT_BUTTON, WHITE, (WIDTH_MAX//8, 2*HEIGHT_MAX//12))
        write(game.screen, "Isótopos", FONT_BUTTON, WHITE, (WIDTH_MAX//9.5, 4*HEIGHT_MAX//12))
        #Mostrar balls
        for ball in found: 
            ball.draw_ball(game.screen)
            if ball.drag_center: drag_ball = ball
        if drag_ball:
            if drag_ball.drag_center: drag_ball.draw_drag_ball(game.screen)

        #Mostrar barra de energia
        game.barr.draw(game.screen, nucleo.increase)
        nucleo.increase = 0
        
        #Nucleo
        nucleo.controler(game) 
        if game.new_found: found += list(map(Ball.turn_ball, game.new_found))   

        #Hover effect
        back_button.draw(game.screen)
        clean_button.draw(game.screen)

        #Mostrar popup
        if game.start_popup: 
            ancient = popup
            popup = PopUp(game.start_popup[0], game)
            if ancient != popup: pygame.mixer.Sound("assets/audio/new_element.mp3").play()
            popup.draw(game.screen)
        
        #Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = back_button.check_click(event, running)
                clean_button.check_click(event)
                if game.start_popup: 
                    popup.button.check_click(event, game, "start")
                else:
                    for ball in found: ball.check_down()
            if event.type == pygame.MOUSEBUTTONUP:
                for ball in found: ball.check_up(nucleo)
            if event.type == pygame.MOUSEMOTION:
                for ball in found: ball.check_motion(event)

        pygame.display.flip()