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

    def compression(self, width, height):
        self.width = len(self.arr[0])
        self.height = len(self.arr)

        arr = []

        for y in range(width):
            row = []
            for x in range(height):
                row.append(0)
            arr.append(row)

        x_factors = []
        y_factors = []

        str_x = str(self.width / width)
        str_y = str(self.height / height)

        length_int_part_x = 0
        length_int_part_y = 0

        for i in str_x:
            if i == '.':
                break
            else:
                length_int_part_x += 1

        for i in str_y:
            if i == '.':
                break
            else:
                length_int_part_y += 1

        int_part_x = int(str_x[0:length_int_part_x])
        int_part_y = int(str_y[0:length_int_part_y])

        balance_x = self.width - width * int_part_x
        balance_y = self.height - height * int_part_y

        for i in range(width):
            if balance_x != 0:
                x_factors.append(int_part_x + 1)
                balance_x -= 1
            else:
                x_factors.append(int_part_x)

        for i in range(width):
            if balance_y != 0:
                y_factors.append(int_part_y + 1)
                balance_y -= 1
            else:
                y_factors.append(int_part_y)

        for y in range(width):
            for x in range(height):
                count_pixels = 0

                for y_pixels in range(sum(y_factors[:y + 1]) - sum(y_factors[:y])):
                    for x_pixels in range(sum(x_factors[:x + 1]) - sum(x_factors[:x])):
                        count_pixels += 1

                        pixel_color = self.arr[sum(y_factors[:y]) + y_pixels][sum(x_factors[:x]) + x_pixels]

                        arr[y][x] += pixel_color[0] + pixel_color[1] + pixel_color[2]

                if arr[y][x] / count_pixels / 3 < 127.5:
                    arr[y][x] = (0, 0, 0)
                else:
                    arr[y][x] = (255, 255, 255)

        self.arr = arr

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
