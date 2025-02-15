# NumPy - быстрая работа с массивами(значительно ускорит алгоритмы)
from numpy import frombuffer, uint8, zeros, full, cumsum, mean
"""
:param frombuffer - создание NumPy массива из байтовой строки
:param uint8 - беззнаковое 8 байтовое целочисленное число NumPy
:param zeros - заполнение массива нулями
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

        # Чтение расстояния в батах до данных пикселей (4 байта, начиная с 10 байта)
        pixels_data_offset = int.from_bytes(file_header[10:14], byteorder='little')

        # Чтение информационного заголовка (40 байт)
        info_header = file.read(40)

        # Чтение высоты и ширина изображения (по 4 байта, начиная с 4 байта)
        width = int.from_bytes(info_header[4:8], byteorder='little')
        height = int.from_bytes(info_header[8:12], byteorder='little')

        # Получение кол-ва байтов в палитре пикселя
        bits_pixels = int.from_bytes(info_header[14:16], byteorder='little')

        # Если байтовая палитра не является 24 битной, то сваливаем всё на ошибку в конвертации файла
        if bits_pixels != 24:
            raise ValueError('Ошибка конвертации изображения')

        # Читаем оставшиеся байты до пикселей
        file.seek(pixels_data_offset)

        # Рассчитываем размер строки с учётом смещения
        row_size = (width * 3 + 3) & ~3

        # Чтение всех пикселей
        arr_data = file.read(row_size * height)

        # Создаю массив на основе всех пикселей в байтах. Тип чисел - беззнаковое 8 байтовое целочисленное
        arr = frombuffer(arr_data, dtype=uint8)

        # Сначала массив перестраивается в height количество первичных массивов в arr, затем в width количество двоичных массивов в каждом массиве первичного массива.
        # Затем обрезаем вторичный массив до width * 3. (: - это все строки)
        # Затем преобразовываем массив в трёхмерный, добавляя в троичный массив по 3 числа
        arr = arr.reshape((height, row_size))[:, :width * 3].reshape(height, width, 3)

        # Изменяем порядок троичных данных массива, переворачивая массив. Было BGR, а стало - RGB
        arr = arr[:, :, [2, 1, 0]]

        # Возвращаем массив
        return arr

def save(arr, file_name):
    """
    Сохранение изображения
    :param arr: изображение
    :param file_name: Имя файла
    :return: ничего
    """
    # Получаем размеры изображения
    height, width, _ = arr.shape

    # Рассчитываем размер строки с учётом смещения
    row_size = (width * 3 + 3) & ~3


    pixels_size = row_size * height


    data_size = 14 + 40 + 83 + pixels_size

    # Файловый заголовок (14 байт)
    file_header = bytearray([
        0x42, 0x4D,  # bfType
        data_size & 0xFF, (data_size >> 8) & 0xFF, (data_size >> 16) & 0xFF, (data_size >> 24) & 0xFF,  # bfSize
        0, 0, 0, 0, 14 + 40 + 83, 0, 0, 0  # bfOffBits
    ])

    # Информационный заголовок (40 байт)
    info_header = bytearray([
        40, 0, 0, 0,  # biSize
        width & 0xFF, (width >> 8) & 0xFF, (width >> 16) & 0xFF, (width >> 24) & 0xFF,  # biWidth
        height & 0xFF, (height >> 8) & 0xFF, (height >> 16) & 0xFF, (height >> 24) & 0xFF,  # biHeight
        1, 0,
        24, 0,  # biBitCount
        0, 0, 0, 0,
        pixels_size & 0xFF, (pixels_size >> 8) & 0xFF, (pixels_size >> 16) & 0xFF,
        (pixels_size >> 24) & 0xFF,  # biSizeImage
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ])

    # Метаданные (83 байта)
    meta_data = bytearray(83)  # Заполняем нулями

    bgr_arr = arr[:, :, [2, 1, 0]]

    padded_arr = zeros((height, row_size), dtype=uint8)
    padded_arr[:, :width * 3] = bgr_arr.reshape(height, width * 3)

    pixels_data = padded_arr.tobytes()

    with open(file_name, 'wb') as file:
        file.write(file_header)
        file.write(info_header)
        file.write(meta_data)
        file.write(pixels_data)

def compression(arr, horizontally, vertically):
    """
    Сжимание изображения
    :param arr: изображение
    :param horizontally: желаемый размер стороны по вертикали
    :param vertically: желаемый размер стороны по горизонтали
    :return: изображение
    """
    # Находим высоту и ширину изображения
    height, width, _ = arr.shape

    # Создаём массивы с указанием размеров блоков: по горизонтали и вертикали. Заполняем его числами полученными в результате деления исходно1 на желаемую стороны изображения
    x_factors =  full(horizontally, width // horizontally)
    y_factors = full(vertically, height // vertically)

    # Остаток раскидываем по массиву указаний размеров блоков
    x_factors[:width % horizontally] += 1
    y_factors[:height % vertically] += 1


