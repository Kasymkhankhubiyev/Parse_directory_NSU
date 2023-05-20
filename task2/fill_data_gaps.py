import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


MEAN = 'mean'
MEDIAN = 'median'
NEAREST_NEIGHBOR = 'nearest_neighbor'
MAX_LIKELIHOOD = 'max_likelihood'


def _find_nan_columns(data: pd.DataFrame) -> list:
    """
    Эта функция ищет колонки с пропущенными значениями и подсчитывает долю пропущенных значений.
    
    Аргументы:
        data, pd.DataFrame - кадр данных

    Возвращаемое значение:
        nan_columns, list[str, float] - список колонок с пустыми значениями в формате: [колонка, доля пропущенных]
    """
    # сохраним количество элементов в датафрейме
    fullsize = data.shape[0]
    nan_columns = []

    # создадим копию датафрейма, чтобы ничего не испортить
    new_train = data.copy()

    # пробежимся по всем колонкам
    for column in data.columns:
        # подсчитаем количество пустых значений
        nulls = new_train[column].isnull().sum()

        # нас интересуют только колонки, содержащие пропуски
        if nulls != 0:
            nan_columns.append([column, nulls / fullsize * 100])

    return nan_columns


def _label_numeric_encoder(data: pd.Series) -> pd.DataFrame:
    new_data = data.copy()
    unique_items = data.unique()
    data_values = np.array([data.values])
    unique_indexes = np.array([np.int32(i) for i in range(len(unique_items))])

    for i in range(len(data_values)):
        for idx, item in enumerate(unique_items):
            if new_data[i] is not None:
                if new_data[i] == item:
                    # new_data[i] = unique_indexes[np.where(unique_items == new_data[i])].flatten()
                    new_data[i] = unique_indexes[idx]

    return new_data


def convertToNumeric(data: pd.DataFrame) -> pd.DataFrame:
    new_data = data.copy()
    LE = LabelEncoder()
    for feature in new_data.columns[:-1]:
        if (new_data[feature].dtype == 'object'):
            new_data[feature] = LE.fit_transform(new_data[feature])
            # new_data[feature] = _label_numeric_encoder(new_data[feature])
    return new_data


def _fill_data_gaps_dist(data: pd.DataFrame, nan_columns: list) -> pd.DataFrame:
    """
    
    """
    df = data.copy()
    df = convertToNumeric(df)
    for i in range(len(nan_columns)):
        
        # начинаем обучать с колонки с наименьшим кол-вом пропущенных значений
        _df = df.copy()

        # выбрасываем колонки с пропущенными значениями: 
        # при этом уже обученные колонки не выбрасываем
        if i+1 != len(nan_columns[i:]):
            for column in nan_columns[i+1:]:
                # column имеет вид: ['название колонки', доля]
                _df = _df.drop(columns=column[0])

        # берем только строки без пропусков
        not_nan_df = _df[_df[nan_columns[i][0]].notnull()]

        # вытаскиваем значения непустих значений
        targets = not_nan_df[nan_columns[i][0]].values

        # выбрасываем текущую клонку
        samples = not_nan_df.drop(columns = nan_columns[i][0]).values
        # print(samples.shape)

        # нужно как в к-ближайших соседях сосчитать расстояние:
        def _calc_distances(XA, XB) -> np.array:
            distance = np.sqrt(np.sum((XA - XB)**2, axis=0))
            return np.array(distance)
        
        # теперь заполним значения
        # хотим только строки с пропусками, получаем список с обозначенными строками с пропусками
        rows = _df[nan_columns[i][0]].isnull()

        # пробегаемся по всем строкам с пропусками
        for k in range(len(rows)):
            if rows[k]:
                # находим ближайшего соседа
                minindex = np.argmin(_calc_distances(_df.drop(columns=nan_columns[i][0]).loc[k].values, samples))
                # подставляем
                df.loc[k, nan_columns[i][0]] = targets[minindex]
    return df


def _fill_data_gaps_mean(data: pd.DataFrame, nan_columns: list) -> pd.DataFrame:
    """
    
    """
    # скопируем кадр данных
    new_data = data.copy()

    # пробежимся по всем строкам с пропусками
    for i in range(len(nan_columns)):

        # берем только строки без пропусков
        not_nan_df = new_data[new_data[nan_columns[i][0]].notnull()]

        # вытаскиваем значения
        targets = not_nan_df[nan_columns[i][0]].values  # np.array

        if type(targets[0]) == str:
            # берем середину
            idx = int(np.floor(len(targets) / 2))
            mean = np.sort(targets)[idx]
        else:
            # рассчитаеем среднее арифметическое
            mean = np.sum(targets) / len(targets)

        # теперь заполним пропуски
        # для этого нам нужно пометить строки с пропусками
        rows = new_data[nan_columns[i][0]].isnull()
        for k in range(len(rows)):
            if rows[k]:
                new_data.loc[k, nan_columns[i][0]] = mean  

    return new_data


def _fill_data_gaps_median(data: pd.DataFrame, nan_columns: list) -> pd.DataFrame:
    pass


def _fill_data_gaps_max_likelihood(data: pd.DataFrame, nan_columns: list) -> pd.DataFrame:
    pass


def fill_data_gaps_nearest(data: pd.DataFrame) -> pd.DataFrame:
    return _fill_data_gaps_dist(data=data, nan_columns=_find_nan_columns(data))

def fill_data_gaps_mean(data: pd.DataFrame) -> pd.DataFrame:
    return _fill_data_gaps_mean(data=data, nan_columns=_find_nan_columns(data))

def fill_data_gaps_median(data: pd.DataFrame) -> pd.DataFrame:
    return _fill_data_gaps_median(data=data, nan_columns=_find_nan_columns(data))

def fill_data_gaps_max_likelihood(data: pd.DataFrame) -> pd.DataFrame:
    return _fill_data_gaps_max_likelihood(data=data, nan_columns=_find_nan_columns(data))

