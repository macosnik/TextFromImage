import os, math

class Image:
    def __init__(self, name):
        self.name = name
        self.width = None
        self.height = None
        self.arr = None

        self.__load__()

    def __load__(self):
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

    def compression(self, horizontally, vertically):
        # Будущее изображение
        new_image = []

        # Заполнение списка нулями, для дальнейшей работы с изображением
        for y in range(vertically):
            # Создание строки изображения
            row = []

            for x in range(horizontally):
                # Заполняем нулём
                row.append(0)

            # Добавляем строку в изображение
            new_image.append(row)

        # Списки с порядком размера ячеек: один - по горизонтали, второй - по вертикали
        x_factors = []
        y_factors = []

        # Представление частного при делении нынешних на будущие размеры изображения, для нахождения целого числа
        str_x = str(self.width / horizontally)
        str_y = str(self.height / vertically)

        # Длина целой части кратного, создание которой представлено выше
        length_int_part_x = 0
        length_int_part_y = 0

        # Увеличиваем длину целой части кратного до точки по горизонтали
        for i in str_x:
            # Если точка, то выходим из процесса
            if i == '.':
                break

            # Иначе увеличиваем длину
            else:
                length_int_part_x += 1

        # Увеличиваем длину целой части кратного до точки по вертикали
        for i in str_y:
            # Если точка, то выходим из процесса
            if i == '.':
                break

            # Иначе увеличиваем длину
            else:
                length_int_part_y += 1

        # Целая часть от кратного
        int_part_x = int(str_x[0:length_int_part_x])
        int_part_y = int(str_y[0:length_int_part_y])

        # Количество оставшихся пикселей от деления нынешних на будущие размеры изображения
        balance_x = self.width - horizontally * int_part_x
        balance_y = self.height - vertically * int_part_y

        # Перебираем список факторов по горизонтали и добавляем в него нужное кратное, если в запасе остались ещё пиксели, то добавляем ещё один
        for i in range(horizontally):
            # Если ещё есть в запасе, то добавляем с учётом его
            if balance_x != 0:
                x_factors.append(int_part_x + 1)
                balance_x -= 1

            # Иначе добавляем просто целую часть кратного
            else:
                x_factors.append(int_part_x)

        # Перебираем список факторов по вертикали и добавляем в него нужное кратное, если в запасе остались ещё пиксели, то добавляем ещё один
        for i in range(vertically):
            # Если ещё есть в запасе, то добавляем с учётом его
            if balance_y != 0:
                y_factors.append(int_part_y + 1)
                balance_y -= 1

            # Иначе добавляем просто целую часть кратного
            else:
                y_factors.append(int_part_y)

        # Заполнение нового изображения пикселями
        for y in range(vertically):
            for x in range(horizontally):
                # Начинаем отсчёт количества пикселей в нынешней зоне
                count_pixels = 0

                # Отсчёт от нуля до разницы начала координат зоны и конца
                for y_pixels in range(sum(y_factors[:y + 1]) - sum(y_factors[:y])):
                    for x_pixels in range(sum(x_factors[:x + 1]) - sum(x_factors[:x])):
                        # Увеличиваем количество пикселей в зоне
                        count_pixels += 1

                        # Оттенки цветов в пикселях нынешней зоны
                        pixel_color = self.arr[sum(y_factors[:y]) + y_pixels][sum(x_factors[:x]) + x_pixels]

                        # Суммируем все оттенки цветов нынешней зоны и сохраняем в изображение
                        new_image[y][x] += pixel_color[0] + pixel_color[1] + pixel_color[2]

                # Если при делении всех оттенков цветов в зоне на количество зон и количество оттенков в одном пикселе(3) получаем число меньше 127.5(половина от 225), то закрашиваем пиксель в чёрный
                if new_image[y][x] / count_pixels / 3 < 127.5:
                    new_image[y][x] = (0, 0, 0)

                # Иначе закрашиваем в белый
                else:
                    new_image[y][x] = (255, 255, 255)

        # Возвращаем новое изображение в формате rgb
        self.arr = new_image
        self.width = horizontally
        self.height = vertically

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
