import numpy as np

container_A = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1]
]

container_E = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1]
]

container_I = [
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1]
]

container_O = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

container_U = [
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0]
]

# Cambio de 0's a -1's
n = len(container_A)
m = len(container_A[0])

for i in range(n):
    for j in range(m):
        if container_A[i][j] == 0:
            container_A[i][j] = -1
        if container_E[i][j] == 0:
            container_E[i][j] = -1
        if container_I[i][j] == 0:
            container_I[i][j] = -1
        if container_O[i][j] == 0:
            container_O[i][j] = -1
        if container_U[i][j] == 0:
            container_U[i][j] = -1

# Conjunto de patrones
matrix_patterns: np.array = [
    np.array(container_A),
    np.array(container_E),
    np.array(container_I),
    np.array(container_O),
    np.array(container_U)
]

# -----------------------------
# CONSTRUCCIÓN DE LA MEMORIA
# -----------------------------

# Matriz identidad y contenedor resultado
# La matriz identidad debe ser de igual tamaño que el resultado
# 7x7
matrix_identity = np.eye(N=n*m, M=n*m)

# A: filas 7 x columna 5
# B: columna 5 x filas 7
# -> C: filas 7 x columnas 7
# C - Identidad: C(7x7) - I(7x7)
sum_matrix = np.zeros((n*m, n*m))

# Se multiplica la matriz por su transpuesta y se resta
# la matriz identidad Y se calcula la suma de todas
for mx  in matrix_patterns:
    # (35 x 1)
    v: np.array = mx.reshape(-1, 1, order='F')
    # (35 x 1) * (1 x 35) 
    aux = (v @ v.T) - matrix_identity
    sum_matrix = sum_matrix + aux


# -----------------------------
# FASE DE RECUPERACIÓN
# -----------------------------

# Convierte a (35 x 1)
column_input_mx = np.array(container_O).reshape(-1, 1, order='F')

# Crea matriz de ceros (35 x 1)
xt_1 = np.zeros((n*m, 1)) # x(t + 1)

# Incializamos con la entrada v (35 x 1)
xt = column_input_mx

while not np.array_equal(xt_1, xt):

    # sum_matrix(35 x 35) * column_mx(35 x 1) = res(35 x 1)
    temp = sum_matrix @ xt # Mij * x(t)

    # calculo x(t+1) = xt_1
    for i in range(n*m):
        if temp[i, 0] < 0:
            xt_1[i, 0] = -1
        else:
            xt_1[i, 0] = 1

    # x(t) = x(t + 1)
    xt = xt_1.copy()


print(xt.reshape((7, 5), order='F'))