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
    wayDrawing.strokeStyle = 'white';

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

// Функция для обновления счетчика изображений
function updateImageCount() {
    const folder = document.getElementById('folderSelect').value;

    fetch(`/get-image-count?folder=${encodeURIComponent(folder)}`)
        .then(response => response.json())

        .then(data => {
            document.getElementById('imageCount').textContent = data.count;
        })

        .catch(error => console.error('Error:', error));
}

// События для мыши:

// Рисование при нажатии кнопки мыши
canvas.addEventListener('mousedown', startDrawing);

// Рисования при отпускании кнопки мыши
canvas.addEventListener('mouseup', endDrawing);

// Рисование при движении мыши
canvas.addEventListener('mousemove', draw);

// События для касания:

// Рисование при касании
canvas.addEventListener('touchstart', startDrawing);

// Рисование при отпускании касания
canvas.addEventListener('touchend', endDrawing);

// Рисование при движении касания
canvas.addEventListener('touchmove', draw);

// Изменения толщины кисти
document.getElementById('brushThickness').addEventListener('change', (e) => {
    // Обновление толщины кисти
    brushSize = parseInt(e.target.value);
});

// Очистка холста
document.getElementById('clearButton').addEventListener('click', () => {
    // Очищаем холст
    wayDrawing.clearRect(0, 0, canvas.width, canvas.height);
});

// Обновляем счетчик при загрузке страницы
document.addEventListener('DOMContentLoaded', updateImageCount);

// Обновляем счетчик при изменении выбора папки
document.getElementById('folderSelect').addEventListener('change', updateImageCount);

document.getElementById('saveButton').addEventListener('click', () => {
    const folder = document.getElementById('folderSelect').value;

    // Создаем временный холст
    const tempCanvas = document.createElement('canvas');

    // Для нового холста задаём 2d пространство
    const tempCtx = tempCanvas.getContext('2d');

    // Устанавливаем ширину временного холста
    tempCanvas.width = canvas.width;

    // Устанавливаем высоту временного холста
    tempCanvas.height = canvas.height;

    // Белый фон на временном холсте
    tempCtx.fillStyle = 'black'; // Устанавливаем цвет фона

    // Заполняем фон белым цветом
    tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);

    // Копируем содержимое оригинального холста на временный холст
    tempCtx.drawImage(canvas, 0, 0);

    // Очищаем оригинальный холст
    wayDrawing.clearRect(0, 0, canvas.width, canvas.height);

    // Данные изображения в формате PNG
    const imageData = tempCanvas.toDataURL('image/png');

    // Отправляем данные изображения на компьютер
    fetch('/save-image', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            image: imageData,
            folder: folder
        }),
    })

    .then(response => {
        if (response.ok) {
            updateImageCount(); // Добавляем обновление счетчика
        }
    })

    .catch(error => console.error('Error:', error));
});