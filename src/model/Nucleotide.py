from __future__ import annotations
import numpy as np
import os
from src.model.StructuralElement import StructuralElement
from src.utils.get_sugar import get_sugar_cords
from src.definitions.rope_def import NT_FOLDER


class nucleotide(StructuralElement):
    def __init__(self,name = 'Nucleotide', file = 'Nucleotide.pdb', symbol = 'N'):
        super().__init__(name, file, symbol)

    def _generate_cords(self):
        start_res_id = None
        start_res_coord = {}
        other_res_coord = []
        other_res_lines = []
        current_res_id = None
        try:
            with open(NT_FOLDER/self.file, 'r') as f:
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
            return None, None, None,None,None
        return sugar_coord, other_res_coord, other_res_lines, last_coord,other_res_coord_dict

