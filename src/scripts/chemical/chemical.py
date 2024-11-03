from mendeleev import element
import json

element_data = []
isotopes_data = []

for i in range(1, 119):
    e = element(i)
    print(e.atomic_number, "-", e.name)
    element_data.append({
        "name": e.name,
        "symbol": e.symbol,
        "atomic_number": e.atomic_number,
        "group": e.group_id,
        "period": e.period,
        "atomic_radius": e.atomic_radius,
        "description": e.description
    })
    for iso in e.isotopes:
        isotopes_data.append({
            "atomic_number": e.atomic_number,
            "mass_number": iso.mass_number,
            "mass": iso.mass,
            "is_radioactive": iso.is_radioactive,
            "abundance": iso.abundance,
            "name_isotope": None
        })

element_path = 'assets/json/element.json'
isotope_path = 'assets/json/isotope.json'

with open(element_path, 'w') as json_file:
    json.dump(element_data, json_file, indent=4)

with open(isotope_path, 'w') as json_file:
    json.dump(isotopes_data, json_file, indent=4)
