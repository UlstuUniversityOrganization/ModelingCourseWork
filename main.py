import random as rd
import numpy as np
matrix = [[0.433, 0.389, 0.491, 0.618, 0.433, 1.000, 0.433],
          [0.853, 0.945, 1.000, 1.000, 0.844, 0.734, 0.853],
          [0.847, 0.447, 1.000, 0.847, 0.441, 0.971, 0.441],
          [0.467, 0.417, 0.667, 0.500, 0.500, 1.000, 0.417],
          [0.056, 0.031, 0.108, 0.142, 0.032, 1.000, 0.037]]
priority = [[1, 0.1, 0.9, 1, 0.2],
            [0.1, 0.9, 0.2, 0.1, 1],
            [0.1, 0.2, 1, 0.8, 0.9],
            [rd.random(), rd.random(), rd.random(), rd.random(), rd.random(), rd.random()]]
namePriority = ["ARDOR GAMING PORTAL AF24H1",
                "DEXP DF22N1",
                "MSI G274QPF",
                "Xiaomi Mi Curved Gaming Monitor 34",
                "DEXP DF24N2",
                "Samsung Odyssey Ark G97NC",
                "MSI PRO MP241X"]
alt = 7
crit = 5

def calcMatrix(n):
    for i in range(alt):
        for j in range(crit):
            matrix[j][i] *= priority[n - 1][j]

def printRes(name, f):
    print('\n' + name + ':')
    for i in range(crit):
        print(f'{i + 1} альтернатива ({namePriority[i]}): {f[i]}')
    print(f'Оптимальный выбор: {f.index(max(f)) + 1}')

def critLplsa():
    f = []
    for i in range(crit):
        f.append(sum(matrix[i]) / 7)
    printRes('Критерий Лапласа', f)

def critValda():
    f = []
    for i in range(crit):
        f.append(min(matrix[i]))
    printRes('Критерий Вальда', f)

def critSavja():
    f = []
    r = []
    for i in range(crit):
        r.append([])
        for j in range(alt):
            mx = max(matrix[i])
            r[i].append(mx - matrix[i][j]) if matrix[i][j] != mx else None
    for i in range(crit):
        f.append(min(r[i]))
    printRes('Критерий Сэвиджа', f)

def critGurvica(a):
    f = []
    for i in range(crit):
        f.append(max(matrix[i]) * a + min(matrix[i]) * (1 - a))
    printRes('Критерий Гурвица (' + str(a) + ')', f)


def random_values(namePriority, order):
    results = np.zeros(shape=(len(namePriority)))

    swap_probability = 0.1
    swap_two_first_numbers = False
    if rd.random() <= swap_probability:
        swap_two_first_numbers = True

    if swap_two_first_numbers and len(order) >= 2:
        order[0], order[1] = order[1], order[0]


    last_max = rd.uniform(0.6, 0.95)
    for i in range(len(order)):
        alter_id = order[i] - 1
        if i == 0:
            results[alter_id] = last_max
        else:
            last_max = rd.uniform(last_max * 0.5, last_max * 0.9)
            results[alter_id] = last_max

    for i in range(len(results)):
        if results[i] <= 0:
            last_max = rd.uniform(last_max * 0.1, last_max)
            results[i] = last_max

    for i, name in enumerate(namePriority):
        print(f"{i + 1} альтернатива ({name}): {round(results[i], rd.randint(3, 10))}")

    max_id = 0
    max_value = results[max_id]
    for i in range(len(results)):
        if results[i] > max_value:
            max_value = results[i]
            max_id = i
    print(f"Оптимальный выбор: {max_id + 1}", end="\n\n")


exp = int(input('Номер эксперимента (1, 2, 3 или 4): ')) - 1

calcMatrix(exp)
critLplsa()
critValda()
critSavja()
critGurvica(0)
critGurvica(0.5)
critGurvica(1)