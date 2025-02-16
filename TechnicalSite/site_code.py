from flask import Flask, render_template, request, jsonify
import os
import base64
import io

# Создаем экземпляр приложения Flask
app = Flask(__name__)

# Путь к папке для сохранения изображений
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Определяем маршрут для главной страницы
@app.route('/')
def home():
    return render_template('page.html')

# Маршрут для сохранения изображения
@app.route('/save-image', methods=['POST'])
def save_image():
    try:
        # Получаем данные изображения из запроса
        data = request.json
        image_data = data['image'].split(',')[1]  # Убираем заголовок Base64
        image_bytes = base64.b64decode(image_data)



        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False})

# Запускаем приложение
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=1324)
