const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
let drawing = false;

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

    ctx.lineWidth = 5; // Толщина линии
    ctx.lineCap = 'round'; // Закругление концов линий
    ctx.strokeStyle = 'black'; // Цвет линии

    // Получаем координаты касания или мыши
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left || e.touches[0].clientX - rect.left;
    const y = e.clientY - rect.top || e.touches[0].clientY - rect.top;

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

// Очистка холста
document.getElementById('clearButton').addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});

// Сохранение изображения
document.getElementById('saveButton').addEventListener('click', () => {
    const imageData = canvas.toDataURL('image/png');
    fetch('/save-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Изображение успешно сохранено!');
        } else {
            alert('Ошибка при сохранении изображения.');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
});