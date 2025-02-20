import flask, os, base64, threading, image_utils

app = flask.Flask(__name__)

def photo_processing(name_file):
    image = image_utils.Image(name_file)
    image.compression(25, 25)
    image.save(name_file)

@app.route('/')
def home():
    return flask.render_template('page.html')

@app.route('/get-image-count')
def get_image_count():
    target_folder = f"../DataCenter/{flask.request.args.get('folder', 'tests')}"
    count = len(os.listdir(target_folder))
    return flask.jsonify({'count': count})

@app.route('/save-image', methods=['POST'])
def save_image():
    try:
        data = flask.request.json

        target_folder = f'../DataCenter/{data.get('folder', 'tests')}'
        num_files = len(os.listdir(target_folder))
        name_file = f'image_{num_files + 1}.bmp'
        file_path = f'{target_folder}/{name_file}'

        with open(file_path, 'wb') as f:
            img_data = str(data['image'])[str(data['image']).rfind(','):]
            f.write(base64.b64decode(img_data))

        all_path = f'{os.getcwd()[:os.getcwd().rfind('/')]}/{target_folder[3:]}/{name_file}'
        threading.Thread(target=photo_processing, args=(all_path,)).start()

        return flask.jsonify({'success': True})

    except Exception as e:
        print(f"Error: {str(e)}")
        return flask.jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=1324)
