from views import *
from models.element import *

def start_menu(screen, isotopes_found):
    running = True
    in_nucleo = []
    angle = 0
    nucleo_radius = 100

    def fusion(element_a, element_b):
        def confere(element_a, element_b, fusion):
            a = f"{element_a.symbol}-{element_a.mass_number}"
            if element_b == None:
                pass #decay
            elif isinstance(element_b, FundamentalParticle):
                b = f"{element_a.symbol}"
            elif isinstance(element_b, Isotope):
                b = f"{element_b.symbol}-{element_b.mass_number}"
            return (fusion.element_a == a and fusion.element_b == b) or (fusion.element_a == b and fusion.element_b == a) 
        
        fusion = list(filter(lambda x: confere(element_a, element_b, x), FUSIONS))
        if fusion: return fusion[0].product
        else: return None

    def show(isotopes_found):
        found = []
        www = WIDTH_MAX//20
        hhh = HEIGHT_MAX//3
        for isotope in isotopes_found:
            found.append({
                "isotope": isotope,
                "center": (www, hhh),
                "drag_center": None,
                "dragging": False,
                "radius": 25
                })
            if isotope.atomic_number % 9 == 0:
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
        
        for isotope in found:
            isotope["isotope"].draw_ball(screen, isotope["center"][0], isotope["center"][1])
            if isotope["drag_center"]:
                isotope["isotope"].draw_ball(screen, isotope["drag_center"][0], isotope["drag_center"][1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                
            for isotope in found:
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        running = False
                    distance = ((pygame.mouse.get_pos()[0] - isotope["center"][0]) ** 2 + (pygame.mouse.get_pos()[1] - isotope["center"][1]) ** 2) ** 0.5
                    if distance < isotope["radius"]:
                        isotope["dragging"] = True  # Começa a arrastar
                        isotope["drag_center"] = list(isotope["center"]) 

                if event.type == pygame.MOUSEBUTTONUP:
                    isotope["dragging"] = False
                    if isotope["drag_center"]:
                        if isotope["drag_center"][0] > CENTER_X:
                            if len(in_nucleo) < 2:
                                in_nucleo.append(isotope["isotope"])
                            isotope["drag_center"] = None
                        else:
                            #é desfeito, efeito de encolher
                            isotope["drag_center"] = None
                            pass
                if event.type == pygame.MOUSEMOTION:
                    if isotope["dragging"]:
                        new_pos = list(event.pos)
                        # Impede que a cópia ultrapasse as bordas da tela
                        new_pos[0] = max(isotope["radius"], min(new_pos[0], WIDTH_MAX - isotope["radius"]))
                        new_pos[1] = max(isotope["radius"], min(new_pos[1], HEIGHT_MAX - isotope["radius"]))

                        isotope["drag_center"] = new_pos

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
                    product_fusion = fusion(*in_nucleo)
                    if product_fusion:
                        for each in product_fusion:
                            each = each.split("-")
                            isotope = list(filter(lambda x: x.symbol == each[0] and x.mass_number == int(each[1]), ISOTOPES))[0]
                            if isotope not in isotopes_found:
                                isotopes_found.append(isotope)
                            else:
                                pass #reacao ja ocorreu
                            break
                    else:
                        print("Fusão não existe")
                    in_nucleo = []
                    angle = 0
                    nucleo_radius = 100
                    found = show(isotopes_found)
        if back_button.collidepoint(pygame.mouse.get_pos()):
            back_button = draw_text(screen, "Back", CENTER_X-100, HEIGHT_MAX-50, 50, GRAY)
        else:
            back_button = draw_text(screen, "Back", CENTER_X-100, HEIGHT_MAX-50)
    
        pygame.display.flip()
    return isotopes_found