

class Element:
    """
    Representa um elemento químico.

    A classe armazena informações sobre um elemento, como seu nome, símbolo, número atômico, 
    grupo, período, raio atômico, cor e descrição. Também possui um método de classe para 
    criar uma instância de um elemento a partir de um dicionário de dados.
    """
    def __init__(self, name: str, symbol: str, atomic_number:int, group: int, period: int, atomic_radius:float, color: tuple, description: str) -> None:
        """
        Constrói um objeto Element.

        Parâmetros:
        -----------
        name : str
            Nome do elemento.
        symbol : str
            Símbolo do elemento.
        atomic_number : int
            Número atômico do elemento.
        group : int
            Grupo do elemento (1 a 18).
        period : int
            Período do elemento (1 a 7).
        atomic_radius : float
            Raio atômico do elemento (em picômetros).
        color : tuple
            Cor associada ao elemento.
        description : str
            Descrição do elemento.
        """
        self.name = name
        self.symbol = symbol
        self.atomic_number = atomic_number
        self.group = group # 1 a 18
        self.period = period # 1 a 7
        self.atomic_radius = atomic_radius # em pm
        self.color = color
        self.description = description

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria um objeto Element a partir de um dicionário de dados.

        Parâmetros:
        -----------
        data : dict
            Dicionário contendo as informações do elemento.

        Retorna:
        --------
        Element
            Instância de Element.
        """
        return cls(
            name = data["name"],
            symbol = data["symbol"],
            atomic_number = data["atomic_number"],
            group = data["group"], # 1 a 18
            period = data["period"], # 1 a 7
            atomic_radius = data["atomic_radius"], # em pm
            color = data["color"],
            description = data["description"]
        )

class Isotope(Element):
    """
    Representa um isótopo de um elemento químico.

    Herda da classe Element e adiciona informações sobre o número de massa, 
    massa, radioatividade, abundância e nome do isótopo.
    """
    def __init__(self, name: str, symbol: str, atomic_number: int, group: int, period: int, atomic_radius: float, color: tuple, description: str, mass_number: int, mass:float, is_radioactive:bool, abundance: float, name_isotope: str) -> None:
        """
        Construtor da classe Isotope.

        Parâmetros:
        -----------
        name : str
            Nome do isótopo.
        symbol : str
            Símbolo do isótopo.
        atomic_number : int
            Número atômico do isótopo.
        group : int
            Grupo do elemento na tabela periódica (1 a 18).
        period : int
            Período do elemento na tabela periódica (1 a 7).
        atomic_radius : float
            Raio atômico do elemento em picômetros (pm).
        color : tuple
            Cor associada ao isótopo.
        description : str
            Descrição do isótopo.
        mass_number : int
            Número de massa do isótopo.
        mass : float
            Massa do isótopo em unidades de massa atômica (U).
        is_radioactive : bool
            Indica se o isótopo é radioativo.
        abundance : float
            Abundância do isótopo em porcentagem (%).
        name_isotope : str
            Nome do isótopo. Se não fornecido, é gerado a partir do símbolo e número de massa.
        """
        super().__init__(name, symbol, atomic_number, group, period, atomic_radius, color, description)
        self.mass_number = mass_number
        self.mass = mass # em U
        self.is_radioactive = is_radioactive
        self.abundance = abundance # em %
        self.name_isotope = name_isotope if name_isotope else f"{symbol}-{mass_number}"
        self.neutrons = mass_number - atomic_number
        
    def __eq__(self, other) -> bool:
        """
        Compara dois isótopos para verificar se são iguais.

        Parâmetros:
        -----------
        other : Isotope
            Outro isótopo a ser comparado com o isótopo atual.

        Retorna:
        --------
        bool
            Retorna True se os isótopos forem iguais (mesmo número atômico e número de massa), caso contrário, False.
        """
        if not isinstance(other, Isotope): return False
        return self.atomic_number == other.atomic_number and self.mass_number == other.mass_number
    
    @classmethod
    def from_dict(cls, data: dict, ELEMENTS: list):
        """
        Cria um objeto Isotope a partir de um dicionário de dados.

        Parâmetros:
        -----------
        data : dict
            Dicionário contendo as informações do isótopo.
        ELEMENTS : list
            Lista de elementos que são utilizados para recuperar informações adicionais do elemento base.

        Retorna:
        --------
        Isotope
            Retorna um objeto da classe Isotope.
        """
        element = list(filter(lambda x: x.atomic_number == data["atomic_number"], ELEMENTS))[0]
        return cls(
            name=element.name,
            symbol=element.symbol,
            atomic_number=element.atomic_number,
            group=element.group,
            period=element.period,
            atomic_radius=element.atomic_radius,
            color=element.color,
            description=element.description,
            mass_number = data["mass_number"],
            mass = data["mass"], # em U
            is_radioactive = data["is_radioactive"],
            abundance = data["abundance"], # em %
            name_isotope = data["name_isotope"] if data["name_isotope"] else f"{element.symbol}-{data['mass_number']}"
        )
    
            
class FundamentalParticle:
    """
    Classe para representar uma partícula fundamental.
    """
    def __init__(self, name: str, symbol: str, mass:float, charge: float, spin: float, color: tuple):
        """
        Inicializa uma partícula fundamental com os seguintes atributos:
        
        Parâmetros:
        ----------
        name : str
            O nome da partícula fundamental.
        symbol : str
            O símbolo da partícula fundamental.
        mass : float
            A massa da partícula em unidades adequadas.
        charge : float
            A carga elétrica da partícula.
        spin : float
            O spin da partícula.
        color : tuple
            A cor associada à partícula.
        """
        self.name = name
        self.symbol = symbol
        self.mass = mass
        self.charge = charge
        self.spin = spin
        self.color = color

    def __eq__(self, other) -> bool:
        """
        Compara duas partículas fundamentais para verificar se são iguais.

        Parâmetros:
        -----------
        other : FundamentalParticle
            Outra partícula a ser comparada com o partícula atual.

        Retorna:
        --------
        bool
            Retorna True se as partículas forem iguais, caso contrário, False.
        """
        if not isinstance(other, FundamentalParticle): return False
        return self.symbol == other.symbol
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria uma instância de FundamentalParticle a partir de um dicionário.

        Parâmetros:
        ----------
        data : dict
            Dicionário contendo os dados da partícula.

        Retorna:
        --------
        FundamentalParticle
            Uma nova instância de FundamentalParticle com os atributos fornecidos.
        """
        return cls(
            name = data["name"],
            symbol = data["symbol"],
            mass = data["mass"],
            charge = data["charge"],
            spin = data["spin"],
            color = data["color"],
        )

