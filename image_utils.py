from sys import byteorder

import numpy

def load(file_name):
    with open(file_name, 'rb') as file:
        file_header = file.read(14)

        if file_header[:2] != b'BM':
            raise ValueError('Ошибка конвертации изображения')

        pixels_data_offset = int.from_bytes(file_header[10:14], byteorder='little')

        print(pixels_data_offset)

        info_header = file.read(40)

        width = int.from_bytes(info_header[4:8], byteorder='little')
        height = int.from_bytes(info_header[8:12], byteorder='little')


