import numpy as np
from pathlib import Path
class StructuralElement():
    def __init__(self,name:str, file:str|Path, symbol:str):
        self.name = name
        self.file = file
        self.start_cord:np.ndarray = np.ndarray((0,0))
        self.build_cords:list[np.ndarray] = [np.ndarray((0,0))]
        self.build_lines:list[list] = []
        self.last_coord = None
        self.coord_dic = None
        self.symbol = symbol
    
    def generate_cords(self):
        self.start_cord,self.build_cords,self.build_lines,self.last_coord,self.coord_dict,self.flie_found = self._generate_cords()
    def _generate_cords(self):
        raise NotImplementedError
