const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
let drawing = false;

// Устанавливаем начальную толщину кисти
let brushThickness = 35;

// Функции для начала и окончания рисования
function startDrawing(e) {
    drawing = true;
    draw(e);
}

function endDrawing() {
    drawing = false;
    ctx.beginPath(); // Сбрасываем путь
}

function draw(e) {
    if (!drawing) return;

    ctx.lineWidth = brushThickness; // Используем выбранную толщину линии
    ctx.lineCap = 'round'; // Закругление концов линий
    ctx.strokeStyle = 'black'; // Цвет линии

    // Получаем координаты касания или мыши
    const rect = canvas.getBoundingClientRect();

    // Проверяем, является ли событие касанием или мышью
    let x, y;
    if (e.touches) {
        // Если это событие касания, берем координаты первого касания
        x = e.touches[0].clientX - rect.left;
        y = e.touches[0].clientY - rect.top;
    } else {
        // Если это событие мыши, берем координаты мыши
        x = e.clientX - rect.left;
        y = e.clientY - rect.top;
    }

    // Масштабируем координаты
    x *= (canvas.width / rect.width);
    y *= (canvas.height / rect.height);

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
}

// Обработчики событий для мыши
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mouseup', endDrawing);
canvas.addEventListener('mousemove', draw);

// Обработчики событий для касания
canvas.addEventListener('touchstart', startDrawing);
canvas.addEventListener('touchend', endDrawing);
canvas.addEventListener('touchmove', draw);

// Обработчик изменения толщины кисти
document.getElementById('brushThickness').addEventListener('change', (e) => {
    brushThickness = parseInt(e.target.value); // Обновляем толщину кисти
});

// Очистка холста
document.getElementById('clearButton').addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});

// Сохранение изображения
document.getElementById('saveButton').addEventListener('click', () => {
    // Создаем временный канвас
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;

    // Рисуем белый фон
    tempCtx.fillStyle = 'white';
    tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);

    // Копируем содержимое оригинального канваса
    tempCtx.drawImage(canvas, 0, 0);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Получаем данные изображения
    const imageData = tempCanvas.toDataURL('image/png');
    fetch('/save-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success == false) {
            alert('Ошибка при сохранении изображения.');;
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
});