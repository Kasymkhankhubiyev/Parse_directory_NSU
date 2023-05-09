import os
import sys

# сообщение об ошибке
exception_message = 'Only directories'
first_sign = '`-- '
other_sign = '|-- '
delta = '    '

def is_path_to_file(path: str) -> None:
    """
    Функция проверяет указывает ли введенный адрес на директорию.
    Если указывает на директорию - вызываем исключение,
    иначе - ничего не делаем.
    """
    if os.path.isfile(path):
        raise Exception(f'{exception_message}')
    
def pars_directory(path: str, deep: int, parent_is_first: bool) -> str:
    has_first = False
    out_put = ''

    _dir_inner = os.listdir(path)
    if len(_dir_inner) != 0:
        for item in _dir_inner:
            line = ''
            if parent_is_first == False:
                line += '|   '
            if os.path.isfile(os.path.join(path, item)):
                if has_first == False:
                    has_first = True
                    if parent_is_first:
                        out_put += line + delta * deep + first_sign + item + ' (f)' + '\n'
                    else:
                        out_put += delta * (deep - 1) + line + first_sign + item + ' (f)' + '\n'
                else:
                    if parent_is_first:
                        out_put += delta * deep + line + other_sign + item + ' (f)' + '\n'
                    else:
                        out_put += delta * (deep - 1) + line + other_sign + item + ' (f)' + '\n'
            elif os.path.isdir(os.path.join(path, item)):
                if has_first == False:
                    has_first = True
                    if parent_is_first:
                        out_put += delta * deep + line + first_sign + item + ' (d)' + '\n'
                        out_put += pars_directory(path=os.path.join(path, item), deep=deep+1, parent_is_first=True)
                    else:
                        out_put += delta * (deep - 1) + line + first_sign + item + ' (d)' + '\n'
                        
                        out = pars_directory(path=os.path.join(path, item), deep=deep+1, parent_is_first=True)
                        lines = out.split('\n')
                        for line in lines:
                            if len(line) > 0:
                                out_put += line[:(deep-1)*4] + '|   ' + line[deep*4 - 1:] + '\n'
                else:
                    if parent_is_first:
                        out_put += delta * deep + line + other_sign + item + '(d)' + '\n'
                    else:
                        out_put += delta * (deep - 1) + line + other_sign + item + '(d)' + '\n'
                    out_put += pars_directory(path=os.path.join(path, item), deep=deep+1, parent_is_first=False)

    return out_put

def main() -> None:

    # получаем данные из командной строки - берем только последний аргумнет
    path = sys.argv[-1]

    output = ''

    # проверяем на директуорию
    if os.path.isfile(path):
        raise Exception(f'{exception_message}')
    
    output += path.split(sep='/')[-1] + '\n'

    output += pars_directory(path, 0, True)   

    print(output)



if __name__ == '__main__':
    main()

