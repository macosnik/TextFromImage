from flask import Flask, render_template, request, jsonify
from os import path, listdir, makedirs
from base64 import b64decode

app = Flask(__name__)

UPLOAD_FOLDER = '../BaseOfData'

@app.route('/')
def home():
    return render_template('page.html')


@app.route('/save-image', methods=['POST'])
def save_image():
    try:
        data = request.json
        folder = data.get('folder', 'tests')

        # Создаем целевую папку
        target_folder = path.join(UPLOAD_FOLDER, folder)
        makedirs(target_folder, exist_ok=True)

        num_picture = len(listdir(target_folder)) + 1

        name_file = f'{target_folder[target_folder.rfind("/") + 1:]}_{num_picture}.png'

        # Сохраняем изображение
        file_path = path.join(target_folder, name_file)
        with open(file_path, 'wb') as f:
            f.write(b64decode(data['image'].split(',')[1]))

        return jsonify({'success': True})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=1324)