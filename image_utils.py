import os, math

def load(name):
    os.system(f"convert {name} -depth 24 -type TrueColor {name[:name.rfind('.')]}.bmp")

    with open(f"{name[:name.rfind('.')]}.bmp", 'rb') as file:
        data = file.read(54)

        distance_to_pixels = int.from_bytes(data[10:14], byteorder='little')
        width = int.from_bytes(data[18:22], byteorder='little')
        height = int.from_bytes(data[22:26], byteorder='little')

        file.seek(distance_to_pixels)

        row_size = (width * 3 + 3) // 4 * 4
        arr = []

        data = file.read(row_size * height)

        for y in range(height - 1, -1, -1):
            row = []
            for x in range(width):
                index = y * row_size + x * 3
                row.append((data[index + 2], data[index + 1], data[index]))
            arr.append(row)

        return arr

def save(arr, file_name):
    width = len(arr[0])
    height = len(arr)
    row_size = (width * 3 + 3) // 4 * 4
    pixels_size = row_size * height
    remains = row_size - width * 3
    data_size = pixels_size + 54

    data = bytearray([
        0x42, 0x4D,
        data_size & 0xFF, (data_size >> 8) & 0xFF, (data_size >> 16) & 0xFF, (data_size >> 24) & 0xFF,
        0, 0, 0, 0, 54, 0, 0, 0, 40, 0, 0, 0,
        width & 0xFF, (width >> 8) & 0xFF, (width >> 16) & 0xFF, (width >> 24) & 0xFF,
        height & 0xFF, (height >> 8) & 0xFF, (height >> 16) & 0xFF, (height >> 24) & 0xFF,
        1, 0, 24, 0, 0, 0, 0, 0,
        pixels_size & 0xFF, (pixels_size >> 8) & 0xFF, (pixels_size >> 16) & 0xFF, (pixels_size >> 24) & 0xFF,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ])

    for y in range(height - 1, -1, -1):
        for x in range(width):
            data.extend([arr[y][x][2], arr[y][x][1], arr[y][x][0]])
        data.extend([0] * remains)

    with open(file_name, 'wb') as file:
        file.write(data)

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
    x_factors =  numpy.full(horizontally, width // horizontally)
    y_factors = numpy.full(vertically, height // vertically)

    # Остаток раскидываем по массиву указаний размеров блоков
    x_factors[:width % horizontally] += 1
    y_factors[:height % vertically] += 1

    # Вычисление индексов для получения блоков изображения
    x_indexes = numpy.cumsum([0] + x_factors.tolist())
    y_indexes = numpy.cumsum([0] + y_factors.tolist())

    # Создаём новый массив, в котором будет конечный результат
    new_arr = numpy.zeros((vertically, horizontally, 3), dtype=numpy.uint8)

    # Поблочная обработка
    for y in range(vertically):
        for x in range(horizontally):
            # Собираем все цвета с изображения в пределе между ближайшими индексами в массиве
            block = arr[y_indexes[y]:y_indexes[y + 1], x_indexes[x]:x_indexes[x + 1]]

            # Сумма цветов в блоке
            sum_colors = numpy.mean(block, axis=(0, 1))

            # Если меньше синего, то закрашиваем в чёрный
            new_arr[y, x] = (255, 255, 255) if numpy.mean(sum_colors) >= 127.5 else (0, 0, 0)

    # Возвращаем сжатое изображение
    return new_arr

def simplify(arr, factor=127.5):
    for y in range(len(arr)):
        for x in range(len(arr[0])):
            if sum(arr[y][x]) / 3 >= factor:
                arr[y][x] = (255, 255, 255)
            else:
                arr[y][x] = (0, 0, 0)
    return arr

def draw_line(arr, x1, y1, x2, y2, color):
    width = len(arr)
    height = len(arr[0])
    delta_x = abs(x1 - x2)
    delta_y = abs(y1 - y2)
    length = int(math.sqrt(delta_x ** 2 + delta_y ** 2))

    for i in range(length):
        x = round(x1 + (x2 - x1) * i / length)
        y = round(y1 + (y2 - y1) * i / length)

        if 0 <= y < height and 0 <= x < width:
            arr[y][x] = color

    return arr
