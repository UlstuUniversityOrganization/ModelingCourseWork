import random as rd
import numpy as np
import statistics
import pandas
matrix = [[0.433, 0.389, 0.491, 0.618, 0.433, 1.000, 0.433],
          [0.853, 0.945, 1.000, 1.000, 0.844, 0.734, 0.853],
          [0.847, 0.447, 1.000, 0.847, 0.441, 0.971, 0.441],
          [0.467, 0.417, 0.667, 0.500, 0.500, 1.000, 0.417],
          [0.056, 0.031, 0.108, 0.142, 0.032, 1.000, 0.037]]

priorities = [[1, 0.1, 0.9, 1, 0.2],
            [0.1, 0.9, 0.2, 0.1, 1],
            [0.1, 0.2, 1, 0.8, 0.9],
            [rd.random(), rd.random(), rd.random(), rd.random(), rd.random(), rd.random()]]

alternative_names = ["ARDOR GAMING PORTAL AF24H1",
                    "DEXP DF22N1",
                    "MSI G274QPF",
                    "Xiaomi Mi Curved Gaming Monitor 34",
                    "DEXP DF24N2",
                    "Samsung Odyssey Ark G97NC",
                    "MSI PRO MP241X"]


def get_laplace_criteria(matrix):
    laplace_criteria = []

    for alternative in matrix:
        laplace_criteria.append(statistics.mean(alternative))

    decision = laplace_criteria.index(max(laplace_criteria))
    return laplace_criteria, decision


def get_wald_criteria(matrix):
    wald_criteria = []

    for alternative in matrix:
        wald_criteria.append(min(alternative))
    decision = wald_criteria.index(max(wald_criteria))

    return wald_criteria, decision


def get_savage_criteria(matrix):
    savage_criteria = []

    max_features = []
    columns_count = len(matrix[0])
    for j in range(columns_count):
        max_feature = 0
        for i in range(len(matrix)):
            if matrix[i][j] > max_feature:
                max_feature = matrix[i][j]
        max_features.append(max_feature)

    risks_matrix = matrix.copy()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            risks_matrix[i][j] = max_features[j] - matrix[i][j]

    for risks in risks_matrix:
        savage_criteria.append(max(risks))

    decision = savage_criteria.index(min(savage_criteria))
    return savage_criteria, decision


def get_hurwitz_criteria(matrix, optimism):
    wald_criteria = []

    for alternative in matrix:
        wald_criteria.append(optimism * max(alternative) + (1 - optimism) * min(alternative))
    decision = wald_criteria.index(max(wald_criteria))

    return wald_criteria, decision


def output_criteria_and_decision(names, criteria, decision):
    for i in range(len(matrix)):
        print(f"{i + 1}) {names[i]}: {criteria[i]}")
    print(f"Оптимальный выбор: {decision + 1}")


def calculate_and_output_criteria(criteria_function, criteria_name, optimism=-1.0):
    if optimism >= 0:
        criteria, decision = criteria_function(matrix, optimism)
    else:
        criteria, decision = criteria_function(matrix)
    print(f"{criteria_name}:")
    output_criteria_and_decision(alternative_names, criteria, decision)
    print()


def get_input_priorities(ask_allowing_input_priorities=True):
    chosen_priorities = []
    allow_input_priorities = 0
    if ask_allowing_input_priorities:
        allow_input_priorities = int(input("Ввести приоритет вручную (0 - нет, 1 - да): "))

    if allow_input_priorities > 0:
        priorities_str = str(input(f"Введите {len(priorities[0])} приоритетов через пробел: ")).split(" ")
        for priority in priorities_str:
            chosen_priorities.append(priority)
    else:
        experiment_index = int(input(f"Введите номер эксперимента (1 - {len(priorities)}): ")) - 1
        chosen_priorities = priorities[experiment_index]
    return chosen_priorities


if __name__ == '__main__':
    input_priorities = get_input_priorities(ask_allowing_input_priorities=False)

    calculate_and_output_criteria(get_laplace_criteria, "Критерий Лапласа")
    calculate_and_output_criteria(get_wald_criteria, "Критерий Вальда")
    calculate_and_output_criteria(get_savage_criteria, "Критерий Сэвиджа")
    calculate_and_output_criteria(get_hurwitz_criteria, "Критерий Гурвица", optimism=0.5)

