# Для быстрой работы с массивами
from numpy import frombuffer, uint8
from os import getcwd, listdir, system
from subprocess import run


def load(file_name):
    """
    Загрузка изображения для получения всех цветов пикселей
    :param file_name: имя файла
    :return: список пикселей rgb формата
    """
    if file_name[-4:] != '.bmp':
        bmp_name = f"{file_name[:file_name.rfind('.')]}.bmp"

        if bmp_name not in listdir(getcwd()):
            run(["convert", file_name, "-depth", "24", "-type", "TrueColor", bmp_name], check=True)

        file_name = bmp_name

    with open(file_name, 'rb') as file:
        file_header = file.read(14)

        if file_header[:2] != b'BM':
            raise ValueError('Ошибка конвертации изображения')

        pixels_data_offset = int.from_bytes(file_header[10:14], byteorder='little')

        info_header = file.read(40)

        width = int.from_bytes(info_header[4:8], byteorder='little')
        height = int.from_bytes(info_header[8:12], byteorder='little')

        bits_pixels = int.from_bytes(info_header[14:16], byteorder='little')

        if bits_pixels != 24:
            raise ValueError('Ошибка конвертации изображения')

        file.seek(pixels_data_offset)

        row_size = (width * 3 + 3) & ~3

        image_data = file.read(row_size * height)

        arr = frombuffer(image_data, dtype=uint8)

        arr = arr.reshape((height, row_size))[:, :width * 3].reshape(height, width, 3)

        arr = arr[:, :, [2, 1, 0]]

        return arr

