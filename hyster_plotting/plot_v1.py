import os
import re
import numpy as np
import matplotlib.pyplot as plt
import math

# Путь к папке с .dat файлами
folder_path = r'C:\Users\User\Documents\VSCode\HysteresisVisualization\data' 

# Список всех .dat файлов в папке
files = [f for f in os.listdir(folder_path) if f.endswith('.dat')]

# Создание фигуры для графика/ов
plt.figure()
plt.style.use('seaborn-v0_8-whitegrid')

# Обрабатываем каждый файл по очереди
for file_name in files:
    file_path = os.path.join(folder_path, file_name)
    
    try:
        # Чтение данных из файла
        data = np.loadtxt(file_path)

        # Преобразование А в mT
        data[:, 0] = -0.0546 * (data[:, 0] ** 3) + 0.0154 * (data[:, 0] ** 2) + 48.153 * data[:, 0]

        # Нормализация второй колонки для приведения модулей минимального и максимального значений к одинаковому значению
        min_val = np.min(data[:, 1])
        max_val = np.max(data[:, 1])
        print(min_val, max_val)
        
         # Определяем смещение, чтобы центрировать график
        shift = (max_val + min_val) / 2
        
        # Смещение всех значений второй колонки для центрирования относительно 0
        data[:, 1] -= shift
        print(np.min(data[:, 1]), np.max(data[:, 1]))

        # Извлечение части названия файла между "T=" и "C" с помощью регулярного выражения
        match = re.search(r'T=(.*?)C', file_name)
        if match:
            plot_label = match.group(1)
        else:
            plot_label = file_name  # Если не удалось извлечь, использовать имя файла целиком

        # Добавление данных на общий график
        plt.plot(data[:, 0], data[:, 1], label=f'{plot_label} C')

    except Exception as e:
        print(f"Произошла ошибка при обработке файла {file_name}: {e}")


plt.xlabel('External Field (mT)')
plt.ylabel('Signal (V)')
plt.title('График данных из всех файлов .dat')
plt.legend()
plt.show()




