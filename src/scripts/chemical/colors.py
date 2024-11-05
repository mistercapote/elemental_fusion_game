import json

file_path = 'data/json/element.json'
with open(file_path, 'r') as file:
    elements_data = json.load(file)

# Define the new specified colors for each category
new_color_scheme = {
    "Hidrogenio": [255, 255, 255],
    "GasNobre": [123, 100, 204],
    "MetalAlcalino": [204, 100, 100],
    "MetalAlcalinoTerroso": [204, 152, 100],
    "MetalTransicaoExterna": [204, 202, 100],
    "MetalPosTransicao": [102, 204, 100],
    "MetalTransicaoInterna": [72, 173, 130],
    "Semimetal": [100, 199, 204],
    "Ametal": [84, 138, 204]
}

# Update the color attribute for each element based on its type using the new colors
for element in elements_data:
    name = element['name']
    group = element.get('group')
    
    if name == "Hydrogen":
        element['color'] = new_color_scheme["Hidrogenio"]
    elif group == 18:
        element['color'] = new_color_scheme["GasNobre"]
    elif group == 1 and name != "Hydrogen":
        element['color'] = new_color_scheme["MetalAlcalino"]
    elif group == 2:
        element['color'] = new_color_scheme["MetalAlcalinoTerroso"]
    elif group is not None and 3 <= group <= 12:
        element['color'] = new_color_scheme["MetalTransicaoExterna"]
    elif name in ["Boron", "Silicon", "Germanium", "Arsenic", "Antimony", "Tellurium"]:
        element['color'] = new_color_scheme["Semimetal"]
    elif name in ["Carbon", "Nitrogen", "Oxygen", "Phosphorus", "Sulfur", "Selenium", 
                  "Fluorine", "Chlorine", "Bromine", "Iodine", "Astatine"]:
        element['color'] = new_color_scheme["Ametal"]
    elif name in ["Lanthanum", "Cerium", "Praseodymium", "Neodymium", "Promethium", "Samarium", 
                  "Europium", "Gadolinium", "Terbium", "Dysprosium", "Holmium", "Erbium", "Thulium", 
                  "Ytterbium", "Lutetium", "Actinium", "Thorium", "Protactinium", "Uranium", 
                  "Neptunium", "Plutonium", "Americium", "Curium", "Berkelium", "Californium", 
                  "Einsteinium", "Fermium", "Mendelevium", "Nobelium", "Lawrencium"]:
        element['color'] = new_color_scheme["MetalTransicaoInterna"]
    else:
        element['color'] = new_color_scheme["MetalPosTransicao"]  # Default for other elements

# Save the updated data to a new JSON file with the revised colors
updated_file_path_v3 = 'data/json/element_2.json'
with open(updated_file_path_v3, 'w') as file:
    json.dump(elements_data, file, indent=4)

