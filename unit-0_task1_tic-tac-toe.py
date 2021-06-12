n = 3
def_value = '-'
# Генерируем поле
board = [[def_value for j in range(n)] for i in range(n)]


def draw(arr):
    """Функция выводит поле с ходом игры после каждого шага"""
    print('{:2}'.format(''), ''.join(['{:4}'.format(str(i)) for i, row in enumerate(arr)]))
    print('\n'.join(
        ['{:2} {}'.format(str(i), ''.join(['{:4}'.format(item) for item in row])) for i, row in enumerate(arr)]))
    print()


def play_game(token):
    """Функция для ввода хода игрока"""
    value = input('Ход игрока {} (введите через пробел номер строки и номер колонки): '.format(token))

    try:
        values = list(map(int, value.strip().split(' ')))
    except ValueError:
        print('Некорректный ввод. Введите два числа через пробел')
        return False

    if len(values) != 2:
        print('Некорректный ввод. Введите два числа через пробел')
        return False

    row = values[0]
    col = values[1]

    if not 0 <= row < n:
        print('Некорректный ввод. Номер строки должен быть от 0 до {}'.format(n - 1))
        return False

    if not 0 <= col < n:
        print('Некорректный ввод. Номер колонки должен быть от 0 до {}'.format(n - 1))
        return False

    if board[row][col] != def_value:
        print('Некорректный ввод. Ячейка уже занята.')
        return False

    board[row][col] = token

    return True


def check_winner(arr, token):
    """Функция проверки окончания игры и определения победителя"""
    columns = list(zip(*arr))

    for i, row in enumerate(arr):
        # проверка по горизонтали
        if row.count(token) == n:
            return True
        # проверка по веритикали
        elif columns[i].count(token) == n:
            return True
        # проверка по диогонали слева направо
        elif [arr[i][i] for i in range(len(arr))].count(token) == n:
            return True
        # проверка по диогонали справа налево
        elif [arr[i][-i - 1] for i in range(len(arr))].count(token) == n:
            return True

    return False


def start():
    """Функция запуска игры"""

    winner = None
    player1 = 'X'
    player2 = 'O'
    current_player = player2
    step = 0

    while winner is None:
        step += 1
        current_player = player1 if current_player == player2 else player2

        if not play_game(current_player):
            current_player = player1 if current_player == player2 else player2
            continue

        draw(board)

        if check_winner(board, current_player):
            winner = current_player
            break

        if step >= n ** 2:
            break

    if winner is not None:
        print('Game over. Победитель: игрок {}'.format(winner).upper())
    else:
        print('Game over. Ничья'.upper())


print()
print('Игра крестики-нолики'.upper())
print()
print('Правила игры:'.upper())
print('Игроки по очереди ставят на свободные клетки поля знаки (один всегда крестики, другой всегда нолики).')
print('Первый, выстроивший в ряд своих фигуры по вертикали, горизонтали или диагонали, выигрывает.')
print()

start()
