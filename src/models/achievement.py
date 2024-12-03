

class Achievement:
    def __init__(self, name, numbers, description, xpos, ypos):
        self.name = name
        self.numbers = numbers
        self.done = False
        self.description = description
        self.xpos = xpos * 1280 // 5
        self.ypos = ypos * 720 // 3.5
    
    def family_list(self, game):
        conquista_atual = None

        for each in game.isotopes_found:
            if each.atomic_number in self.gasnobre:
                self.gasnobre.remove(each.atomic_number)
                if not self.gasnobre:
                    conquista_atual = "Gases nobres"
                    self.conquistas.append("Gases nobres")
            elif each.atomic_number in self.metalalcalino:
                self.metalalcalino.remove(each.atomic_number)
                if not self.metalalcalino:
                    conquista_atual = "Metais alcalinos"
                    self.conquistas.append("Metais alcalinos")
            elif each.atomic_number in self.metalalcalinoterroso:
                self.metalalcalinoterroso.remove(each.atomic_number)
                if not self.metalalcalinoterroso:
                    conquista_atual = "Metais alcalino terrosos"
                    self.conquistas.append("Metais alcalino terrosos")
            elif each.atomic_number in self.metaltransicaoexterna:
                self.metaltransicaoexterna.remove(each.atomic_number)
                if not self.metaltransicaoexterna:
                    conquista_atual = "Metais de transição externa"
                    self.conquistas.append("Metais de transição externa")
            elif each.atomic_number in self.metalpostransicao:
                self.metalpostransicao.remove(each.atomic_number)
                if not self.metalpostransicao:
                    conquista_atual = "Metais pós-transição"
                    self.conquistas.append("Metais pós-transição")
            elif each.atomic_number in self.metaltransicaointerna:
                self.metaltransicaointerna.remove(each.atomic_number)
                if not self.metaltransicaointerna:
                    conquista_atual = "Metais de transição interna"
                    self.conquistas.append("Metais de transição interna")
            elif each.atomic_number in self.semimetal:
                self.semimetal.remove(each.atomic_number)
                if not self.semimetal:
                    conquista_atual = "Semimetais"
                    self.conquistas.append("Semimetais")
            elif each.atomic_number in self.ametal:
                self.ametal.remove(each.atomic_number)
                if not self.ametal:
                    conquista_atual = "Ametais"
                    self.conquistas.append("Ametais")

        return conquista_atual, self.conquistas
    
    def recently_achievement(self):
         conquista_atual, _ = self.family_list()

         return f"Parabens! Você desbloqueou todos os {conquista_atual}"
    
    def draw(self):
        _, self.conquistas = self.family_list()
        historico = []

        return historico
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name = data["name"],
            numbers = data["numbers"],
            description = data["description"],
            xpos = data["xpos"],
            ypos = data["ypos"],
        )