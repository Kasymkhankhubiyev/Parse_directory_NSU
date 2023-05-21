import pandas as pd
import numpy as np
import os  


MIN = 'min'
MAX = 'max'
MEAN = 'mean'
MEDIAN = 'median'


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


def _fill_data_gaps(data: pd.DataFrame, nan_columns: list) -> pd.DataFrame:
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


def _delete_NaN(data: pd.DataFrame, critical_value: float) -> pd.DataFrame:
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


def data_cleaner(data=None, data_path=None, column_drop_critical_value=0.25, dropout_method=MIN, 
                 dropout_critical_difference=None, save_path='/cleaned_data', save_file_name='/out.scv', save_to_file=None):
    """
    Функция - конвейер очистки данных. сохраняется 

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
        dropout_method, str - метод замены выбросов, принимает следующие значения:
                              'min' - замена минимальным значением из невыбросов,
                              'max' - замена максимальным значением из невыбросов,
                              'mean' - замена средним значением из невыбросов,
                              'median' - заполнение медианным значением из невыбросов.
        dropout_critical_difference, float - максимальная величина отклонения от медианного значения, определяющая выброс.
        sava_path, str - путь к директории в которую нужно выгрузить новый датафрейм

    Возвращаемое значение:
        dataframe, pd.DataFrame - датафрейм очищенный.

    """

    # если не передали датафрейм, то читаем из директории
    if data is None and data_path is not None:
    # читаем данные
        try:
            data = pd.read_csv(data_path)
        except:
            raise Exception('Ошибка при чтении файла, проверьте путь к файлу.')
    elif data is None and data_path is None:
        # если ничего не передали выдаем ошибку
        raise Exception('Введите либо датафрейм или путь к файлу с данными.')

    dataframe = data
    # выбрасываем дубликаты
    dataframe = dataframe.drop_duplicates()

    # удаление неинформативных строк
    dataframe = _delete_NaN(data=dataframe, critical_value=column_drop_critical_value)

    # обработка пропущенных значений
    dataframe = _fill_data_gaps(data=dataframe, nan_columns=_find_nan_columns(dataframe))

    # обработка выбросов
    dataframe = replace_dropouts(data=dataframe, method=dropout_method, critical_distance=dropout_critical_difference)
    
    # создаем каталог, если существует, ничего не произойдет 
    os.makedirs(save_path, exist_ok=True)  

    # загружаем в файл
    dataframe.to_csv(save_path + save_file_name)  

    return dataframe



if __name__ == '__main__':
    pass