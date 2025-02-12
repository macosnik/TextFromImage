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


