import numpy as np
import math


# Параметры DH-таблицы
DH_PARAMS = [
    {"a": 0.0, "d": 0.21, "alpha": math.pi/2},
    {"a": -0.8, "d": 0.193, "alpha": 0.0},
    {"a": -0.598, "d": -0.16, "alpha": 0.0},
    {"a": 0.0, "d": 0.25, "alpha": math.pi/2},
    {"a": 0.0, "d": 0.25, "alpha": -math.pi/2},
    {"a": 0.0, "d": 0.25, "alpha": 0.0}
]


def dh_matrix(a, d, alpha, theta):
    """Создает матрицу преобразования"""
    ct = math.cos(theta)
    st = math.sin(theta)
    ca = math.cos(alpha)
    sa = math.sin(alpha)

    return np.array([
        [ct, -st*ca, st*sa, a*ct],
        [st, ct*ca, -ct*sa, a*st],
        [0, sa, ca, d],
        [0, 0, 0, 1]
    ])


def forward_kinematics(theta_degrees):
    """Вычисляет позицию конечного звена для заданных углов сочленений."""
    T = np.eye(4)
    theta_radians = [math.radians(t) for t in theta_degrees]

    for i in range(6):
        params = DH_PARAMS[i]
        A = dh_matrix(
            params["a"],
            params["d"],
            params["alpha"],
            theta_radians[i]
        )
        T = np.dot(T, A)

    return T[0, 3], T[1, 3], T[2, 3]  # x, y, z
