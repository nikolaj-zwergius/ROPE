from __future__ import annotations
import numpy as np
import os
from pathlib import Path
from rope.model.StructuralElement import StructuralElement
from rope.utils.get_sugar import get_sugar_cords


class Nucleotide(StructuralElement):
    def __init__(self,name:str, file:str|Path, symbol:str):
        super().__init__(name, file, symbol)
        self.generate_cords()

    def _generate_cords(self):
        start_res_id = None
        start_res_coord:dict[str,tuple[float,float,float]] = {}
        other_res_coord = []
        other_res_lines = []
        current_res_id = None
        try:
            with open(self.file, 'r') as f:
                for line in f:
                    if line.startswith('ATOM'):
                        if start_res_id is None:
                            start_res_id = int(line[22:26])
                        if int(line[22:26]) != current_res_id:
                                other_res_coord.append({})
                                other_res_lines.append([])
                                current_res_id = int(line[22:26])
                        other_res_coord[-1][line[12:16].strip()] = (float(line[30:38]), float(line[38:46]), float(line[46:54])) 
                        other_res_lines[-1].append(line)
                        if int(line[22:26]) == start_res_id:
                            start_res_coord[line[12:16].strip()] = (float(line[30:38]), float(line[38:46]), float(line[46:54]))
            sugar_coord = get_sugar_cords(start_res_coord)
            last_coord = get_sugar_cords(other_res_coord[-1])
            other_res_coord_dict = other_res_coord
            for i in range(len(other_res_coord)):
                other_res_coord[i] = np.array(list(other_res_coord[i].values()), dtype=np.float32)
            
        except FileNotFoundError:
            print(f"File {self.file} not found. Please check the file path.")
            raise
            return None, None, None,None,None,False
        return sugar_coord, other_res_coord, other_res_lines, last_coord,other_res_coord_dict,True