class Fusion:
    """
    Classe que representa uma fusão entre dois elementos ou partículas.
    """
    def __init__(self, process: str, element_a: Isotope, element_b: Isotope|FundamentalParticle|None, product: list, description: str):
        """
        Inicializa uma fusão com os seguintes atributos:

        Parâmetros:
        ----------
        process : str
            Nome do processo químico ao qual a fusão pertence.
        element_a : Isotope
            Primeiro elemento participante da fusão (objeto da classe Isotope).
        element_b : Isotope, FundamentalParticle ou None
            Segundo elemento ou partícula da fusão (objeto das classes Isotope, FundamentalParticle ou None).
        product : list
            Lista de produtos gerados pela fusão (objetos das classes Isotope ou FundamentalParticle).
        description : str
            Descrição do processo de fusão.
        """
        self.process = process # Nome do processo quimico que a fusão pertence
        self.element_a = element_a # Objeto da classe Isotope
        self.element_b = element_b # Objeto da classe Isotope ou FuntamentalParticle ou None
        self.product = product # Lista de Objetos das classes Isotope e FuntamentalParticle
        self.description = description # Texto falando um pouco sobre a fusão

    def __eq__(self, other) -> bool:
        """
        Verifica se duas instâncias de fusão são iguais.

        Parâmetros:
        ----------
        other : Fusion
            Outra instância da classe Fusion a ser comparada.

        Retorna:
        --------
        bool
            True se as duas fusões envolvem os mesmos elementos, False caso contrário.
        """
        if not isinstance(other, Fusion): return False
        return self.element_a == other.element_a and self.element_b == other.element_b and self.product == other.product

    # Energia gerada pela reação
    def get_energy(self):
        """
        Calcula a energia gerada pela fusão.

        Retorna:
        --------
        float
            Energia gerada pela fusão em megaelectronvolts (MeV).
        """
        U_TO_KG = 1.66053906660e-27
        J_TO_MEV =  6.242e12
        C_2 = (2.99792458e8)**2
        m_initial = self.element_a.mass + self.element_b.mass if self.element_b else self.element_a.mass
        m_final = sum([obj.mass for obj in self.product if (isinstance(obj, Isotope) or obj.symbol == "n")])
        energy_mev = (m_initial - m_final) * U_TO_KG * C_2 * J_TO_MEV
        return round(energy_mev, 4)
    
    @classmethod
    def from_dict(cls, data: dict, PARTICLES: list, ISOTOPES:list):
        """
        Cria uma instância da classe Fusion a partir de um dicionário.

        Parâmetros:
        ----------
        data : dict
            Dicionário contendo os dados para a fusão.
        PARTICLES : list
            Lista de objetos da classe FundamentalParticle.
        ISOTOPES : list
            Lista de objetos da classe Isotope.

        Retorna:
        --------
        Fusion
            Uma nova instância de Fusion.
        """
        """Cria uma instância da classe a partir de um dicionário."""
        
        def aux1(data: dict) -> Isotope|FundamentalParticle|None:
            """
            Auxilia na determinação do segundo elemento da fusão.

            Parâmetros:
            ----------
            data : dict
                Dicionário contendo os dados do segundo elemento.

            Retorna:
            --------
            Isotope ou FundamentalParticle ou None
                O segundo elemento da fusão, que pode ser um isótopo, uma partícula fundamental, ou None.
            """
            if data["element_a"] == None:
                return None
            elif "-" in data["element_a"]:
                return next((obj for obj in ISOTOPES if obj.name_isotope == data["element_a"]), None) 
            else:
                return next((obj for obj in PARTICLES if obj.symbol == data["element_a"]), None) 
        
        def aux2(data: dict) -> Isotope|FundamentalParticle|None:
            """
            Auxilia na determinação do segundo elemento da fusão.

            Parâmetros:
            ----------
            data : dict
                Dicionário contendo os dados do segundo elemento.

            Retorna:
            --------
            Isotope ou FundamentalParticle ou None
                O segundo elemento da fusão, que pode ser um isótopo, uma partícula fundamental, ou None.
            """
            if data["element_b"] == None:
                return None
            elif "-" in data["element_b"]:
                return next((obj for obj in ISOTOPES if obj.name_isotope == data["element_b"]), None) 
            else:
                return next((obj for obj in PARTICLES if obj.symbol == data["element_b"]), None) 
        
        def aux3(data: dict) -> list:
            """
            Auxilia na determinação dos produtos da fusão.

            Parâmetros:
            ----------
            data : dict
                Dicionário contendo os dados dos produtos da fusão.

            Retorna:
            --------
            list
                Lista de produtos gerados pela fusão, composta por objetos das classes Isotope ou FundamentalParticle.
            """
            resultado = []
            for each in data["product"]:
                if "-" in each:
                    resultado.append(next((obj for obj in ISOTOPES if obj.name_isotope == each), None) )
                else:
                    resultado.append(next((obj for obj in PARTICLES if obj.symbol == each), None) )
            return resultado

        return cls(
            process = data["process"], # Nome do processo quimico que a fusão pertence
            element_a = aux1(data), # Objeto da classe Isotope
            element_b = aux2(data), # Objeto da classe Isotope ou FuntamentalParticle ou None
            product = aux3(data), # Lista de Objetos das classes Isotope e FuntamentalParticle
            description = data["description"] # Texto falando um pouco sobre a fusão
        )
