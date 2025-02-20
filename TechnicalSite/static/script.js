const canvas = document.getElementById('drawingCanvas');
const wayDrawing = canvas.getContext('2d');
let drawing = false;
let brushSize = 50;

function startDrawing(e) {
    drawing = true;
    draw(e);
}
function endDrawing() {
    drawing = false;
    wayDrawing.beginPath();
}
function draw(e) {
    if (!drawing) {
        return;
    }
    wayDrawing.lineWidth = brushSize;
    wayDrawing.lineCap = 'round';
    wayDrawing.strokeStyle = 'white';

    const rect = canvas.getBoundingClientRect();
    let x, y;

    if (e.touches) {
        x = e.touches[0].clientX - rect.left;
        y = e.touches[0].clientY - rect.top;
    }
    else {
        x = e.clientX - rect.left;
        y = e.clientY - rect.top;
    }
    x *= (canvas.width / rect.width);
    y *= (canvas.height / rect.height);

    wayDrawing.lineTo(x, y);
    wayDrawing.stroke();
    wayDrawing.beginPath();
    wayDrawing.moveTo(x, y);
}

function updateImageCount() {
    const folder = document.getElementById('folderSelect').value;

    fetch(`/get-image-count?folder=${encodeURIComponent(folder)}`)
        .then(response => response.json())

        .then(data => {
            document.getElementById('imageCount').textContent = data.count;
        })

        .catch(error => console.error('Error:', error));
}
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mouseup', endDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('touchstart', startDrawing);
canvas.addEventListener('touchend', endDrawing);
canvas.addEventListener('touchmove', draw);

document.getElementById('brushThickness').addEventListener('change', (e) => {
    brushSize = parseInt(e.target.value);
});

document.getElementById('clearButton').addEventListener('click', () => {
    wayDrawing.clearRect(0, 0, canvas.width, canvas.height);
});

document.addEventListener('DOMContentLoaded', updateImageCount);
document.getElementById('folderSelect').addEventListener('change', updateImageCount);

document.getElementById('saveButton').addEventListener('click', () => {
    const folder = document.getElementById('folderSelect').value;
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');

    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    tempCtx.fillStyle = 'black';
    tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
    tempCtx.drawImage(canvas, 0, 0);

    wayDrawing.clearRect(0, 0, canvas.width, canvas.height);

    const imageData = tempCanvas.toDataURL('image/png');

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
            updateImageCount();
        }
    })
    .catch(error => console.error('Error:', error));
});