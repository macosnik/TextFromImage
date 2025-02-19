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
        pass

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
