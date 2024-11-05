from views import *
from models.element import Element

def start_menu(screen):
    round = True
    hidrogenio = Element("Hidrogenio", "H", 1, 1, 1, 25, (0,0,255), "Elemento mais abundante")
    circle_center = [CENTER_X//4, CENTER_Y]
    circle_radius = 25
    dragging = False
    circle_drag_center = None
    nucleo_radius = 100

    in_nucleo = []
    angle = 0
    while round:
        angle += 0.01
        screen.fill(BLACK)
        draw_text(screen, "Particles", CENTER_X//4, CENTER_Y//8)
        # Protons, Neutrons, Eletrons, Neutrinos...
        draw_text(screen, "Elements", CENTER_X//4, CENTER_Y//2)
        pygame.draw.line(screen, WHITE, [CENTER_X, 0], [CENTER_X, HEIGHT_MAX], 5)
        back_button = draw_text(screen, "Back", CENTER_X-100, HEIGHT_MAX-50)
    
        hidrogenio.draw_ball(screen, *circle_center)
        if circle_drag_center:
            hidrogenio.draw_ball(screen, *circle_drag_center)
            
            #Hidrogenio, helio...
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                round = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    round = False 
                distance = ((pygame.mouse.get_pos()[0] - circle_center[0]) ** 2 + (pygame.mouse.get_pos()[1] - circle_center[1]) ** 2) ** 0.5
                if distance < circle_radius:
                    dragging = True  # Começa a arrastar
                    circle_drag_center = list(circle_center)  # Cópia da posição do círculo original

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                if circle_drag_center:
                    if circle_drag_center[0] > CENTER_X:
                        if len(in_nucleo) < 2:
                            in_nucleo.append(hidrogenio)
                        circle_drag_center = None
                    else:
                        #é desfeito, efeito de encolher
                        circle_drag_center = None
                        pass
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    new_pos = list(event.pos)
                    # Impede que a cópia ultrapasse as bordas da tela
                    new_pos[0] = max(circle_radius, min(new_pos[0], WIDTH_MAX - circle_radius))
                    new_pos[1] = max(circle_radius, min(new_pos[1], HEIGHT_MAX - circle_radius))

                    circle_drag_center = new_pos

        if in_nucleo:
            especial_angle = 0
            for each_particule in in_nucleo:
                circle_nucleo_center = nucleo_pos(angle + especial_angle, nucleo_radius)
                each_particule.draw_ball(screen, *circle_nucleo_center)
                especial_angle += math.pi
            if len(in_nucleo)==2:
                if nucleo_radius > 0:
                    nucleo_radius -= 0.2
                else:
                    #fundir(*in_nucleo)
                    pass
                        
        pygame.display.flip()