"""
В этом пакете реализованы стратегии заполнения пропусков.

Заполнять пропущенные значения тем, что понравится на угад - не лучшая стратегия, 
часто применяют статистику для вычисления более-менее подходящего значения.

1. Самый простой и интуитивный способ - заполнить средним арифметическим значением колонки. 
Это не изменит среднее значение по всем значениям колонки.

2. Но иногда попадаются выбросы, поэтому, чтобы сделать вычисление среднего более робастным, 
можно брать усеченное среднее - сортируем значения в колонке, 
отбрасываем n штук слева и n штук справа и считаем среднее арифметическое.

3.Медианное среднее - медиана это точка ровно по середине выборки - сортируем значения колонки и тыкаем в середку. 
Такое среднее более устойчиво к выбросам, чем среднее арифметическое.

4. Наиболее часто встрчаемое - еще одна стратегия для заполнения - если чаще всего встречается - почему бы и нет.

5. Когда находим пропуск, можно искать наиболее похожую строку в датасете и заполнить этим значением. 
Близость можно определить расстоянием в пространстве значений, например евклидово расстояние или косинусное расстояние.

6. Maximum Likelihood (ML) метод крутая техника для восстановления истинных параметров популяции/населения.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


MEAN = 'mean'
MEDIAN = 'median'
NEAREST_NEIGHBOR = 'nearest_neighbor'
MAX_LIKELIHOOD = 'max_likelihood'
MOST_FREQUENT = 'most_frequent'


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


def convertToNumeric(data: pd.DataFrame) -> pd.DataFrame:
    """
    Функция конвертирует качественные характеристики в числовые.

    применяется LabelEncoder из библиотеки cikit-learn

    кодировка осуществляется следующим образом:
        получаем список уникальных значений и каждому уникальному значению 
        присваивается уникальный номер.

    Аргументы:
        data, pd.DataFrame - датафрейм, над которым необходимо произвести преобразования

    Возвращаемое значение:
        new_data, pd.DataFrame - датафрейм только с числовыми признаками
    """
    # копируем датафрейм, чтобы не испортить исходный
    new_data = data.copy()

    # инициализируем инкодер
    LE = LabelEncoder()

    # пробежимся по столбцам
    for feature in new_data.columns[:-1]:
        # интересуют только качественные признаки
        if (new_data[feature].dtype == 'object'):
            # заменяем столбец
            new_data[feature] = LE.fit_transform(new_data[feature])
            # new_data[feature] = _label_numeric_encoder(new_data[feature])
    return new_data


def _fill_data_gaps_dist(data: pd.DataFrame, nan_columns: list) -> pd.DataFrame:
    """
    Функция заполняет пустые значения данных наиболее ближайшим значением.

    Расстояние рассчитывается как евклидово расстояние и ближайший определяется 
    минимумом расстояния до элемента.

    Если попадаются качественные признаки, кодируем их в числовые признаки.

    Сначала удаляются все столбцы с пропусками (заполненные ранее не удаляются),
    вытаскиваем только строки без пропусков и по ним заполняем пропуски.

    Расстояние рассчитывается так:
        :math:  `distance = \sum(x^a_i - x^b_i)` , 
            где x^a_i - элемент из выборки с пропущенными значениями,
                x^b_i - элемент из выборки с без пропущенныч значений,

    Аргументы: 
        data, pd.DataFrame - датафрейм, в котором нужно заполнить пропуски
        nan_columns - список заголовков столбцов, содержащих пропуски

    Возвращаемое значение:
        new_data, pd.DataFrame - датафрейм с заполненными пропусками
    """
    # создаем копию датасета
    df = data.copy()
    
    # конвертируе все качественные характеристики в числовые
    df = convertToNumeric(df)

    # пробежимся по всем пустым колонкам
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
    Функция заполняет пустые значения данных средним значением в столбце,
    такой подход не изменяется среднего значения в датасете.

    Если попадаются качественные признаки - заполняем медианным значением

    Сначала удаляются все столбцы с пропусками (заполненные ранее не удаляются),
    вытаскиваем только строки без пропусков и по ним заполняем пропуски.

    Аргументы: 
        data, pd.DataFrame - датафрейм, в котором нужно заполнить пропуски
        nan_columns - список заголовков столбцов, содержащих пропуски

    Возвращаемое значение:
        new_data, pd.DataFrame - датафрейм с заполненными пропусками
    """
    # скопируем кадр данных
    new_data = data.copy()

    # пробежимся по всем строкам с пропусками
    for i in range(len(nan_columns)):

        # берем только строки без пропусков
        not_nan_df = new_data[new_data[nan_columns[i][0]].notnull()]

        # вытаскиваем значения
        targets = not_nan_df[nan_columns[i][0]].values  # np.array

        # если это качественные характеристики, просто заменяем медианным.
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
    """
    Функция заполняет пустые значения данных медианным значением.

    Сначала удаляются все столбцы с пропусками (заполненные ранее не удаляются),
    вытаскиваем только строки без пропусков и по ним заполняем пропуски.

    Аргументы: 
        data, pd.DataFrame - датафрейм, в котором нужно заполнить пропуски
        nan_columns - список заголовков столбцов, содержащих пропуски

    Возвращаемое значение:
        new_data, pd.DataFrame - датафрейм с заполненными пропусками
    """
    # скопируем кадр данных
    new_data = data.copy()

    # пробежимся по всем строкам с пропусками
    for i in range(len(nan_columns)):

        # берем только строки без пропусков
        not_nan_df = new_data[new_data[nan_columns[i][0]].notnull()]

        # вытаскиваем значения
        targets = not_nan_df[nan_columns[i][0]].values  # np.array

        # берем середину
        idx = int(np.floor(len(targets) / 2))
        mean = np.sort(targets)[idx]

        # теперь заполним пропуски
        # для этого нам нужно пометить строки с пропусками
        rows = new_data[nan_columns[i][0]].isnull()
        for k in range(len(rows)):
            if rows[k]:
                new_data.loc[k, nan_columns[i][0]] = mean  

    return new_data


