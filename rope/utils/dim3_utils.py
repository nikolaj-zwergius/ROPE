import numpy as np
from numpy import ndarray,float32
from rope.definitions.rope_def import SUGAR_ATOMS


def umeyama(P:ndarray, Q:ndarray) -> tuple[float32,ndarray,ndarray]:
    assert P.shape == Q.shape
    n, dim = P.shape

    centeredP = P - P.mean(axis=0)
    centeredQ = Q - Q.mean(axis=0)

    C = np.dot(np.transpose(centeredP), centeredQ) / n

    V, S, W = np.linalg.svd(C)
    d = (np.linalg.det(V) * np.linalg.det(W)) < 0.0

    if d:
        S[-1] = -S[-1]
        V[:, -1] = -V[:, -1]

    R = np.dot(V, W)

    varP = np.var(P, axis=0).sum()
    c = 1/varP * np.sum(S) # scale factor

    t = Q.mean(axis=0) - P.mean(axis=0).dot(c*R)

    return c, R, t


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