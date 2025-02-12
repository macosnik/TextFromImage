def load(name_file): # Чтение изображений
    if name_file[-3:] != 'bmp': # Если тип файла не BMP
        from os import system # Для работы с терминалом

        system(f"convert {name_file} -depth 24 -type TrueColor {f'{name_file[:name_file.rfind('.')]}.bmp'}") # Преобразовываем формат изображения в BMP с помощью терминала
        name_file = f'{name_file[:name_file.rfind('.')]}.bmp' # Новое имя файла (Меняем с нынешнего формата на BMP)

    with open(name_file, 'rb') as file: # Открытие файла для чтения
        data = file.read() # Читаем файл и получаем байтовое представление файла

    width = int.from_bytes(data[18:22], byteorder='little') # Ширина изображения
    height = int.from_bytes(data[22:26], byteorder='little') # Высота изображения

    data = data[138:] # Оставляем только пиксельные данные, идущие за 137 байтом (заголовки и метаданные в байтах)

    arr = [] # Создаём список для будущего изображения в RGB формате

    row_size = (width * 3 + 3) // 4 * 4 # Длина строки с учётом выравнивания по байтам (кратно 4)

    for y in range(height - 1, -1, -1): # Отзеркаливаем изображение во все стороны, поскольку BMP файл их хранит в перевёрнутом виде
        row = [] # Создаём список для строки

        for x in range(width):
            index = y * row_size + x * 3 # Положение нынешнего пикселя на изображении

            row.append((data[index + 2], data[index + 1], data[index])) # Добавляем в строку соответствующий RGB цвет

        arr.append(row) # Добавляем строку в изображение

    return arr # Возвращаем изображение

def save(arr, name_file): # Сохранение BMP изображения
    width = len(arr[0]) # Ширина изображения
    height = len(arr) # Высота изображения

    row_size = ((width * 3 + 3) // 4) * 4 # Длина строки с учётом выравнивания по байтам (кратно 4)

    pixels_size = row_size * height # Размер данных пикселей (в байтах)
    data_size = 137 + pixels_size # Размер всего файла (в байтах). 137 - это размер заголовков и метаданных

    pixels_data = bytearray() # Пиксельные данные
    for y in range(height - 1, -1, -1): # Отзеркаливаем изображение во все стороны, поскольку BMP файл их хранит в перевёрнутом виде
        for x in range(width):
            pixels_data.extend([arr[y][x][2], arr[y][x][1], arr[y][x][0]]) # Добавляем в данные цвета в формате BGR

        pixels_data.extend([0] * (row_size - width * 3)) # Добавляем дополнительные байты для выравнивания

    with open(name_file, 'wb') as data: # Открываем файл, если нет, то создаём
        # Записываем файловые данные
        data.write(bytearray([0x42, 0x4D, # Тип
                   data_size & 0xFF, (data_size >> 8) & 0xFF, (data_size >> 16) & 0xFF, (data_size >> 24) & 0xFF, # Размер
                   0, 0, 0, 0, 137, 0, 0, 0 # 137 - заголовки + метаданные в байтах
                   ]))

        # Записываем информационные данные
        data.write(bytearray([
                   40, 0, 0, 0,  # Размер
                   width & 0xFF, (width >> 8) & 0xFF, (width >> 16) & 0xFF, (width >> 24) & 0xFF,  # Ширина
                   height & 0xFF, (height >> 8) & 0xFF, (height >> 16) & 0xFF, (height >> 24) & 0xFF,  # Высота
                   1, 0, 24, 0, 0, 0, 0, 0, # 24 - скольки байтовое изображение
                   pixels_size & 0xFF, (pixels_size >> 8) & 0xFF, (pixels_size >> 16) & 0xFF, (pixels_size >> 24) & 0xFF,  # Размер
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                   ]))

        data.write(bytearray(83)) # Записываем пиксельные данные

        data.write(pixels_data) # Записываем пиксельные данные