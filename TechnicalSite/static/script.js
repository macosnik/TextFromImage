const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');

// Установка размеров холста
canvas.width = 500;
canvas.height = 500;

let isDrawing = false;
let lastX = 0;
let lastY = 0;

// Обработка рисования
function draw(e) {
    if (!isDrawing) return; // Рисуем только при нажатии мыши
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 5;
    ctx.stroke();
    [lastX, lastY] = [e.offsetX, e.offsetY];
}

// Слушатели событий
canvas.addEventListener('mousedown', (e) => {
    isDrawing = true;
    [lastX, lastY] = [e.offsetX, e.offsetY];
});
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', () => isDrawing = false);
canvas.addEventListener('mouseout', () => isDrawing = false);

// Обработка сохранения
document.getElementById('saveButton').addEventListener('click', async () => {
    const dataURL = canvas.toDataURL('image/png'); // Преобразуем холст в Base64
    const response = await fetch('/save-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: dataURL })
    });
    const result = await response.json();
    if (result.success) {
        alert('Изображение сохранено!');
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Очистка холста
    } else {
        alert('Ошибка сохранения.');
    }
});