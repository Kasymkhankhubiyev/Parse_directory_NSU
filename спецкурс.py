#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def pascal_triangle(n):
    if n <= 0:
        return []
    triangle = [[1]]
    if n == 1:
        return ['1']
    for i in range(1, n):
        prev_row = triangle[i - 1]
        cur_row = [1]
        for j in range(1, i):
            cur_row.append(prev_row[j - 1] + prev_row[j])
        cur_row.append(1)
        triangle.append(cur_row)
        return triangle
    

while True:
    try:
        n = int(input("Введите число строк для генерации треугольника Паскаля: "))
        if n <= 0:
            print("Число строк должно быть положительным.")
            continue
        break
    except ValueError:
        print("Введите целое число.")
triangle = pascal_triangle(n)

for row in triangle:
    print(' '.join([str(elem) for elem in row]))


# In[ ]:
def check_input(input: str) -> bool:
    if input.isdigit() and '.' not in input and int(input) > 0:
        return True
    return False

while True:
    try:
        n = input('Введите число n: ')
        if not check_input(n):
            raise ValueError()
    except ValueError:
        print('Вы ввели невалидное значение. Попробуйте еще раз.')
        continue
    
    n = int(n)
    rows = []
    for i in range(n):
        rows.append([1] * (i+1))
        for j in range(1, i):
            rows[i][j] = rows[i-1][j-1] + rows[i-1][j]
    
    for row in rows:
        print(*row)
    
    break  # выход из бесконечного цикла


# In[ ]:


def is_balanced(s):
    stack = []
    for c in s:
        if c in "([{":
            stack.append(c)
        elif c in ")]}":
            if not stack:
                return False
            if c == ")" and stack[-1] == "(" or c == "]" and stack[-1] == "[" or c == "}" and stack[-1] == "{":
                stack.pop()
            else:
                return False
    return not stack

s = input("Введите скобочную последовательность: ")
if is_balanced(s):
    print("Скобочная последовательность правильная.")
else:
    print("Скобочная последовательность неправильная.")


# In[ ]:




