# Проект по графам
Задание выполнили [Лисов Кирилл](https://github.com/Kiruha01), [Григорьев Григорий](https://github.com/GrigorevGrigorii), 
[Карп Дмитрий](https://github.com/Dmitry913)

[![](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kiruha01/graphs/blob/master/graph_results.ipynb)
> Для запуска в Google Colab необходимо загрузить папку `datasets` в корень своего Google Drive

## Файлы проекта
* `graph_results.ipub` - блокнот Jupyter Notebook с выполненым заданием
* `NetworkX_compare.ipub` - блокнот, сравнивающий время работы наших алгоритмов с networkX
* `models.py`  - файл, содержащий реализацию графов
* `utils.py` - функции для работы с графом
* `import_datasets.py` - функции для импорта датасетов из файла
* `requirements.txt` - зависимости проекта
* `pickles` - файлы с просчитанными результатами работы алгоритмов. 
Загружаются с помощью модуля `pickle`

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
