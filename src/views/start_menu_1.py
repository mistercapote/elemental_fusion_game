from views import *
from models.element import *
from models.draw import ButtonStarting, Ball
from models.game import Nucleo

def start_menu(game):
    running = True
    nucleo = Nucleo()
    Ball.start_draw()
    found = list(map(Ball.turn_ball, game.isotopes_found + game.particles_found))
    
    back_button = ButtonStarting(game.screen, "Back", CENTER_X-100, HEIGHT_MAX-50)
    clean_button = ButtonStarting(game.screen, "Clean", CENTER_X+100, HEIGHT_MAX-50, nucleo.start_nucleo)

    while running:
        nucleo.angle += 0.01
        game.screen.fill(BLACK)
        pygame.draw.line(game.screen, WHITE, [CENTER_X, 0], [CENTER_X, HEIGHT_MAX], 5)
        
        for ball in found:
            ball.draw_ball(game.screen)
            if ball.drag_center: ball.draw_drag_ball(game.screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = back_button.check_click(event, running)
                clean_button.check_click(event)
                for ball in found: ball.check_down()
            if event.type == pygame.MOUSEBUTTONUP:
                for ball in found: nucleo = ball.check_up(nucleo)
            if event.type == pygame.MOUSEMOTION:
                for ball in found: ball.check_motion(event)
       
        nucleo, game, xfound = nucleo.controler(game) 
        if xfound: found += list(map(Ball.turn_ball, xfound))

        #Hover effect
        back_button.draw(game.screen, pygame.mouse.get_pos())
        clean_button.draw(game.screen, pygame.mouse.get_pos())

        pygame.display.flip()
    return game