def _fill_data_gaps_most_frequent(data: pd.DataFrame, nan_columns: list) -> pd.DataFrame:
    """
    Функция заполняет пустые значения данных на основе статистических данных,
    т.е. ведется подсчет наиболее часто встречаемого и этим значением заполняются пропуски.

    Такой подход применяется, например, в CatBoost от Yandex при обработке пропусков.
    Мы в данной работе применим простой метод заполнения статистическим значением.

    Сначала удаляются все столбцы с пропусками (заполненные ранее не удаляются),
    вытаскиваем только строки без пропусков, подсчитываются вхождения всех уникальных значений,
    берется наиболее часто встречаемое и заполняется пропуск.


    Аргументы: 
        data, pd.DataFrame - датафрейм, в котором нужно заполнить пропуски
        nan_columns - список заголовков столбцов, содержащих пропуски

    Возвращаемое значение:
        new_data, pd.DataFrame - датафрейм с заполненными пропусками
    """
    # скопируем кадр данных
    new_data = data.copy()

    # пробежимся по всем строкам с пропусками
    for i in range(len(nan_columns)):

        # берем только строки без пропусков
        not_nan_df = new_data[new_data[nan_columns[i][0]].notnull()]

        # вытаскиваем значения
        targets = not_nan_df[nan_columns[i][0]].values  # np.array

        # получим подсчет количества вхождений каждого уникального значения
        appearance = not_nan_df[nan_columns[i][0]].value_counts()

        most_frequent = appearance[np.argmax(appearance.values)]

        # теперь заполним пропуски
        # для этого нам нужно пометить строки с пропусками
        rows = new_data[nan_columns[i][0]].isnull()
        for k in range(len(rows)):
            if rows[k]:
                new_data.loc[k, nan_columns[i][0]] = most_frequent 

    return new_data


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

def fill_data_gaps_most_frequent(data: pd.DataFrame) -> pd.DataFrame:
    return _fill_data_gaps_most_frequent(data=data, nan_columns=_find_nan_columns(data))


#### TODO: needs fixes

def _label_numeric_encoder(data: pd.Series) -> pd.Series:
    """
    Инкодер строковых значений в числовое

    Аргументы:
        data, pd.Series - столбец, над которым нуобходимо произвести преобразования

    Возвращаемое значение
        new_data, pd.Series - столбец с измененными значениями
    """
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

