import os
import sys

from helper import is_file_sign, is_dir_sign, new_line, commands, file, directory
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

def add_info_by_flags(path: str, command_flags: dict) -> str:
    """
    Производим подстановку дополнительных данных в соответствии с введенными флагами.

    Аргументы:
        path, str - путь к файлу
        item, str - наименование файла
    """
    print(command_flags)
    add_str = ''
    if command_flags['-l']:
        if os.path.isfile(path):
            add_str += is_file_sign
        else: add_str += is_dir_sign
    
    if command_flags['-s']:
        add_str += f' {os.stat(path).st_size}'

    return add_str

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
    
def process_file(index: int, item:str, parent_is_first: bool, deep: int, line: str, path: str, command_flags: dict) -> str:
    """

    """
    output = ''
    if index == 0: # если первый в списке директории
        if parent_is_first: # Если родительская директория тоже первая, ничего лишнего ставить не нужно
            output += line + delta * deep + first_sign + item + add_info_by_flags(path=os.path.join(path, item),
                                                                                  command_flags=command_flags) + '\n'
        else: # а если не первая то по уровню родительской вдоль вертикали надо спец отступ ставить
            output += delta * (deep - 1) + line + first_sign + item + add_info_by_flags(path=os.path.join(path, item), 
                                                                                        command_flags=command_flags) + '\n'
    else: # не первый в списке
        if parent_is_first: # аналогично
            output += delta * deep + line + other_sign + item + add_info_by_flags(path=os.path.join(path, item),
                                                                                  command_flags=command_flags) + '\n'
        else:
            output += delta * (deep - 1) + line + other_sign + item + add_info_by_flags(path=os.path.join(path, item),
                                                                                        command_flags=command_flags) + '\n'

    return output


def process_directory(index: int, parent_is_first: bool, deep: int, item: str, path: str, 
                      line: str, command_flags: dict) -> str:
    """
    
    """
    output = ''
    if index == 0: # если первый в списке директории
        if parent_is_first: # если родительская директория тоже первая 
            output += delta * deep + line + first_sign + item + add_info_by_flags(path=os.path.join(path, item),
                                                                                  command_flags=command_flags) + '\n'
            # идем глубже в директории
            output += pars_directory(path=os.path.join(path, item), deep=deep+1, parent_is_first=True, command_flags=command_flags)
        else: # директория не первая в списке
            output += delta * (deep - 1) + line + first_sign + item + add_info_by_flags(path=os.path.join(path, item),
                                                                                  command_flags=command_flags) + '\n'
            
            # идем глубже в директорию - не забываем установить 'parent_is_first=True', т.к. idx = 0
            out = pars_directory(path=os.path.join(path, item), deep=deep+1, parent_is_first=True, command_flags=command_flags)

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
                    output += line[:(deep-1)*4] + '|   ' + line[deep*4 - 1:] + '\n'
    else: # не первый в списке 
        if parent_is_first:
            output += delta * deep + line + other_sign + item + add_info_by_flags(path=os.path.join(path, item),
                                                                                  command_flags=command_flags) + '\n'
        else:
            output += delta * (deep - 1) + line + other_sign + item + add_info_by_flags(path=os.path.join(path, item),
                                                                                  command_flags=command_flags) + '\n'
        output += pars_directory(path=os.path.join(path, item), deep=deep+1, parent_is_first=False, command_flags=command_flags)

    return output

    
    
def pars_directory(path: str, deep: int, parent_is_first: bool, command_flags: dict) -> str:
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
        commands_flags - dict(str, bool) - словарь флагов команд

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
                dir_tree += process_file(index=idx, item=item, parent_is_first=parent_is_first, deep=deep, line=line, 
                                         path=path, command_flags=command_flags)

            elif os.path.isdir(os.path.join(path, item)): # является ли директорией, как в случае с файлом
                dir_tree += process_directory(index=idx, parent_is_first=parent_is_first, deep=deep, item=item, 
                                              path=path, line=line, command_flags=command_flags)
                
    return dir_tree


def check_input(input: list, settings: dict) -> 'tuple(str, dict)':
    """
    Эта функция проверяет введенные данные.
    """
    if input[0] in commands:
        raise Exception(f'Сначала введите название директории')
    if os.path.isfile(input[0]):
        raise Exception(f'{exception_message}')
    if len(input) > 0:
        for i in range(1, len(input[1:])+1):
            if input[i] not in commands:
                raise Exception(f'Неизвестная команда {input[i]}, \n досутпные команды: {commands}')
            print(settings[input[i]])
            settings[input[i]] = True
    return input[0], settings


def main() -> None:

    # получаем данные из командной строки - берем только последний аргумнет
    input_commands = {}
    for command in commands:
        input_commands[command] = False

    try:
        path, input_commands = check_input(sys.argv[1:], input_commands)
    except Exception as e:
        raise Exception(e.args)

    output = ''
    
    output += path.split(sep='/')[-1] + '\n'

    output += pars_directory(path, 0, True, input_commands)   

    print(output)


if __name__ == '__main__':
    main()
