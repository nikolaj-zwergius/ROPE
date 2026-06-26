import numpy as np

class StructuralElement():
    def __init__(self,name = 'Module', file = 'Module.pdb', symbol = 'M'):
        self.name = name
        self.file = file
        self.start_cord = None
        self.build_cords = None
        self.build_lines = None
        self.last_coord = None
        self.coord_dic = None
        self.symbol = symbol
    
    def generate_cords(self):
        self.start_cord,self.build_cords,self.build_lines,self.last_coord,self.coord_dict,self.flie_found = self._generate_cords()
