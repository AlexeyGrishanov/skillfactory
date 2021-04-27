import numpy as np


def score_game(game_core):
    # Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы эксперимент был воспроизводим!
    random_array = np.random.randint(1, 101, size=1000)
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return score


def game_core_bisection(number):
    """Сначала устанавливаем любое random число, а потом применяем метод Бисекции для угадывания числа.
       Функция принимает загаданное число и возвращает число попыток"""
    count = 1
    min_value = 1
    max_value = 101
    predict = np.random.randint(min_value, max_value)
    while number != predict:
        count += 1

        if number > predict:
            min_value = predict
        elif number < predict:
            max_value = predict

        predict = int((max_value+min_value)/2)

    return count


score_game(game_core_bisection)
