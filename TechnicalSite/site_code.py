from flask import Flask, render_template, request, jsonify
import os
import base64

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('page.html')

@app.route('/save-image', methods=['POST'])
def save_image():
    try:
        data = request.json
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)

        file_path = os.path.join(UPLOAD_FOLDER, 'drawing.png')
        with open(file_path, 'wb') as f:
            f.write(image_bytes)

        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=1324)