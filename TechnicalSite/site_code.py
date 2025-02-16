from flask import Flask, render_template, request, jsonify  # Flask и компоненты для веб-приложения
from os import path, listdir, makedirs  # Работа с файловой системой
from base64 import b64decode  # Декодирование base64

# Создание Flask приложения
app = Flask(__name__)

# Путь для сохранения загруженных изображений
UPLOAD_FOLDER = '../BaseOfData'


# Маршрут для главной страницы
@app.route('/')
def home():
    # Рендеринг html шаблона из папки templates
    return render_template('page.html')


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

        # Возврат ответа
        return jsonify({'success': True})

    except Exception as e:
        # Обработка ошибок: вывод в консоль и возврат сообщения
        print(f"Error: {str(e)}")

        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Хост 0.0.0.0 позволяет доступ с любого IP
    app.run(host='0.0.0.0', debug=True, port=1324)
