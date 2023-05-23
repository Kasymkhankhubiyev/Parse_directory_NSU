import io
import sys

ru = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
en = 'abcdefghijklmnopqrstuvwxyz'


def incode(path: str, shift: int, language: str):
    lines = load_file(path).split('\n')

    output = ''
    for line in lines:
        _line = ''
        if len(line) > 0:
            _line += _encode_by_word(word=line, language=language, shift=shift) + ' '

        output += _line + '\n'

    print('перевод\n')
    print(output)
        

def load_file(path: str):
    with io.open(path, encoding='utf-8-sig', mode='r') as text_file:
        data = text_file.read()

    return data


def _encode_by_word(word: str, language: str, shift: int):
    result = ""
    if language == 'en':
        alphabet = en
    else: alphabet = ru 
    
    print(alphabet)
    for i in range(len(word)):
        char = word[i]
        if char.lower() in alphabet:
            if char.isupper():
                result += alphabet[abs((alphabet.index(char.lower()) + shift) % len(alphabet))].upper()
            else:
                result += alphabet[abs((alphabet.index(char) + shift) % len(alphabet))]
        else:
            result += char
    return result
    

if __name__ == "__main__":
    input = sys.argv[1:]
    print(input)
    incode(path=input[0], shift=int(input[1]), language=input[2])
