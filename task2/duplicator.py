import numpy as np
import pandas as pd


def _randomize_index(dataset_length: int):
    """
    Реализуем генерацию случайных индексов и разделителя для
    вставки дубликатов.

    Аргументы:
        dataset_length, int - размер датасета
    """

    power = int(np.floor(np.log10(dataset_length)))
    # print(powers)
    idx = 0
    if power % 2 == 0:
        for i in range(power // 2):
            # if (i + 1) * 2 == power:
            #     randint = np.abs(dataset_length % 10 ** ((i + 1) * 2))
            # else: randint = 101
            idx += 10 ** (i * 2) * np.random.randint(101)
        idx += 10 ** (power-1) * np.random.randint(dataset_length // 10 ** (power-1))
    else:
        for i in range(power // 2):
            idx += 10 ** (i * 2) * np.random.randint(101)
        idx += 10 ** (power-1) * np.random.randint(dataset_length // 10 ** (power-1))

    if idx > dataset_length:
        return dataset_length - 1
    else: return idx


def add_duplicates_randomly(data: pd.DataFrame, duplicates_num: int) -> pd.DataFrame:
    """
    Функция рандомно вставляет дупликаты рандомно выбранных элементов.

    Аргументы:
        data, pd.DataFrame - датафрейм, в который нужно вставить дубликаты
        duplicates_num, int - количество дубликатов, которые нужно вставить

    Возвращаемое значение:
        new_data_frame, pd.DataFrame - новый датафрейм с дубликатами.
    """

    new_data_frame = data.copy()

    for i in range(duplicates_num):
        idx = _randomize_index(data.shape[0])
        separator = _randomize_index(new_data_frame.shape[0])

        data_sample = data.iloc[[idx]]
        new_data_frame = pd.concat([new_data_frame.iloc[:separator], data_sample, new_data_frame[separator:]])

    return new_data_frame