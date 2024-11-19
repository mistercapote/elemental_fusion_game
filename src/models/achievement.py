class Achievement:
    def __init__(self):
        self.gasnobre = [2, 10, 18, 36, 54, 86, 118]
        self.metalalcalino = [3, 11, 19, 37, 55, 87]
        self.metalalcalinoterroso = [4, 12, 20, 38, 56, 88]
        self.metaltransicaoexterna = [21, 22, 23, 24,25,26, 27, 28, 29, 30,
                                      39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
                                      72, 73, 74, 75, 76, 77, 78, 79, 80,
                                      104, 105, 106, 107, 108, 109, 110, 111, 112]
        self.metalpostransicao = [13, 31, 49, 50, 81, 82,83, 84, 85, 113, 114, 115, 116, 117]
        self.metaltransicaointerna = [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,
                                      89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103]
        self.semimetal = [5, 14, 32, 33, 51, 52]
        self.ametal = [6, 7, 8, 9, 15, 16, 17, 34, 35, 53]
        self.conquistas = []
        #self.possíveis_conquistas = ["Gases nobres", "Metais alcalinos", "Metais alcalino terrosos", "Metais de transição externa", "Metais pós-transição", "Metais de transição interna", "Semimetais", "Ametais"]


    def family_list(self, game : Game):
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
    
    def list_achievements(self):
        _, self.conquistas = self.family_list()
        historico = []

        if "Gases nobres" in self.conquistas:
            historico.append("Gases Nobres: Elementos estáveis e pouco reativos com configuração eletrônica completa.")

        if "Metais alcalinos" in self.conquistas:
            historico.append("Metais Alcalinos: Metais altamente reativos encontrados no grupo 1 da tabela periódica.")

        if "Metais alcalino terrosos" in self.conquistas:
            historico.append("Metais Alcalino-Terrosos: Metais do grupo 2, menos reativos que os alcalinos, usados em ligas e reações químicas.")

        if "Metais de transição externa" in self.conquistas:
            historico.append("Metais de Transição Externa: Metais do bloco d com alta condutividade e diversas propriedades químicas.")

        if "Metais pós-transição" in self.conquistas:
            historico.append("Metais Pós-Transição: Metais macios com baixa reatividade encontrados abaixo dos metais de transição.")

        if "Metais de transição interna" in self.conquistas:
            historico.append("Metais de Transição Interna: Elementos das séries dos lantanídeos e actinídeos, com orbitais f parcialmente preenchidos.")

        if "Semimetais" in self.conquistas:
            historico.append("Semimetais: Elementos com propriedades intermediárias entre metais e não metais.")

        if "Ametais" in self.conquistas:
            historico.append("Ametais: Elementos não metálicos com tendência a ganhar elétrons e formar compostos covalentes.")

        return historico
    