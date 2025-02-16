from flask import Flask, render_template, request, jsonify
import os
import base64

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
        target_folder = os.path.join(UPLOAD_FOLDER, folder)
        os.makedirs(target_folder, exist_ok=True)

        # Сохраняем изображение
        file_path = os.path.join(target_folder, 'drawing.png')
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(data['image'].split(',')[1]))

        return jsonify({'success': True})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=1324)