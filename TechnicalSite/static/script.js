// Получаем элемент canvas по его ID
const canvas = document.getElementById('drawingCanvas');
// Получаем контекст рисования 2D для canvas
const ctx = canvas.getContext('2d');
// Переменная для отслеживания состояния рисования
let drawing = false;

// Устанавливаем начальную толщину кисти
let brushThickness = 35;

// Функция для начала рисования
function startDrawing(e) {
    drawing = true; // Устанавливаем состояние рисования в true
    draw(e); // Вызываем функцию рисования
}

// Функция для окончания рисования
function endDrawing() {
    drawing = false; // Устанавливаем состояние рисования в false
    ctx.beginPath(); // Сбрасываем текущий путь рисования
}

// Функция для рисования на canvas
function draw(e) {
    if (!drawing) return; // Если не рисуем, выходим из функции

    ctx.lineWidth = brushThickness; // Устанавливаем толщину линии
    ctx.lineCap = 'round'; // Устанавливаем закругление концов линий
    ctx.strokeStyle = 'black'; // Устанавливаем цвет линии

    // Получаем размеры canvas относительно окна
    const rect = canvas.getBoundingClientRect();

    // Переменные для координат
    let x, y;
    if (e.touches) {
        // Если это событие касания, берем координаты первого касания
        x = e.touches[0].clientX - rect.left; // Вычисляем координату X
        y = e.touches[0].clientY - rect.top; // Вычисляем координату Y
    } else {
        // Если это событие мыши, берем координаты мыши
        x = e.clientX - rect.left; // Вычисляем координату X
        y = e.clientY - rect.top; // Вычисляем координату Y
    }

    // Масштабируем координаты для корректного отображения
    x *= (canvas.width / rect.width);
    y *= (canvas.height / rect.height);

    ctx.lineTo(x, y); // Рисуем линию до новых координат
    ctx.stroke(); // Применяем рисование
    ctx.beginPath(); // Начинаем новый путь
    ctx.moveTo(x, y); // Перемещаем "перо" в новые координаты
}

// Обработчики событий для мыши
canvas.addEventListener('mousedown', startDrawing); // Начало рисования при нажатии кнопки мыши
canvas.addEventListener('mouseup', endDrawing); // Окончание рисования при отпускании кнопки мыши
canvas.addEventListener('mousemove', draw); // Рисование при движении мыши

// Обработчики событий для касания
canvas.addEventListener('touchstart', startDrawing); // Начало рисования при касании
canvas.addEventListener('touchend', endDrawing); // Окончание рисования при отпускании касания
canvas.addEventListener('touchmove', draw); // Рисование при движении касания

// Обработчик изменения толщины кисти
document.getElementById('brushThickness').addEventListener('change', (e) => {
    brushThickness = parseInt(e.target.value); // Обновляем толщину кисти на основе выбранного значения
});

// Очистка холста
document.getElementById('clearButton').addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Очищаем весь холст
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

    ctx.clearRect(0, 0, canvas.width, canvas.height); // Очищаем оригинальный canvas

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