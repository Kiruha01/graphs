# Проект по графам
Задание выполнили [Лисов Кирилл](https://github.com/Kiruha01), [Григорьев Григорий](https://github.com/GrigorevGrigorii), 
[Карп Дмитрий](https://github.com/Dmitry913)

[![](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kiruha01/graphs/blob/master/graph_results.ipynb)
> Для запуска в Google Colab необходимо загрузить папку `datasets` в корень своего Google Drive

## Файлы проекта
* `graph_results.ipynb` - блокнот Jupyter Notebook с выполненым заданием 1
* `Landmarks.ipynb` - блокнот Jupyter Notebook с выполненым заданием 2
* `models.py`  - файл, содержащий реализацию графов
* `utils.py` - функции для работы с графом
* `landmarks.py` - модуль для нахождения неточного расстояния между вершинами с помощью вершин-ориентиров
* `import_datasets.py` - функции для импорта датасетов из файла
* `requirements.txt` - зависимости проекта

## Запуск проекта
Для запуска проекта необходм Python версии, не ниже `3.7`

### Установка зависимостей
В командной строке выполните 
```
pip install -r requitements.txt
```

### Запуск Jupyter
В папке проекта запустите команду
```
jupyter notebook
```
В открывшемся окне браузера откройте файл `graph_results.ipub` и запустите ячейки

## Выбор датасета
Если проект запускается локально (переменная `google_drive = False`), используются
тестовые датасеты небольших размеров (находятся в папке `test_datasets`)


## Работа с landmarks
В файле `landmarks.py` есть две реализации алгоритма - Базоввый (`LandmarksBasic`) и LCA (`LandmarksLCA`).
Для инициализации алгоритма и алгоритма необходимо выполнить:

```python
from landmarks import *

landmark = LandmarksBasic(graph, 42, SelectLandmarksMethod.RANDOM)
# или
landmark = LandmarksLCA(graph, 42, SelectLandmarksMethod.RANDOM)
```

Для выбора метода поиска вершин-ориентиров в качестве третьего аргумента необходимо передать 
один из следующих параметров
```python
from landmarks import SelectLandmarksMethod

SelectLandmarksMethod.RANDOM  # Для случайного выбора вершин-ориентиров
SelectLandmarksMethod.MAX_DEGREE  # Для выбора вершин-ориентиров с наибольшими степенями
SelectLandmarksMethod.BEST_COVERAGE  # Для выбора вершин-ориентиров с наилучшем покрытием
```

Для разработки существует ручной метод выбора:
```python
SelectLandmarksMethod.MANUAL
```
В этом случае номера необходимо ввести с клавиатуры номера вершин-ориентиров, когда система попросит об этом.

В скрипте этот метод можно использовать через потоки ввода:
```python
import io
import sys

from landmarks import SelectLandmarksMethod, LandmarksLCA

for i in range(1, 1000, 3):
    sys.stdin = io.StringIO(f"{i} {i+1} {i+2}")
    landmarks = LandmarksLCA(graph, 0, SelectLandmarksMethod.MANUAL)
```