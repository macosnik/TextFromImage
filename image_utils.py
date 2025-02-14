# NumPy - быстрая работа с массивами(значительно ускорит алгоритмы)
from numpy import frombuffer, uint8
"""
:param frombuffer - создание NumPy массива из байтовой строки
:param uint8 - беззнаковое 8 байтовое целочисленное число NumPy
"""

# os - модуля для взаимосвязи с компьютером
from os import getcwd as path, listdir as path_obj
"""
:param path - функция для нахождения пути по компьютеру к данной директории
:param path_obj - функция для нахождения всех папок и фалов по пути
"""

# subprocess - модуль для реализации компьютерных процессов
from subprocess import run as terminal
"""
:param terminal - функция для обращения к терминалу
"""

def load(file_name):
    """
    Загрузка изображения для получения всех цветов пикселей
    :param file_name: имя файла
    :return: список пикселей rgb формата
    """
    # Если нынешний тип файла не bmp:
    if file_name[-4:] != '.bmp':
        # Вид будущего названия фала (bmp формат)
        bmp_name = f"{file_name[:file_name.rfind('.')]}.bmp"

        # Если в директории нет ожидаемого типа файла, то выполняем:
        if bmp_name not in path_obj(path()):
            # Нынешний тип файла конвертируем в ожидаемый тип
            terminal(["convert", file_name, "-depth", "24", "-type", "TrueColor", bmp_name], check=True)

        # Присваиваем нынешнему названию ожидаемое
        file_name = bmp_name

    # Открываем файл
    with open(file_name, 'rb') as file:
        # Читаем первые 14 байтов (файловый заголовок файла)
        file_header = file.read(14)

        # Если типом файла не является bmp, то сваливаем всё на ошибку в конвертации файла
        if file_header[:2] != b'BM':
            raise ValueError('Ошибка конвертации изображения')

        pixels_data_offset = int.from_bytes(file_header[10:14], byteorder='little')

        info_header = file.read(40)

        width = int.from_bytes(info_header[4:8], byteorder='little')
        height = int.from_bytes(info_header[8:12], byteorder='little')

        bits_pixels = int.from_bytes(info_header[14:16], byteorder='little')

        # Если байтовая палитра не является 24 битной, то сваливаем всё на ошибку в конвертации файла
        if bits_pixels != 24:
            raise ValueError('Ошибка конвертации изображения')

        file.seek(pixels_data_offset)

        row_size = (width * 3 + 3) & ~3

        image_data = file.read(row_size * height)

        arr = frombuffer(image_data, dtype=uint8)

        arr = arr.reshape((height, row_size))[:, :width * 3].reshape(height, width, 3)

        arr = arr[:, :, [2, 1, 0]]

        return arr

