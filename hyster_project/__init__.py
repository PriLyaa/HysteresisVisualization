import os
import numpy as np
import matplotlib.pyplot as plt
import math

# Путь к папке с .dat файлами
folder_path = r'C:\Users\User\Documents\VSCode\HysteresisVisualization\data' 

# Список всех .dat файлов в папке
files = [f for f in os.listdir(folder_path) if f.endswith('.dat')]

# Создание фигуры для графика/ов
plt.figure()

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
        #print(min_val, max_val)
        max_mod = max(abs(min_val), abs(max_val))
        data[:, 1] = np.interp(data[:, 1], [min_val, max_val], [-max_mod, max_mod])
        #print(np.min(data[:, 1]), np.max(data[:, 1]))

        # Добавление данных на общий график
        plt.plot(data[:, 0], data[:, 1], label=file_name)

    except Exception as e:
        print(f"Произошла ошибка при обработке файла {file_name}: {e}")


plt.xlabel('External Field (mT)')
plt.ylabel('Signal (V)')
plt.title('График данных из всех файлов .dat')
plt.legend()
plt.show()




