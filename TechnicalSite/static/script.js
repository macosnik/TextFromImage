// Получение элемента холста по его id
const canvas = document.getElementById('drawingCanvas');

// Получение контекста для рисования 2d холста
const wayDrawing = canvas.getContext('2d');

// Вводим переменную для отслеживания рисования
let drawing = false;

// Начальная толщина кисти
let brushSize = 35;

// Начало рисования
function startDrawing(e) {
    // Устанавливаем состояние рисования в true
    drawing = true;

    // Функция рисования
    draw(e);
}

// Окончания рисования
function endDrawing() {
    // Устанавливаем состояние рисования в false
    drawing = false;

    // Сбрасываем текущий путь рисования
    wayDrawing.beginPath();
}

// Рисование на холсте
function draw(e) {
    // Если не рисуем, выходим
    if (!drawing) {
        return;
    }

    // Устанавливаем толщину линии
    wayDrawing.lineWidth = brushSize;

    // Устанавливаем закругление концов линий
    wayDrawing.lineCap = 'round';

    // Устанавливаем цвет линии
    wayDrawing.strokeStyle = 'black';

    // Получаем размеры холста относительно окна
    const rect = canvas.getBoundingClientRect();

    // Объявляем координаты
    let x, y;

    // Если это событие касания, берем координаты первого касания
    if (e.touches) {
        // Вычисляем координату X
        x = e.touches[0].clientX - rect.left;

        // Вычисляем координату Y
        y = e.touches[0].clientY - rect.top;
    }

    // Иначе если это событие мыши, берем координаты мыши
    else {
        // Вычисляем координату X
        x = e.clientX - rect.left;

        // Вычисляем координату Y
        y = e.clientY - rect.top;
    }

    // Масштабируем координаты для корректного отображения
    x *= (canvas.width / rect.width);
    y *= (canvas.height / rect.height);

    // Рисуем линию до новых координат
    wayDrawing.lineTo(x, y);

    // Применяем рисование
    wayDrawing.stroke();

    // Начинаем новый путь
    wayDrawing.beginPath();

    // Перемещаем курсор в новые координаты
    wayDrawing.moveTo(x, y);
}

// Обработчики событий для мыши:

// Начало рисования при нажатии кнопки мыши
canvas.addEventListener('mousedown', startDrawing);

// Окончание рисования при отпускании кнопки мыши
canvas.addEventListener('mouseup', endDrawing);

// Рисование при движении мыши
canvas.addEventListener('mousemove', draw);

// Обработчики событий для касания:

// Начало рисования при касании
canvas.addEventListener('touchstart', startDrawing);

// Окончание рисования при отпускании касания
canvas.addEventListener('touchend', endDrawing);
canvas.addEventListener('touchmove', draw); // Рисование при движении касания

// Обработчик изменения толщины кисти
document.getElementById('brushThickness').addEventListener('change', (e) => {
    brushSize = parseInt(e.target.value); // Обновляем толщину кисти на основе выбранного значения
});

// Очистка холста
document.getElementById('clearButton').addEventListener('click', () => {
    wayDrawing.clearRect(0, 0, canvas.width, canvas.height); // Очищаем весь холст
});

// Сохранение изображения
document.getElementById('saveButton').addEventListener('click', () => {
    // Создаем временный canvas для сохранения изображения
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');
    tempCanvas.width = canvas.width; // Устанавливаем ширину временного canvas
    tempCanvas.height = canvas.height; // Устанавливаем высоту временного canvas

    // Рисуем белый фон на временном canvas
    tempCtx.fillStyle = 'white'; // Устанавливаем цвет фона
    tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height); // Заполняем фон белым цветом

    // Копируем содержимое оригинального canvas на временный canvas
    tempCtx.drawImage(canvas, 0, 0);

    wayDrawing.clearRect(0, 0, canvas.width, canvas.height); // Очищаем оригинальный canvas

    // Получаем данные изображения в формате PNG
    const imageData = tempCanvas.toDataURL('image/png');
    // Отправляем данные изображения на сервер
    fetch('/save-image', {
        method: 'POST', // Указываем метод запроса
        headers: {
            'Content-Type': 'application/json', // Указываем тип содержимого
        },
        body: JSON.stringify({ image: imageData }), // Преобразуем данные изображения в JSON-формат
    })
    .then(response => response.json()) // Обрабатываем ответ от сервера, ожидая JSON
    .then(data => {
        if (data.success == false) { // Проверяем, успешен ли ответ
            alert('Ошибка при сохранении изображения.'); // Если нет, выводим сообщение об ошибке
        }
    })
    .catch(error => {
        console.error('Ошибка:', error); // Логируем ошибку в консоль, если произошла ошибка
    });
});