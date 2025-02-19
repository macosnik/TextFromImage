import os, math

class Image:
    def __init__(self, name):
        self.name = name
        self.width = None
        self.height = None
        self.arr = None

    def load(self):
        os.system(f"convert {self.name} -depth 24 -type TrueColor {self.name[:self.name.rfind('.')]}.bmp")

        with open(f"{self.name[:self.name.rfind('.')]}.bmp", 'rb') as file:
            data = file.read(54)

            distance_to_pixels = int.from_bytes(data[10:14], byteorder='little')
            self.width = int.from_bytes(data[18:22], byteorder='little')
            self.height = int.from_bytes(data[22:26], byteorder='little')

            file.seek(distance_to_pixels)

            row_size = (self.width * 3 + 3) // 4 * 4
            self.arr = []

            data = file.read(row_size * self.height)

            for y in range(self.height - 1, -1, -1):
                row = []
                for x in range(self.width):
                    index = y * row_size + x * 3
                    row.append((data[index + 2], data[index + 1], data[index]))
                self.arr.append(row)

    def save(self, file_name):
        row_size = (self.width * 3 + 3) // 4 * 4
        pixels_size = row_size * self.height
        remains = row_size - self.width * 3
        data_size = pixels_size + 54

        data = bytearray([
            0x42, 0x4D,
            data_size & 0xFF, (data_size >> 8) & 0xFF, (data_size >> 16) & 0xFF, (data_size >> 24) & 0xFF,
            0, 0, 0, 0, 54, 0, 0, 0, 40, 0, 0, 0,
            self.width & 0xFF, (self.width >> 8) & 0xFF, (self.width >> 16) & 0xFF, (self.width >> 24) & 0xFF,
            self.height & 0xFF, (self.height >> 8) & 0xFF, (self.height >> 16) & 0xFF, (self.height >> 24) & 0xFF,
            1, 0, 24, 0, 0, 0, 0, 0,
            pixels_size & 0xFF, (pixels_size >> 8) & 0xFF, (pixels_size >> 16) & 0xFF, (pixels_size >> 24) & 0xFF,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ])

        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                data.extend([self.arr[y][x][2], self.arr[y][x][1], self.arr[y][x][0]])
            data.extend([0] * remains)

        with open(file_name, 'wb') as file:
            file.write(data)

    def compression(self, arr, horizontally, vertically):
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

    def simplify(self, factor=127.5):
        for y in range(self.height):
            for x in range(self.width):
                if sum(self.arr[y][x]) / 3 >= factor:
                    self.arr[y][x] = (255, 255, 255)
                else:
                    self.arr[y][x] = (0, 0, 0)

    def draw_line(self, x1, y1, x2, y2, color):
        width = len(self.arr)
        height = len(self.arr[0])
        delta_x = abs(x1 - x2)
        delta_y = abs(y1 - y2)
        length = int(math.sqrt(delta_x ** 2 + delta_y ** 2))

        for i in range(length):
            x = round(x1 + (x2 - x1) * i / length)
            y = round(y1 + (y2 - y1) * i / length)

            if 0 <= y < height and 0 <= x < width:
                self.arr[y][x] = color
