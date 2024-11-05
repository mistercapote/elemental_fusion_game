from views import *
from models.element import Element

def start_menu(screen, isotopes_found):
    running = True
    in_nucleo = []
    angle = 0
    nucleo_radius = 100

    def show(isotopes_found):
        found = []
        www = WIDTH_MAX//20
        hhh = HEIGHT_MAX//3
        for element in isotopes_found:
            found.append({
                "element": element,
                "center": (www, hhh),
                "drag_center": None,
                "dragging": False,
                "radius": 25
                })
            if element.atomic_number % 9 == 0:
                www = WIDTH_MAX//20
                hhh += HEIGHT_MAX//12
            else:
                www += WIDTH_MAX//20
        return found
        
    found = show(isotopes_found)

    while running:
        angle += 0.01
        back_button = draw_text(screen, "Back", CENTER_X-100, HEIGHT_MAX-50)
        
        screen.fill(BLACK)
        draw_text(screen, "Particles", CENTER_X//4, CENTER_Y//8)
        draw_text(screen, "Elements", CENTER_X//4, CENTER_Y//2)
        pygame.draw.line(screen, WHITE, [CENTER_X, 0], [CENTER_X, HEIGHT_MAX], 5)
        
        for element in found:
            element["element"].draw_ball(screen, element["center"][0], element["center"][1])
            if element["drag_center"]:
                element["element"].draw_ball(screen, element["drag_center"][0], element["drag_center"][1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                
            for element in found:
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        running = False
                    distance = ((pygame.mouse.get_pos()[0] - element["center"][0]) ** 2 + (pygame.mouse.get_pos()[1] - element["center"][1]) ** 2) ** 0.5
                    if distance < element["radius"]:
                        element["dragging"] = True  # Começa a arrastar
                        element["drag_center"] = list(element["center"]) 

                if event.type == pygame.MOUSEBUTTONUP:
                    element["dragging"] = False
                    if element["drag_center"]:
                        if element["drag_center"][0] > CENTER_X:
                            if len(in_nucleo) < 2:
                                in_nucleo.append(element["element"])
                            element["drag_center"] = None
                        else:
                            #é desfeito, efeito de encolher
                            element["drag_center"] = None
                            pass
                if event.type == pygame.MOUSEMOTION:
                    if element["dragging"]:
                        new_pos = list(event.pos)
                        # Impede que a cópia ultrapasse as bordas da tela
                        new_pos[0] = max(element["radius"], min(new_pos[0], WIDTH_MAX - element["radius"]))
                        new_pos[1] = max(element["radius"], min(new_pos[1], HEIGHT_MAX - element["radius"]))

                        element["drag_center"] = new_pos

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
                    in_nucleo = []
                    angle = 0
                    nucleo_radius = 100
                    if ELEMENTS[1] not in isotopes_found:
                        isotopes_found.append(ELEMENTS[1])
                    else:
                        pass #reacao ja ocorreu
                    found = show(isotopes_found)
                    pass
        if back_button.collidepoint(pygame.mouse.get_pos()):
            back_button = draw_text(screen, "Back", CENTER_X-100, HEIGHT_MAX-50, 50, GRAY)
        else:
            back_button = draw_text(screen, "Back", CENTER_X-100, HEIGHT_MAX-50)
    
        pygame.display.flip()
    return isotopes_found