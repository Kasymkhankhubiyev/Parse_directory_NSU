"""
В данном приложении реализован конвейер, обрабатывающий данные из csv

взаимодействие осуществляется через функцию data_cleaner(*args), на вход которой подается путь к файлу.

Осуществляются следующие этапы:

    1. Чтение файла и загрузга кадра данных
    2. Удаление дубликатов 
    3. Обработка пропущенных значений
    4. Обработка выбросов
    5. Сохранение обработанных данных по указаному адресу.

"""
import pandas as pd 
import numpy as np
import os


from fill_data_gaps import fill_data_gaps_mean, fill_data_gaps_median, fill_data_gaps_nearest, fill_data_gaps_max_likelihood
from fill_data_gaps import MEAN, MEDIAN, NEAREST_NEIGHBOR, MAX_LIKELIHOOD

from data_dropouts_processing import MAX, MIN, replace_dropouts
    

def delete_NaN(data: pd.DataFrame, critical_value: float) -> pd.DataFrame:
    """
    Функция реализует удаление столбцов, количеством пропущенных значений
    в которых превышает заданное максимальное значение.

    Столбцы с большим количеством пропусков не информативны и лишь только испортят работу.

    Аргументы:
        data, pd.DataFrame - кадр данных, который нужно очистить от неиформативных столбцов.
        critical_value, float - величина критической доли пропущенных значений от количества строк.

    Возвращаемое значение:
        new_data, pd.DataFrame - кадр данных без неинформативных столбцов.
    """
    # скопируем датафрейм, чтобы не навредить исходным данным
    new_data = data.copy()

    # получаем список заголовком столбцов
    columns = new_data.columns

    # пробежимся во всем столбцам
    for column in columns:
        # посчитаем количество пустых значений для текущего столбца
        nulls = new_data[column].isnull().sum()

        # расчитаем долю пропущенных значений
        ratio = nulls / new_data.shape[0]

        # если доля пропущенных значений больше критического значения
        # столбец не информативен - выбрасываем его
        if ratio > critical_value:
            new_data = new_data.drop(columns = column)
    
    return new_data


def fill_gaps(data: pd.DataFrame, method=MEAN):
    """
    Функция - коммутатор. Вызывает нужную функцию из пакета fill_data_gaps.py в
    соответствии с указанным методом заполнения пропущенных значений.

    Аргументы:
        data, pd.DataFrame - датафрейм, в котором нужно заполнить пропуски.
        method, str - метод заполнения пропущенных значений, принимает начения:
                        'mean' - заполнение средним значением,
                        'median' - заполнение медианным значением,
                        'nearest_neighbor' - ближайшее значение,
                        'max_likelihood' - заполнение методом максимизации функции правдоподобия (в разработке)
    """
    if method == MEAN:
        return fill_data_gaps_mean(data)
    elif method == MEDIAN:
        return fill_data_gaps_median(data)
    elif method == NEAREST_NEIGHBOR:
        return fill_data_gaps_nearest(data)
    elif method == MAX_LIKELIHOOD:
        return fill_data_gaps_max_likelihood(data)


def data_cleaner(data=None, data_path=None, column_drop_critical_value=0.25, fill_gaps_method=MEAN, dropout_method=MIN, 
                 dropout_critical_difference=None, save_path='/cleaned_dataframe', save_file_name='out.csv'):
    """
    Функция - конвейер очистки данных.

    Реализует следуюшщие этапы:
        1. Чтение файла и загрузга кадра данных
        2. Удаление дубликатов 
        3. Обработка пропущенных значений
        4. Обработка выбросов
        5. Сохранение обработанных данных по указаному адресу.

    Аргументы:
        data, pd.DataFrame - датафрейм, который нужно обработать
        data_path, str - путь к файлу для чтения в формате csv
        column_drop_critical_value, float - критическое значение доли пропущенных значений в столбце,
                                            чтобы исключить столбец, 
                                            принимает значение от 0 до 1.
        fill_gaps_method, str - метод заполнения пропущенных значений, принимает следующие значения:
                                'mean' - заполнение средним значением,
                                'median' - заполнение медианным значением,
                                'nearest_neighbor' - ближайшее значение,
                                'max_likelihood' - заполнение методом максимизации функции правдоподобия (в разработке).
        dropout_method, str - метод замены выбросов, принимает следующие значения:
                              'min' - замена минимальным значением из невыбросов,
                              'max' - замена максимальным значением из невыбросов,
                              'mean' - замена средним значением из невыбросов,
                              'median' - заполнение медианным значением из невыбросов.
        dropout_critical_difference, float - максимальная величина отклонения от медианного значения, определяющая выброс.

    Возвращаемое значение:
        dataframe, pd.DataFrame - датафрейм очищенный.

    """

    if data is None and data_path is not None:
    # читаем данные
        data = pd.read_csv(data_path)
    elif data is None and data_path is None:
        raise Exception('Введите либо датафрейм или путь к файлу с данными')

    dataframe = data
    # выбрасываем дубликаты
    dataframe = dataframe.drop_duplicates()

    # удаление неинформативных строк
    dataframe = delete_NaN(data=dataframe, critical_value=column_drop_critical_value)

    # обработка пропущенных значений
    dataframe = fill_gaps(data=dataframe, method=fill_gaps_method)

    # обработка выбросов
    dataframe = replace_dropouts(data=dataframe, method=dropout_method, critical_distance=dropout_critical_difference)
    
    # создаем каталог, если существует, ничего не произойдет 
    os.makedirs(save_path, exist_ok=True)  

    # загружаем в файл
    dataframe.to_csv(save_path + '/' + save_file_name)  
    return dataframe



## TODO: needs further fixing

def remove_duplicates(data: pd.DataFrame, method: str, keep='first') -> list:
    """
    methods = ['grid', 'fast]

    keep = ['first', 'last', False]
    """
    """
    O(n^2)
    """
    new_data = pd.DataFrame(columns=data.columns)
    if method == 'grid':
        for i in range(data.shape[0]):
            if i == 0:
                new_data = pd.concat([new_data, data.iloc[[i]]])
            else:
                equality = 0
                is_equal = False
                for j in range(i, new_data.shape[0]):
                    for column in data.columns:
                        if data.iloc[i][column] == new_data.iloc[j][column]:
                            equality += 1
                    if equality == len(data.shape[-1]):
                        is_equal = True
                        break
                if is_equal == False:
                    new_data = pd.concat([new_data, data.iloc[[i]]])

        return new_data

