import numpy as np

class StructuralElement():
    def __init__(self,name = 'Module', file = 'Module.pdb', symbol = 'M'):
        self.name = name
        self.file = file
        self.symbol = symbol
        self.generate_cords()

    def generate_cords(self):
        self.start_cord,self.build_cords,self.build_lines,self.last_coord,self.coord_dict,self.flie_found = self._generate_cords()

    def _generate_cords(self) -> tuple[np.ndarray, list, list, np.ndarray, list[dict], bool]:
        raise NotImplementedError
