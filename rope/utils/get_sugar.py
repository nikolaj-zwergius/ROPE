import numpy as np
from rope.definitions.rope_def import SUGAR_ATOMS
def get_sugar_cords(coords:dict) -> np.ndarray:
    sugar_coord = {}
    sugar_corrd_list=[]
    for atom in coords.keys():
        if atom in SUGAR_ATOMS:
            sugar_coord[atom] = coords[atom]
    sc_sorted = sorted(sugar_coord.keys())
    for i in range(len(sc_sorted)):
        sugar_corrd_list.append(sugar_coord[sc_sorted[i]])
    sugar_coord = np.array(sugar_corrd_list, dtype=np.float32)
    return sugar_coord