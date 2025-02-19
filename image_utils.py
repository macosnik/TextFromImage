import os

def load(file_name):
    os.system(f"convert {file_name} -depth 24 -type TrueColor {file_name[:file_name.rfind('.')]}.bmp")

    with open(f"{file_name[:file_name.rfind('.')]}.bmp", 'rb') as file:
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

    # Размер пиксельный данных
    pixels_size = row_size * height

    # Размер файла
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

    # Создаём из rgb изображения rgb
    bgr_arr = arr[:, :, [2, 1, 0]]

    # Создаём массив и выравниваем каждую строку
    padded_arr = numpy.zeros((height, row_size), dtype=numpy.uint8)
    padded_arr[:, :width * 3] = bgr_arr.reshape(height, width * 3)

    # Преобразуем массив в битовый вид
    pixels_data = padded_arr.tobytes()

    with open(file_name, 'wb') as file:
        # Записываем все данные
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
    """
    Преобразование изображения в чёрно-белое
    :param arr: исходное изображение
    :param factor: пороговое значение для бинаризации
    :return: чёрно-белое изображение
    """
    # Средняя яркость для каждого пикселя
    brightness = numpy.mean(arr, axis=2)

    # Трёхканальный результат
    result = numpy.zeros((*brightness.shape, 3), dtype=numpy.uint8)

    # Бинаризация для всех трёх каналов одновременно
    result[:, :, :] = 255 * (brightness >= factor)[:, :, None]

    # Возвращаем чёрно-белое изображение
    return result

def draw_line(image, x1, y1, x2, y2, color):
    """
    Рисует прямую на рисунке
    :param image: изображение
    :param x1: координата начальной точки по горизонтали
    :param y1: координата начальной точки по вертикали
    :param x2: координата конечной точки по горизонтали
    :param y2: координата конечной точки по вертикали
    :param color: цвет линии в формате RGB
    :return: изображение с нарисованной линией
    """
    # Параметры ширины и высоты изображения
    height, width, _ = image.shape
    
    # Отзеркаливаем начало точек координат по вертикали
    y1 = height - y1
    y2 = height - y2

    # Вычисляем разницу по x и y
    delta_x = x2 - x1
    delta_y = y2 - y1

    # Находим длину линии
    length = max(abs(delta_x), abs(delta_y))  # Используем Bresenham-like подход

    if length == 0:
        # Если длина равна нулю, просто закрашиваем одну точку
        if 0 <= y1 < height and 0 <= x1 < width:
            image[y1, x1] = color
        return image

    # Генерируем координаты точек вдоль линии
    x_coords = numpy.round(numpy.linspace(x1, x2, length)).astype(int)
    y_coords = numpy.round(numpy.linspace(y1, y2, length)).astype(int)

    # Фильтруем точки, которые находятся внутри границ изображения
    valid_indices = (0 <= y_coords) & (y_coords < height) & (0 <= x_coords) & (x_coords < width)

    # Закрашиваем пиксели
    image[y_coords[valid_indices], x_coords[valid_indices]] = color

    # Возвращаем изображение с линией
    return image
