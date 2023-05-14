import os
import sys

from helper import is_file_sign, is_dir_sign, new_line, commands
# сообщение об ошибке
exception_message = 'Only directories'

# отступ первого элемента в каталоге
first_sign = '`-- '

# отступ второго элемента в каталоге
other_sign = '|-- '

# отступ для жлементова подкаталогов
subdir_sign = '|   '

# отступ для элементов подкаталога
delta = '    '

def is_path_to_file(path: str) -> None:
    """
    Функция проверяет указывает ли введенный адрес на директорию.
    Если указывает на директорию - вызываем исключение,
    иначе - ничего не делаем.

    Аргументы:
        path, string - путь к директории/файлу
    """
    if os.path.isfile(path):
        # бросаем исключение с ошибкой - выполнение сразу прерывается
        raise Exception(f'{exception_message}')
    
    
def pars_directory(path: str, deep: int, parent_is_first: bool) -> str:
    """
    В данной функции реализуем чтение и запись дерева каталога.
    
    Получаем путь к директории, получаем список содержимого этой директории.
    Пробегаемся по всем элементам.
    Если попадается файл - просто записываем файл.
    Если директория - рекурсивно проходим до конца ветви - конец ветви: пустая директория или
                      директория, содержащая только файлы.

    Аргументы:
        path, string - путь к директории
        deep, integer - глубина текущей ветви дерева
        parent_is_first, bool - указывает, является ли родительская 
            директория первой в своей директории. это нужно для того,
            чтобы правильно устанавливать отступы для элементов подкаталогов.

    Возвращаемое значение:
        dir_tree, str - дерево каталога в виде строки.
    
    """
    dir_tree = ''

    # получаем список файлов и каталогов внутри текущего каталога
    _dir_inner = os.listdir(path)

    # если директория пустая - конец, иначе нужно пробежаться
    if len(_dir_inner) != 0:

        # enumerate возвращается кортеж (пару значений): 
        # idx - индекс (порядковый номер) элемента массива и 
        # item - элемент массива соответствующий индексу
        for idx, item in enumerate(_dir_inner):
            line = ''

            # Если родительская директория не была первой в своем списке
            # нужно вдоль вертикали устанавливать отступ '|   '.
            if parent_is_first == False:
                line += '|   '

            # проверяем является ли элемент в списке файлом посредством функции: os.path.isfile(path),
            # если файл - возвращается True, иначе False
            # os.path.join(path, file) - конкатенирует путь и название файла.
            if os.path.isfile(os.path.join(path, item)):
                if idx == 0: # если первый в списке директории
                    if parent_is_first: # Если родительская директория тоже первая, ничего лишнего ставить не нужно
                        dir_tree += line + delta * deep + first_sign + item + is_file_sign + '\n'
                    else: # а если не первая то по уровню родительской вдоль вертикали надо спец отступ ставить
                        dir_tree += delta * (deep - 1) + line + first_sign + item + is_file_sign + '\n'
                else: # не первый в списке
                    if parent_is_first: # аналогично
                        dir_tree += delta * deep + line + other_sign + item + is_file_sign + '\n'
                    else:
                        dir_tree += delta * (deep - 1) + line + other_sign + item + is_file_sign + '\n'

            elif os.path.isdir(os.path.join(path, item)): # является ли директорией, как в случае с файлом
                if idx == 0: # если первый в списке директории
                    if parent_is_first: # если родительская директория тоже первая 
                        dir_tree += delta * deep + line + first_sign + item + is_dir_sign + '\n'
                        # идем глубже в директории
                        dir_tree += pars_directory(path=os.path.join(path, item), deep=deep+1, parent_is_first=True)
                    else: # директория не первая в списке
                        dir_tree += delta * (deep - 1) + line + first_sign + item + is_dir_sign + '\n'
                        
                        # идем глубже в директорию - не забываем установить 'parent_is_first=True', т.к. idx = 0
                        out = pars_directory(path=os.path.join(path, item), deep=deep+1, parent_is_first=True)

                        '''
                        т.к. текущая директория не первая, все последующие файлы/директории
                        должны быть помечены отступом с вертикальной чертой на уровне объявления директории

                        пример: 
                            Dir
                            `-- first_dir (d)
                            |-- second_dir (d)
                            |   `-- first_subdir (d)
                            |   |-- second_subdir (d)
                            |   |-- file (f)
                        '''
                        # разрезаем out на строки
                        lines = out.split('\n')
                        for line in lines:
                            if len(line) > 0: # пустую строку в конце надо выкинуть
                                dir_tree += line[:(deep-1)*4] + '|   ' + line[deep*4 - 1:] + '\n'
                else: # не первый в списке 
                    if parent_is_first:
                        dir_tree += delta * deep + line + other_sign + item + is_dir_sign + '\n'
                    else:
                        dir_tree += delta * (deep - 1) + line + other_sign + item + is_dir_sign + '\n'
                    dir_tree += pars_directory(path=os.path.join(path, item), deep=deep+1, parent_is_first=False)

    return dir_tree


def check_input(input: list) -> list:
    if input[0] in commands:
        raise Exception(f'Сначала введите название директории')
    if os.path.isfile(input[0]):
        raise Exception(f'{exception_message}')
    if len(input) > 0:
        for i in range(len(input[1:])):
            if input[i] not in commands:
                raise Exception(f'Неизвестная команда {input[i]}, \n досутпные команды: {commands}')
    return input


def main() -> None:

    # получаем данные из командной строки - берем только последний аргумнет
    try:
        input = check_input(sys.argv[1:])
    except Exception as e:
        raise Exception(e.args)

    output = ''
    
    output += input[0].split(sep='/')[-1] + '\n'

    output += pars_directory(input[0], 0, True)   

    print(output)


if __name__ == '__main__':
    main()
