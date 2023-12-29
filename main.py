import random
import statistics

matrix = [[0.433, 0.389, 0.491, 0.618, 0.433, 1.000, 0.433],
          [0.853, 0.945, 1.000, 1.000, 0.844, 0.734, 0.853],
          [0.847, 0.441, 1.000, 0.847, 0.441, 0.971, 0.441],
          [0.467, 0.417, 0.667, 0.500, 0.500, 1.000, 0.417],
          [0.974, 1.000, 0.920, 0.886, 0.999, 0.000, 0.994]]


priorities_range = [
    [0, 3, 2, 4, 1],
    [4, 1, 2, 0, 3],
    [2, 4, 3, 1, 0],
    [-1, -1, -1, -1, -1],
]

priorities_vector = [
    [1, 1, 2, 4, 1],
    [1, 1, 5, 2, 1],
    [1.2, 1, 4, 2, 1],
    [-1, -1, -1, -1, -1]
]

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

    risks_matrix = [[]] * len(matrix)
    for i in range(len(matrix)):
        risks_matrix[i] = matrix[i].copy()
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


def get_input_weights(ask_allowing_input_priorities=True):
    local_priorities_range = []
    local_priorities_vector = []
    allow_input_priorities = 0
    if ask_allowing_input_priorities:
        allow_input_priorities = int(input("Ввести приоритет вручную (0 - нет, 1 - да): "))

    if allow_input_priorities > 0:
        local_priorities_range = list(map(int, str(input(f"Введите ряд приоритетов ({len(priorities_range[0])} чисел): ")).split(" ")))
        local_priorities_vector = list(map(float, str(input(f"Введите вектор приоритетов ({len(priorities_vector[0])} чисел): ")).split(" ")))
    else:
        experiment_index = int(input(f"Введите номер эксперимента (1 - {len(priorities_range)}): ")) - 1
        if experiment_index != len(priorities_range) - 1:
            local_priorities_range = priorities_range[experiment_index]
            local_priorities_vector = priorities_vector[experiment_index]
        else:
            local_priorities_range = list(range(len(priorities_range[0])))
            random.shuffle(local_priorities_range)

            local_priorities_vector = [1 + random.random() * (len(priorities_vector[0]) - 1) for i in range(len(priorities_vector[0]))]

    weight_vector = priority_to_weight(local_priorities_vector)
    weight_vector_sorted = [0] * len(weight_vector)
    for id, sorted_id in enumerate(local_priorities_range):
        weight_vector_sorted[sorted_id] = weight_vector[id]

    return local_priorities_range, local_priorities_vector, weight_vector_sorted


def transpose_matrix(matrix):
    transposed_matrix = []

    for j in range(len(matrix[0])):
        row = []
        for i in range(len(matrix)):
            row.append(matrix[i][j])
        transposed_matrix.append(row)
    return transposed_matrix


def priority_to_weight(priority):
    a = [0.0] * len(priority)

    for q in range(len(a)):
        numerator = 1.0
        for i in range(q, len(a)):
            numerator *= priority[i]

        denominator = 0.0
        for j in range(1, len(a)):
            local_denominator = 1
            for n in range(j, len(a)):
                local_denominator *= priority[n]
            denominator += local_denominator

        a[q] = numerator / denominator

    sum = 0
    for i in range(len(a)):
        sum += a[i]
    for i in range(len(a)):
        a[i] /= sum

    return a


def print_list(text, list, round_num=2):
    print(text, end="")
    for v in list:
        print(f"{round(v, round_num)} ", end="")
    print()


if __name__ == '__main__':
    matrix = transpose_matrix(matrix)

    (input_priorities_range,
     input_priorities_vector,
     input_weight_vector_sorted) = get_input_weights(ask_allowing_input_priorities=True)

    #input_weight_vector_sorted = [1, 0.75, 0.84, 1.00, 0.50, 0.66]
    #[1.00, 1.00, 0.84, 0.75, 0.66, 0.50]
    #[1, 1.2, 1.12, 1.13, 1.32, 1]

    print("\n=== Исходные данные ===")

    print_list("Ряд приоритетов: ", input_priorities_range)
    print_list("Вектор прироритетов: ", input_priorities_vector)
    print_list("Весовой вектор: ", input_weight_vector_sorted)

    print("\n=== Результаты вычислений ===")

    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            matrix[y][x] *= input_weight_vector_sorted[x]

    calculate_and_output_criteria(get_laplace_criteria, "Критерий Лапласа")
    calculate_and_output_criteria(get_wald_criteria, "Критерий Вальда")
    calculate_and_output_criteria(get_savage_criteria, "Критерий Сэвиджа")
    calculate_and_output_criteria(get_hurwitz_criteria, "Критерий Гурвица (0)", optimism=0)
    calculate_and_output_criteria(get_hurwitz_criteria, "Критерий Гурвица (0.5)", optimism=0.5)
    calculate_and_output_criteria(get_hurwitz_criteria, "Критерий Гурвица (1)", optimism=1)
