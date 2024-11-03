class Element:
    def __init__(self, name, symbol, atomic_number, group, period, atomic_radius, description):
        self.name = name
        self.symbol = symbol
        self.atomic_number = atomic_number
        self.group = group # 1 a 18
        self.period = period # 1 a 7
        self.atomic_radius = atomic_radius # em pm
        self.description = description

    def __str__(self):
        #get card 
        pass

class Isotope(Element):
    def __init__(self, name, symbol, atomic_number, group, period, description, mass_number, mass, abundance, name_isotope):
        super().__init__(self, name, symbol, atomic_number, group, period, description)
        self.mass_number = mass_number
        self.mass = mass # em U
        self.abundance = abundance # em %
        self.name_isotope = name_isotope if name_isotope else f"{name}-{mass_number}"
        self.neutrons = mass_number - atomic_number

    def __str__(self):
        # get card
        pass


class FundamentalParticle:
    pass

