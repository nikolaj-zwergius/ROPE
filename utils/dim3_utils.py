import numpy as np
from numpy import ndarray

#def align_vectors(a:ndarray, b:ndarray):
#    b = b / np.linalg.norm(b) # normalize a
#    a = a / np.linalg.norm(a) # normalize b
#    v = np.cross(a, b)
#    # s = np.linalg.norm(v)
#    c = np.dot(a, b)
#    if np.isclose(c, -1.0):
#        return -np.eye(3, dtype=np.float64)
#
#    v1, v2, v3 = v
#    h = 1 / (1 + c)
#
#    Vmat = np.array([[0, -v3, v2],
#                  [v3, 0, -v1],
#                  [-v2, v1, 0]])
#
#    R = np.eye(3, dtype=np.float64) + Vmat + (Vmat.dot(Vmat) * h)
#    print(type(R))
#    return R

def umeyama(P:ndarray, Q:ndarray) -> tuple[int,ndarray,ndarray]:
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