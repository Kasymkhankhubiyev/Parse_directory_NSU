import pandas as pd 
import numpy as np


from fill_data_gaps import fill_data_gaps_mean, fill_data_gaps_median, fill_data_gaps_nearest, fill_data_gaps_max_likelihood
from fill_data_gaps import MEAN, MEDIAN, NEAREST_NEIGHBOR, MAX_LIKELIHOOD


def prepare_dataset(data_frame: pd.DataFrame) -> list:
    """
    
    """

    # коныертируем в словарь с элементами в виде списка
    data_dict = data_frame.to_dict(orient='list')

    # получаем ключи и ковертируем в список
    keys = list(data_dict.keys())

    # запомним количество строк
    rows = len(data_dict[keys[0]])

    data_list = []

    for row in range(rows):
        data_item = []
        for key in keys:
            data_item.append(data_dict[key][row])
        data_list.append(data_item)

    return data_list


def _randomize_index(dataset_length: int):
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

    new_data_frame = data.copy()

    for i in range(duplicates_num):
        idx = _randomize_index(data.shape[0])
        separator = _randomize_index(new_data_frame.shape[0])

        data_sample = data.iloc[[idx]]
        new_data_frame = pd.concat([new_data_frame.iloc[:separator], data_sample, new_data_frame[separator:]])

    return new_data_frame
    

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
    

def delete_NaN(data: pd.DataFrame, critical_value: float) -> pd.DataFrame:
    """
    
    """
    new_data = data.copy()
    columns = new_data.columns
    # пробежимся во всем столбцам
    for column in columns:
        # посчитаем количество пустых значений для текущего столбца
        nulls = new_data[column].isnull().sum()
        ratio = nulls / new_data.shape[0]
        # если доля пропущенных значений больше критического значения
        # столбец не информативен - выбрасываем его
        if ratio > critical_value:
            new_data = new_data.drop(columns = column)
    
    return new_data


def fill_gaps(data: pd.DataFrame, method=MEAN):
    if method == MEAN:
        return fill_data_gaps_mean(data)
    elif method == MEDIAN:
        return fill_data_gaps_median(data)
    elif method == NEAREST_NEIGHBOR:
        return fill_data_gaps_nearest(data)
    elif method == MAX_LIKELIHOOD:
        return fill_data_gaps_max_likelihood(data)


def data_cleaner(data: pd.DataFrame, column_drop_critical_value=0.25, fill_gaps_method=MEAN):
    # создадим копию дата-кадра
    new_dataframe = data.copy()

    # выбрасываем дубликаты
    new_dataframe = new_dataframe.drop_duplicates()

    # удаление неинформативных строк
    new_dataframe = delete_NaN(data=new_dataframe, critical_value=column_drop_critical_value)

    # обработка пропущенных значений
    new_dataframe = fill_gaps(data=new_dataframe, method=fill_gaps_method)

    # обработка выбросов
    

    return new_dataframe