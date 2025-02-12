def load(name_file):
    if name_file[-3:] != 'bmp':
        import os
        os.system(f"convert {name_file} -depth 24 -type TrueColor {f'{name_file[:name_file.rfind('.')]}.bmp'}")
        name_file = f'{name_file[:name_file.rfind('.')]}.bmp'

    with open(name_file, 'rb') as file:
        data = file.read()

    width = int.from_bytes(data[18:22], byteorder='little')
    height = int.from_bytes(data[22:26], byteorder='little')

    data = data[138:]

    arr = []

    row_size = (width * 3 + 3) // 4 * 4

    for y in range(height - 1, -1, -1):
        row = []

        for x in range(width):
            index = y * row_size + x * 3

            row.append((data[index + 2], data[index + 1], data[index]))

        arr.append(row)

    return arr

def save(arr, name_file):
    width = len(arr[0])
    height = len(arr)

    row_size = ((width * 3 + 3) // 4) * 4

    pixels_size = row_size * height
    data_size = 138 + pixels_size

    pixels_data = bytearray()
    for y in range(height - 1, -1, -1):
        for x in range(width):
            pixels_data.extend([arr[y][x][2], arr[y][x][1], arr[y][x][0]])

        pixels_data.extend([0] * (row_size - width * 3))

    with open(name_file, 'wb') as data:
        data.write(bytearray([0x42, 0x4D, # Тип
                   data_size & 0xFF, (data_size >> 8) & 0xFF, (data_size >> 16) & 0xFF, (data_size >> 24) & 0xFF, # Размер
                   0, 0, 0, 0, 138, 0, 0, 0 # 138 - заголовки + метаданные в байтах
                   ]))

        data.write(bytearray([
                   40, 0, 0, 0,  # Размер
                   width & 0xFF, (width >> 8) & 0xFF, (width >> 16) & 0xFF, (width >> 24) & 0xFF,  # Ширина
                   height & 0xFF, (height >> 8) & 0xFF, (height >> 16) & 0xFF, (height >> 24) & 0xFF,  # Высота
                   1, 0, 24, 0, 0, 0, 0, 0, # 24 - скольки байтовое изображение
                   pixels_size & 0xFF, (pixels_size >> 8) & 0xFF, (pixels_size >> 16) & 0xFF, (pixels_size >> 24) & 0xFF,  # Размер
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                   ]))

        data.write(bytearray(83))

        data.write(pixels_data)