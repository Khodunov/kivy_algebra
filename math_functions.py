import numpy as np
from scipy.linalg import null_space


def find_vk(matrix, c):

    n = len(matrix)
    id_n = np.eye(n)
    quasi_nil = np.matrix(matrix) - c * id_n

    vk = [kernel(quasi_nil)]
    last_rank = np.linalg.matrix_rank(quasi_nil)
    power = quasi_nil
    while True:
        power = np.dot(power, quasi_nil)
        if last_rank == np.linalg.matrix_rank(power):
            break
        else:
            last_rank = np.linalg.matrix_rank(power)
            vk.append(kernel(power))

    return vk


def kernel(a):
    ker = null_space(a).T
    result = []
    for line in ker:
        for el in line:
            if abs(el) > 1e-10:
                line = line/el
                break
        result.append(line)
    return result


a = np.matrix([[0,1,1],
              [0,1,1]])
print(kernel(a))