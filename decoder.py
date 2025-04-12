# decoder.py
import numpy as np
import time

def spa_decode(H, r, I_max=50):
    m, n = H.shape
    I = 0
    M = np.zeros((m, n))

    for i in range(n):
        for j in np.where(H[:, i])[0]:
            M[j, i] = r[i]

    start_time = time.time()

    while True:
        E = np.zeros((m, n))
        for j in range(m):
            indices = np.where(H[j])[0]
            for i in indices:
                others = [k for k in indices if k != i]
                product = np.prod([np.tanh(M[j, k] / 2) for k in others])
                E[j, i] = np.log((1 + product) / (1 - product + 1e-12))

        L = np.zeros(n)
        z = np.zeros(n, dtype=int)
        for i in range(n):
            connected = np.where(H[:, i])[0]
            L[i] = np.sum(E[connected, i]) + r[i]
            z[i] = 1 if L[i] <= 0 else 0

        if I >= I_max or np.all(np.mod(H @ z, 2) == 0):
            break

        for i in range(n):
            connected = np.where(H[:, i])[0]
            for j in connected:
                others = [jj for jj in connected if jj != j]
                M[j, i] = r[i] + np.sum(E[others, i])

        I += 1

    decode_time = time.time() - start_time
    return z, I, decode_time, L
