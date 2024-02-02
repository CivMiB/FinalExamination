import ast
import time
import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Устанавливаем параметры окна
        width = 500  # ширина окна
        height = 400  # высота окна
        # вычисляем координаты начала окна относительно максимальной длины и ширины экрана
        x = int((self.winfo_screenwidth() - width) / 2)
        y = int((self.winfo_screenheight() - height) / 2)
        # Задаём геометрию окна
        self.wm_geometry("%dx%d+%d+%d" % (width, height, x, y))
        # Устанавливаем название окна
        self.title('Сортировщик чисел')
        # Делаем размеры окна неизменяемыми
        self.resizable(0, 0)
        # Вызываем функцию установки дочерних фреймов на это окно
        self.put_frames()

    # Создаём фреймы основного окна
    def put_frames(self):
        self.main_panel = MainPanel(self)
        self.test_panel = TestPanel(self)


class MainPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Указываем размещение нашего фрейма на главном окне
        self.place(x=0, y=0, width=500, height=280)
        # Конфигурируем сетку
        self.columnconfigure((0), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, uniform='a')
        # Создаём рамку этого фрейма
        self['bd'] = 1
        self['relief'] = 'solid'
        # Вызываем функцию установки виджетов на это окно
        self.put_widgets()

    def put_widgets(self):
        self.sort_method_index = 0
        self.time_to_sort = 0
        self.sort_method = ('Пузырьковая сортировка (Bubble Sort)',
                            'Сортировка выбором (Selection Sort)',
                            'Сортировка вставками (Insertion Sort)',
                            'Сортировка слиянием (Merge Sort)',
                            'Быстрая сортировка (Quick Sort)')
        # Выводим информационную строку
        self.label1 = ttk.Label(self, text='Введите последовательность чисел через запятую:', foreground='black',
                                font=("Arial", 12))
        self.label1.grid(row=0, column=0, sticky='s')
        # Выводим виджет Entry для ввода последовательности чисел
        self.entry_val = ttk.Entry(self, justify='center', font=("Arial", 12))
        self.entry_val.insert(0, 'Например: 1,53,-5,44.12,93')
        self.entry_val.grid(row=1, column=0, sticky='nswe', padx=15)
        # Создаём виджет со списком
        self.var = tk.StringVar()
        self.combobox = ttk.Combobox(self, textvariable=self.var, font=("Arial", 11))
        self.combobox['values'] = self.sort_method
        self.combobox['state'] = 'readonly'
        self.combobox.current(0)
        self.combobox.grid(row=2, column=0, sticky='nswe', padx=100, pady=3)
        # Устанавливаем трассировку для данной переменной
        self.var.trace('w', self.callback)
        # Создаём кнопку старта сортировки
        self.button = tk.Button(self, text='СТАРТ', background='#006600', foreground='white', command=self.start_sort,
                                width=20, font=("Arial", 12))
        self.button.grid(row=3, column=0, sticky='ns')
        # Выводим информационную строку
        self.label2 = ttk.Label(self, text='Результат:', font=("Arial", 12))
        self.label2.grid(row=4, column=0, sticky='s')
        # Выводим информационную строку
        self.label3 = ttk.Label(self, text='', font=("Arial", 12), anchor='c', background='#FFFFFF',
                                borderwidth=2, relief="solid", wraplength=480)
        self.label3.grid(row=5, column=0, sticky='nswe', padx=15, pady=5, rowspan=2)
        self.label4 = ttk.Label(self, text='Время затраченное на сортировку:', font=("Arial", 12))
        self.label4.grid(row=7, column=0, sticky='s')
        self.label5 = ttk.Label(self, text=f'{self.time_to_sort} мс', font=("Arial", 12))
        self.label5.grid(row=8, column=0, sticky='n')

    def callback(self, *args):  # Функция обработки виджета со списком
        self.sort_method_index = self.combobox.current()

    def start_sort(self):  # Функция сортировки
        self.str = self.entry_val.get()  # Определяем переменной self.str значение поля entry
        # Проверяем на правильность ввода
        if len(self.str) < 100:  # Задаём максимальную длину строки для последовательности
            # Проверяем на правильность ввода
            try:
                # Используем модуль ast для преобразования строки с запятыми в список чисел
                self.new_list = list(ast.literal_eval(self.str))
            except:
                self.label1.config(text='Неверный ввод, попробуйте ещё раз', foreground='red')
                return
        else:
            self.label1.config(text='Слишком длинная последовательность, попробуйте ещё раз', foreground='red')
            return

        self.start_time = time.perf_counter()  # Засекам начальное время выполнения функции сортировки
        if self.sort_method_index == 0:
            self.sorted_list = bubble_sort(self.new_list)
        if self.sort_method_index == 1:
            self.sorted_list = selection_sort(self.new_list)
        if self.sort_method_index == 2:
            self.sorted_list = insertion_sort(self.new_list)
        if self.sort_method_index == 3:
            self.sorted_list = merge_sort(self.new_list)
        if self.sort_method_index == 4:
            self.sorted_list = bubble_sort(self.new_list)
        self.end_time = time.perf_counter()  # Засекам конечное время выполнения функции сортировки
        # Вычисляем время выполнения функции сортировки
        self.time_to_sort = (self.end_time - self.start_time) * 1000
        self.label1.config(text='Введите последовательность чисел через запятую:', foreground='black')
        self.label3.config(text=str(self.sorted_list)[1:-1])  # Выводим полученный список, исключая квадратные скобки
        self.label5.config(text=f'{self.time_to_sort} мс')  # Выводим время выполнения


class TestPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Указываем размещение нашего фрейма на главном окне
        self.place(x=0, y=280, width=500, height=120)
        # Конфигурируем сетку
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        # Создаём рамку этого фрейма
        self['bd'] = 1
        self['relief'] = 'solid'
        # Вызываем функцию установки виджетов на это окно
        self.put_widgets()

    def put_widgets(self):
        # Выводим информационную строку
        self.label1 = ttk.Label(self, text='Тестирование логики программы стандартными библиотеками',
                                font=("Arial", 12))
        self.label1.grid(row=0, column=0, columnspan=3, sticky='s')
        # Создаём кнопку старта тестирования
        self.button = tk.Button(self, text='Запустить тест', background='#9999FF', foreground='white',
                                command=self.start_test, width=20, font=("Arial", 12))
        self.button.grid(row=1, column=0, columnspan=3, sticky='ns')
        # Выводим информационную строку
        self.label2 = ttk.Label(self, text='Результат:', font=("Arial", 12))
        self.label2.grid(row=2, column=0, columnspan=3, sticky='s')

    def start_test(self):
        self.start_all_test([1, 4, 2], [1, 2, 4])
        self.label3 = ttk.Label(self, text='Тест №1 пройден', background='#99FF99',
                                anchor='c', font=("Arial", 10))
        self.label3.grid(row=3, column=0, sticky='nswe', padx=5, pady=5)

        self.start_all_test([-44, 1323.55, 22, 99], [-44, 22, 99, 1323.55])
        self.label3 = ttk.Label(self, text='Тест №2 пройден', background='#99FF99',
                                anchor='c', font=("Arial", 10))
        self.label3.grid(row=3, column=1, sticky='nswe', padx=5, pady=5)

        self.start_all_test([-325, 1.22, -99], [-325, -99, 1.22])
        self.label3 = ttk.Label(self, text='Тест №3 пройден', background='#99FF99',
                                anchor='c', font=("Arial", 10))
        self.label3.grid(row=3, column=2, sticky='nswe', padx=5, pady=5)

    def start_all_test(self, list_in, list_out):  # Функция тестирования всеми видами сортировок
        assert (bubble_sort(list_in)) == list_out
        assert (selection_sort(list_in)) == list_out
        assert (insertion_sort(list_in)) == list_out
        assert (merge_sort(list_in)) == list_out
        assert (quick_sort(list_in)) == list_out


# Пузырьковая сортировка
def bubble_sort(arr):
    # итерируемся по неотсорт. массиву до предпоследнего элемента
    for i in range(0, len(arr) - 1):
        # проставляем условия флага для финального списка
        swapped = False
        # итерируемся по осташвимся неотсортированным объектам
        for j in range(0, len(arr) - 1 - i):
            # сравниваем соседние элементы
            if arr[j] > arr[j + 1]:
                # меняем элементы местами
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        # завершаем алгоритм, если смены не произошло
        if not swapped:
            return arr


# Сортировка выбором
def selection_sort(arr):
    for i in range(len(arr)):
        minimum = i
        for j in range(i + 1, len(arr)):
            # Выбор наименьшего значения
            if arr[j] < arr[minimum]:
                minimum = j
        # Помещаем это перед отсортированным концом массива
        arr[minimum], arr[i] = arr[i], arr[minimum]
    return arr


# Сортировка вставками
def insertion_sort(arr):
    for i in range(len(arr)):
        cursor = arr[i]
        pos = i
        while pos > 0 and arr[pos - 1] > cursor:
            # Меняем местами число, продвигая по списку
            arr[pos] = arr[pos - 1]
            pos = pos - 1
        # Остановимся и сделаем последний обмен
        arr[pos] = cursor
    return arr


# Сортировка слиянием
def merge_sort(arr):
    # Последнее разделение массива
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    # Выполняем merge_sort рекурсивно с двух сторон
    left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])
    # Объединяем стороны вместе
    return merge(left, right, arr.copy())


def merge(left, right, merged):
    left_cursor, right_cursor = 0, 0
    while left_cursor < len(left) and right_cursor < len(right):
        # Сортируем каждый и помещаем в результат
        if left[left_cursor] <= right[right_cursor]:
            merged[left_cursor + right_cursor] = left[left_cursor]
            left_cursor += 1
        else:
            merged[left_cursor + right_cursor] = right[right_cursor]
            right_cursor += 1
    for left_cursor in range(left_cursor, len(left)):
        merged[left_cursor + right_cursor] = left[left_cursor]
    for right_cursor in range(right_cursor, len(right)):
        merged[left_cursor + right_cursor] = right[right_cursor]
    return merged


# Быстрая сортировка
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if x <= pivot]
    greater = [x for x in arr[1:] if x > pivot]
    return quick_sort(less) + [pivot] + quick_sort(greater)


if __name__ == "__main__":
    app = App()
    app.mainloop()
