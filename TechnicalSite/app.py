# Flask и компоненты для веб-приложения
from flask import Flask, render_template, request, jsonify

# Работа с файловой системой
from os import path, listdir, makedirs, getcwd

# Декодирование base64
from base64 import b64decode

# Наш модуль для обработки изображений
import image_utils

import threading

# Создание Flask приложения
app = Flask(__name__)

# Путь для сохранения загруженных изображений
UPLOAD_FOLDER = '../BaseOfData'

def photo_processing(name_file):
    image = image_utils.load(name_file)

    image = image_utils.compression(image, 25, 25)

    image_utils.save(image, f"{name_file[:-3]}bmp")

# Маршрут для главной страницы
@app.route('/')
def home():
    # Рендеринг html шаблона из папки templates
    return render_template('page.html')

@app.route('/get-image-count')
def get_image_count():
    folder = request.args.get('folder', 'tests')
    target_folder = path.join(UPLOAD_FOLDER, folder)
    if not path.exists(target_folder):
        return jsonify({'count': 0})
    try:
        count = len([f for f in listdir(target_folder) if path.isfile(path.join(target_folder, f))])
        return jsonify({'count': count})
    except Exception as e:
        print(f"Error getting image count: {e}")
        return jsonify({'count': 0})


# Маршрут для сохранения изображений
@app.route('/save-image', methods=['POST'])
def save_image():
    try:
        # Получение json данных
        data = request.json

        # Извлечение имени папки из запроса
        folder = data.get('folder', 'tests')

        # Создание полного пути к целевой папке
        target_folder = path.join(UPLOAD_FOLDER, folder)

        # Создание папки (если не существует)
        makedirs(target_folder, exist_ok=True)

        # Подсчет количества файлов для генерации имени
        num_picture = len(listdir(target_folder))

        # Генерация имени файла
        name_file = f'{target_folder[target_folder.rfind("/") + 1:]}_{num_picture + 1}.png'

        # Полный путь для сохранения файла
        file_path = path.join(target_folder, name_file)

        # Сохранение изображения
        with open(file_path, 'wb') as f:
            # Разделение данных изображения на части (тип и данные)
            img_data = data['image'].split(',')[1]

            # Запись в файл
            f.write(b64decode(img_data))

        all_path = f'{getcwd()[:getcwd().rfind('/')]}/{target_folder[3:]}/{name_file}'

        threading.Thread(target=photo_processing, args=(all_path,)).start()

        # Возврат ответа
        return jsonify({'success': True})

    except Exception as e:
        # Обработка ошибок: вывод в консоль и возврат сообщения
        print(f"Error: {str(e)}")

        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Хост 0.0.0.0 позволяет доступ с любого IP
    app.run(host='0.0.0.0', debug=True, port=1324)