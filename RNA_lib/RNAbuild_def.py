class Module():
    def __init__(self,name = 'Module', file = 'Module.pdb', symbol = 'M',sequence:tuple[str,str] = None):
        self.name = name
        self.file = file
        self.start_cord,self.build_cords = self.generate_cords()
        self.symbol = symbol
        self.sequence = sequence
        pass
    
    def generate_cords(self):
        start_cord = None
        build_cords = []
        return start_cord, build_cords
    def __str__(self):
        return f"Module: {self.name}"
    def __repr__(self): 
        return f"Module: {self.name}"


A=Module(name = 'A', file = '2xRNA.pdb', symbol = 'A')
C=Module(name = 'C', file = '2xRNA.pdb', symbol = 'C')
G=Module(name = 'G', file = '2xRNA.pdb', symbol = 'G')
U=Module(name = 'U', file = '2xRNA.pdb', symbol = 'U')


nucleotide_libary = {
    'A': A,
    'C': C,
    'G': G,
    'U': U,
}


Helix = Module(name = 'Helix', file = '2xRNA.pdb', symbol = 'H')
Crossover = Module(name = 'Crossover', file = '2xRNA.pdb', symbol = 'X')
TetraLoop = Module(name = 'TetraLoop', file = '2xRNA.pdb', symbol = 'T')
KissingLoop = Module(name = 'KissingLoop', file = '2xRNA.pdb', symbol = 'K')
Broccoli = Module(name = 'Broccoli', file = '2xRNA.pdb', symbol = 'B')
Mango = Module(name = 'Mango', file = '2xRNA.pdb', symbol = 'M')
Pepper = Module(name = 'Pepper', file = '2xRNA.pdb', symbol = 'P')
Cilivia = Module(name = 'Cilivia', file = '2xRNA.pdb', symbol = 'C')
Squash = Module(name = 'Squash', file = '2xRNA.pdb', symbol = 'Sq')
Spinach = Module(name = 'Spinach', file = '2xRNA.pdb', symbol = 'Sp')


module_libary = {
    'H': Helix,
    'X': Crossover,
    'T': TetraLoop,
    'K': KissingLoop,
    'B': Broccoli,
    'M': Mango,
    'P': Pepper,
    'C': Cilivia,
    'S': Squash,
    'Sp': Spinach,
    'Sq': Squash,
}