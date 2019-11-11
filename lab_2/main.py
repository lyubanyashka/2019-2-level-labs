"""
Labour work #2. Levenshtein distance.
"""


def generate_edit_matrix(num_rows: int, num_cols: int) -> list:
    if type(num_rows) is not int or type(num_cols) is not int:
        return []
    return [[0 for j in range(num_cols)] for i in range(
        num_rows)]  # вложенный генератор: генератор списка столбцов из 0*m является элементом для генератора списка строк


def initialize_edit_matrix(edit_matrix: tuple, add_weight: int,
                           remove_weight: int) -> list:
    res_list = list(edit_matrix)
    if type(add_weight) is not int or type(remove_weight) is not int:
        return res_list
    if len(res_list) == 0:
        return []
    for j in range(len(res_list[0])):  # заполняем первую строку по длине от 0 до значения len
        res_list[0][j] = j * add_weight
    for i in range(len(res_list)):
        if len(res_list[i]) == 0:  # проверяем, что i-я строка не пустая
            continue
        res_list[i][0] = i * remove_weight
    return res_list


def minimum_value(numbers: tuple) -> int:
    return min(numbers)


def fill_edit_matrix(edit_matrix: tuple,
                     add_weight: int,
                     remove_weight: int,
                     substitute_weight: int,
                     original_word: str,
                     target_word: str) -> list:
    minimum_value(edit_matrix)
    if type(original_word) is not str or type(target_word) is not str:
        return list(edit_matrix)
    if type(add_weight) is not int or type(remove_weight) is not int or type(substitute_weight) is not int:
        return list(edit_matrix)
    for i in range(len(edit_matrix)):
        for j in range(len(edit_matrix[0])):  # сколько элементов (столбцов в матрице) в первой строке
            if i == 0 or j == 0:
                continue
            first_option = edit_matrix[i - 1][j] + remove_weight
            second_option = edit_matrix[i][j - 1] + add_weight
            third_option = edit_matrix[i - 1][j - 1]
            if original_word[i - 1] != target_word[
                j - 1]:  # чтобы не выходить за границы массива; игнорим нулевую строку
                third_option += substitute_weight
            edit_matrix[i][j] = min(first_option, second_option, third_option)
    return list(edit_matrix)


def find_distance(original_word: str,
                  target_word: str,
                  add_weight: int,
                  remove_weight: int,
                  substitute_weight: int) -> int:
    if type(original_word) is not str or type(target_word) is not str:
        return -1
    if type(add_weight) is not int or type(remove_weight) is not int or type(substitute_weight) is not int:
        return -1
    matrix = tuple(generate_edit_matrix(len(original_word) + 1, len(target_word) + 1))
    matrix = tuple(initialize_edit_matrix(matrix, add_weight, remove_weight))
    matrix = fill_edit_matrix(matrix, add_weight, remove_weight, substitute_weight, original_word, target_word)
    return matrix[len(original_word)][len(target_word)]


def save_to_csv(edit_matrix: tuple, path_to_file: str) -> None:
    file = open(path_to_file, 'w')
    for line in edit_matrix:
        row = [str(i) for i in line]
        row = ','.join(row)
        file.write(row)
        file.write('/n')
    return None


def load_from_csv(path_to_file: str) -> list:
    text = []
    file = open(path_to_file, 'r')
    file = file.readlines()
    for line in file:
        row = []
        for i in line.split(','):
            row.append(i)
        text.append(row)
    return list(text)


def print_path(edit_matrix: tuple,
               original_word: str,
               target_word: str,
               add_weight: int,
               remove_weight: int,
               substitute_weight: int):
    reverse_path = describe_edits(edit_matrix, original_word, target_word, add_weight, remove_weight, substitute_weight)
    reverse_path.reverse()
    for item in reverse_path:
        print(item)


def describe_edits(edit_matrix: tuple,
                   original_word: str,
                   target_word: str,
                   add_weight: int,
                   remove_weight: int,
                   substitute_weight: int) -> list:
    edit_matrix = list(edit_matrix)
    current_i = len(original_word)  # начальные координаты
    current_j = len(target_word)
    res = []  # вывод инструкций
    while current_i != 0 or current_j != 0:  # пока не дойдем до старта
        if current_j > 0 and current_i > 0 and original_word[current_i - 1] == target_word[
            current_j - 1]:  # по диагонали бесплатно
            current_i -= 1
            current_j -= 1
            continue

        if current_j > 0 and current_i > 0 and edit_matrix[current_i][current_j] == edit_matrix[current_i - 1][
            current_j - 1] + substitute_weight:  # по диагонали за sub_weight
            res.append("substitute " + original_word[current_i - 1] + " with " + target_word[current_j - 1])
            current_i -= 1
            current_j -= 1
            continue

        if current_i > 0 and edit_matrix[current_i][current_j] == edit_matrix[current_i - 1][
            current_j] + remove_weight:  # движение вверх на 1 = удаление
            res.append("remove " + original_word[current_i - 1])
            current_i -= 1
            continue
        if current_j > 0 and edit_matrix[current_i][current_j] == edit_matrix[current_i][
            current_j - 1] + add_weight:  # движение влево
            res.append("insert " + target_word[current_j - 1])
            current_j -= 1
            continue
        print('incorrect matrix')
        return []

    return res
