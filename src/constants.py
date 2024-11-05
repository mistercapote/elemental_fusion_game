#Constant
from models.element import Element, Isotope
from models.fusion import Fusion
WIDTH_MAX = 1280
HEIGHT_MAX = 720

CENTER_X = WIDTH_MAX // 2
CENTER_Y = HEIGHT_MAX // 2

SQUARE_WIDTH = WIDTH_MAX // 20
SQUARE_HEIGHT = HEIGHT_MAX // 12

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

ELEMENTS = Element.load_elements_from_json("data/json/element.json")
ISOTOPES = Isotope.load_elements_from_json_2(ELEMENTS, "data/json/element.json", "data/json/isotope.json")
FUSIONS = Fusion.load_elements_from_json("data/json/fusion.json")

# for i in ISOTOPES:
#     print(i.atomic_number, i.name. i.)
# ISOTOPES = Isotope.