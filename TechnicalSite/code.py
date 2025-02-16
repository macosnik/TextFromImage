from flask import Flask

# Создаем экземпляр приложения Flask
app = Flask(__name__)

# Определяем маршрут для главной страницы
@app.route('/')
def home():
    # Возвращаем HTML с текстом "TextFromImage"
    return open('html.html')

# Запускаем приложение
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=1324)