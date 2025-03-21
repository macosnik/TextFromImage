import os
import cv2
import numpy as np
from torchvision import datasets, transforms

# Создаем директорию для сохранения изображений
output_dir = "mnist_images"
os.makedirs(output_dir, exist_ok=True)

# Загрузка датасета MNIST
mnist_dataset = datasets.MNIST(root="./data", train=True, download=True, transform=transforms.ToTensor())

# Сохраняем все изображения
for idx, (image_tensor, label) in enumerate(mnist_dataset):
    # Преобразуем тензор в массив NumPy
    image_np = image_tensor.squeeze().numpy()  # Убираем размерность канала (1, 28, 28) -> (28, 28)
    image_np = (image_np * 255).astype(np.uint8)  # Масштабируем до [0, 255] и преобразуем в uint8

    # Создаем поддиректорию для каждого класса (цифры от 0 до 9)
    class_dir = os.path.join(output_dir, str(label))
    os.makedirs(class_dir, exist_ok=True)

    # Сохраняем изображение с помощью OpenCV
    image_path = os.path.join(class_dir, f"{idx}.png")
    cv2.imwrite(image_path, image_np)

    # Выводим прогресс
    if idx % 1000 == 0:
        print(f"Сохранено {idx + 1} изображений")

print(f"Все изображения сохранены в директорию: {output_dir}")