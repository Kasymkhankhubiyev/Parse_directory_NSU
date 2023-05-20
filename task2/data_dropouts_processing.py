import pandas as pd
import numpy as np


MIN = 'min'
MAX = 'max'
MEAN = 'mean'
MEDIAN = 'median'


# надо передавать функцию
def _calc_IQR(data: pd.Series) -> float:
    """
    Функция рассчитывает разность между первой и третьей квантилями.

    Аргументы:
        data, pd.Series - столбец значений, для которого рассчитывается межквартильное расстояние.

    Возвращаемое значение:
        iqr, float - межквартильное расстояние
    """
    q75, q25 = np.percentile(data, [75 ,25])
    iqr = q75 - q25

    return iqr

def _replace_series(data: pd.Series, method: str, critical_value: float) -> pd.Series:
    """
    Функция определяет и заменяет выбросы в столбцах в соответсвии с указанными
    критической разностью с медианой и функцией замены выбросов.

    Аргументы:
        data, pd.Series - столбец значений, который нужн отредактировать
        method, str - метод замены выбросов, принимает значения:
                      'min' - замена минимальным значением из невыбросов,
                      'max' - замена максимальным значением из невыбросов,
                      'mean' - замена средним значением из невыбросов,
                      'median' - заполнение медианным значением из невыбросов.
        critical_value, float - максимальная величина отклонения от медианного значения, определяющая выброс.

    Возвращаемое значение:
        new_data, pd.Series - столбец без выбросов.
    """
    # получаем список значений в столбце
    targets = data.values

    # найдем индекс середины массива
    idx = int(np.floor(len(targets) / 2))

    # найдем медиану, для этого отсортируем список и возьмем значение в середине
    median = np.sort(targets)[idx]

    # проверим, есть ли вообще выбросы, если нет, то вернем тот же столбец
    if len(np.where(targets > median + critical_value)) == 0:
        return data

    # получим список не выбросов
    filtered = targets[np.where(targets < median + critical_value)]

    # теперь получим заменяющее значение в соответствии с заданным методом
    if method == MIN: # заменяем минимальным значение
        replace_value = np.min(filtered)
    elif method == MAX: # заменяем максимальным значением
        replace_value = np.max(filtered)
    elif method == MEAN: # заменяем средним значением
        replace_value = np.sum(filtered) / len(filtered)
    elif method == MEDIAN: # заменяем медианным значением
        replace_value = filtered[int(np.floor(len(filtered) / 2))]

    # если был интовый тип, надо таким и заменить
    if type(targets[0]) in [int, np.int32, np.int64]:
        replace_value = int(replace_value)
    
    # теперь заменим выбросы вычисленным значением в соответствии с заданным методом
    new_data = pd.Series(np.where(targets > median + critical_value, replace_value, targets))

    return new_data
    

def replace_dropouts(data: pd.DataFrame, method=MIN, critical_distance=None) -> pd.DataFrame:
    """
    Функция корректирует датафрейм, выявляя и заменяя выбросы значениями в 
    соответствии с выбранными критическим отклонением и методом.

    Аргументы:
        data, pd.DataFrame - датафрейм, который следует отредактировать
        method, str - метод замены выбросов, принимает значения:
                      'min' - замена минимальным значением из невыбросов,
                      'max' - замена максимальным значением из невыбросов,
                      'mean' - замена средним значением из невыбросов,
                      'median' - заполнение медианным значением из невыбросов.
        critical_distance - максимальное отклонение величины от медианы, больше 
                            которого значением считается выбросом

    Возвращаемое значение:
        new_data, pd.DataFrame - датафрейм без выбросов
    """
    # скопируем датафрейм, чтобы не испортить исходный
    new_data = data.copy()

    # пробедимся по столбцам
    for feature in new_data.columns[:-1]:

        # нас интересуют только числеенные характеристики
        if (new_data[feature].dtype != 'object'):
            # если критическое расстояние не задано, задаем одно межквартильное расстояние
            if critical_distance is None:
                critical_distance = _calc_IQR(new_data[feature])

            # сохраняем новые данные
            new_data[feature] = _replace_series(data=new_data[feature], method=method, critical_value=critical_distance)

    return new_data

            


            