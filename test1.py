import os
import cv2
import numpy as np
from torchvision import datasets, transforms

# Создаем директорию для сохранения изображений
output_dir = "emnist_images"
os.makedirs(output_dir, exist_ok=True)

# Загрузка датасета EMNIST (буквы и цифры)
emnist_dataset = datasets.EMNIST(
    root="./data",
    split="byclass",  # Используем 'byclass' для всех классов (цифры и буквы)
    train=True,
    download=True,
    transform=transforms.ToTensor()
)

# Сохраняем все изображения
for idx, (image_tensor, label) in enumerate(emnist_dataset):
    # Преобразуем тензор в массив NumPy
    image_np = image_tensor.squeeze().numpy()  # Убираем размерность канала (1, 28, 28) -> (28, 28)
    image_np = (image_np * 255).astype(np.uint8)  # Масштабируем до [0, 255] и преобразуем в uint8

    # Создаем поддиректорию для каждого класса
    class_name = chr(label + 65) if label < 26 else chr(label + 71)  # Преобразуем метку в символ
    class_dir = os.path.join(output_dir, class_name)
    os.makedirs(class_dir, exist_ok=True)

    # Сохраняем изображение с помощью OpenCV
    image_path = os.path.join(class_dir, f"{idx}.png")
    cv2.imwrite(image_path, image_np)

    # Выводим прогресс
    if idx % 1000 == 0:
        print(f"Сохранено {idx + 1} изображений")

print(f"Все изображения сохранены в директорию: {output_dir}")
