# **Автоматизация рутинных задач**

В мире, в котором мы живём, учимся, работаем, многие стремятся добиться автоматизации, облегчения рутинной работы, что достигается в большинстве благодаря компьютерным программам🤖. Люди, на своём подобии, в стремлении к автоматизации рутинных задач, придумали математическое строение нейронной сети, которое повседневно используется в разных сферах, от подбора рекомендаций видео в _VK видео_ до расчётов и анализов космических кораблей.

###### Работа с изображениями

Для реализации обучения нейронной сети, а также использования готового продукта, требуется модуль, для чтения и обработки изображений. В данном проекте, был написан `image_utils` модуль для работы с изображениями. Он поддерживает функции чтения, масштабирования, рисования, сохранения и представления изображения в чёрно-белом виде. Описание каждой функции модуля ниже👇

`load` - 
функция для чтения изображения. Функция читает только bmp файлы, а поэтому на вход поступает имя файла, с помощью которого программа, используя терминал (через `os.system`), преобразует любой формат изображения в bmp (при условии, если файл токовым не является). После этого, следует узнать размеры изображения, которые можно узнать, зная структуру bmp файлов:

![icon.png](TechnicalSite/static/icon.png)
![struct_bmp.jpg](Materials/struct_bmp.jpg)
