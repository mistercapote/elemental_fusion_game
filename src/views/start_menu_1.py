from views import *
from models.element import *
from models.draw import ButtonStarting, ElementBall, ParticleBall
import numpy as np

def recursive_fusion(game, a, b):
    fusions = [obj for obj in FUSIONS if (obj.element_a == a and obj.element_b == b) or (obj.element_a == b and obj.element_b == a)]
    if fusions: 
        chosen_fusion = fusions[np.random.randint(0, len(fusions))]
        if chosen_fusion not in game.fusions_found:
            game.fusions_found.append(chosen_fusion.product)
            for each in chosen_fusion.product:
                if isinstance(each, Isotope) and each not in game.isotopes_found:
                    game.isotopes_found.append(each)
                    #pop-up
                    if each.is_radioactive:
                        game = recursive_fusion(game, each, None)
                elif isinstance(each, FundamentalParticle) and each not in game.particles_found:
                    game.particles_found.append(each)
        else:
            print(f"Fusão já ocorreu")
    else:
        print(f"Fusão para {a.name} e algo mais não existe")
    return game

def start_nucleo(in_nucleo, angle, nucleo_radius): return [], 0, 100

def nucleo_pos(angle, radius):
    x = 3*CENTER_X//2 + radius * math.cos(angle)
    y = CENTER_Y + radius * math.sin(angle)
    return [x,y]

def show(isotopes_found):
    found = []
    www = WIDTH_MAX//20
    hhh = HEIGHT_MAX//3
    line_break = 0
    for isotope in isotopes_found:
        line_break +=1
        found.append(ElementBall(isotope, www, hhh))
        if line_break % 9 == 0:
            www = WIDTH_MAX//20
            hhh += HEIGHT_MAX//12
        else:
            www += WIDTH_MAX//20
    return found

def show2(particles_found):
    found = []
    www = WIDTH_MAX//20
    hhh = HEIGHT_MAX//5
    line_break = 0
    for particle in particles_found:
        line_break +=1
        found.append(ParticleBall(particle, www, hhh))
        if line_break % 9 == 0:
            www = WIDTH_MAX//20
            hhh += HEIGHT_MAX//12
        else:
            www += WIDTH_MAX//20
    return found

def start_menu(game):
    running = True
    in_nucleo, angle, nucleo_radius = start_nucleo(None, None, None)
    found = show(game.isotopes_found)
    particles_found = show2(game.particles_found)

    back_button = ButtonStarting(game.screen, "Back", CENTER_X-100, HEIGHT_MAX-50)
    clean_button = ButtonStarting(game.screen, "Clean", CENTER_X+100, HEIGHT_MAX-50, start_nucleo)

    while running:
        angle += 0.01
        game.screen.fill(BLACK)
        pygame.draw.line(game.screen, WHITE, [CENTER_X, 0], [CENTER_X, HEIGHT_MAX], 5)
        
        for ball in found:
            ball.draw_ball(game.screen)
            if ball.drag_center: ball.draw_drag_ball(game.screen)
        for ball in particles_found:
            ball.draw_ball(game.screen)
            if ball.drag_center: ball.draw_drag_ball(game.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = back_button.check_click(event, running)
                in_nucleo, angle, nucleo_radius = clean_button.check_click(event, in_nucleo, angle, nucleo_radius)
   
            for eee in [found, particles_found]:
                for ball in eee:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        distance = ((pygame.mouse.get_pos()[0] - ball.xpos) ** 2 + (pygame.mouse.get_pos()[1] - ball.ypos) ** 2) ** 0.5
                        if distance < ball.radius:
                            ball.dragging = True  # Começa a arrastar
                            ball.drag_center = [ball.xpos, ball.ypos]
                    if event.type == pygame.MOUSEBUTTONUP:
                        ball.dragging = False
                        if ball.drag_center:
                            if ball.drag_center[0] > CENTER_X:
                                if len(in_nucleo) < 2:
                                    in_nucleo.append(ball)
                                ball.drag_center = None
                            else:
                                #é desfeito, efeito de encolher
                                ball.drag_center = None
                                pass
                    if event.type == pygame.MOUSEMOTION:
                        if ball.dragging:
                            new_pos = list(event.pos)
                            # Impede que a cópia ultrapasse as bordas da tela
                            new_pos[0] = max(ball.radius, min(new_pos[0], WIDTH_MAX - ball.radius))
                            new_pos[1] = max(ball.radius, min(new_pos[1], HEIGHT_MAX - ball.radius))

                            ball.drag_center = new_pos
                
            
        if in_nucleo:
            especial_angle = 0
            for ball in in_nucleo:
                circle_nucleo_center = nucleo_pos(angle + especial_angle, nucleo_radius)
                ball.draw_nucleo_ball(game.screen, *circle_nucleo_center)
                especial_angle += math.pi
            if len(in_nucleo)==2:
                if nucleo_radius > 0:
                    nucleo_radius -= 0.2
                else:
                    a, b = in_nucleo
                    game = recursive_fusion(game, a.entity, b.entity)

                    in_nucleo, angle, nucleo_radius = start_nucleo(None, None, None)
                    found = show(game.isotopes_found)
                    particles_found = show2(game.particles_found)
        #Hover effect
        back_button.draw(game.screen, pygame.mouse.get_pos())
        clean_button.draw(game.screen, pygame.mouse.get_pos())

        pygame.display.flip()
    return game