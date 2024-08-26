import os
import re
import numpy as np
import matplotlib.pyplot as plt
import math

# Путь к папке с .dat файлами
folder_path = r'C:\Users\User\Documents\VSCode\HysteresisVisualization\data' 

# Список всех .dat файлов в папке
files = [f for f in os.listdir(folder_path) if f.endswith('.dat')]

# Функция для извлечения значения между "T=" и "C"
def extract_T_value(file_name):
    match = re.search(r'T=(.*?)C', file_name)
    return float(match.group(1)) if match else float('inf')

# Сортировка файлов по значению T
files.sort(key=extract_T_value)

# Нормировка всех графиков по максимальному значению сигнала + 10%
global_max_val = -float('inf')
for file_name in files:
    file_path = os.path.join(folder_path, file_name)
    data = np.loadtxt(file_path)
    max_val = np.max(data[:, 1])
    if max_val > global_max_val:
        global_max_val = max_val
global_max_val += global_max_val * 0.1

# Определение количества строк и столбцов для подграфиков
n_files = len(files)
if not math.sqrt(n_files) == round(math.sqrt(n_files)):
    cols = int((math.sqrt(n_files))) + 1
else:
    cols = int(math.sqrt(n_files))
rows = (n_files + cols - 1) // cols  # Количество строк зависит от количества файлов

# Создание глобальной фигуры и массива подграфиков
plt.style.use('seaborn-v0_8-whitegrid')
fig, axs = plt.subplots(rows, cols, layout='constrained')

for i, file_name in enumerate(files):
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
            
        # Определение смещения, чтобы центрировать график
        shift = (max_val + min_val) / 2
            
        # Смещение всех значений второй колонки для центрирования относительно 0
        data[:, 1] -= shift
        print(np.min(data[:, 1]), np.max(data[:, 1]))

        # Извлечение части названия файла между "T=" и "C"
        plot_label = extract_T_value(file_name)

        # Определение позиции текущего подграфика
        ax = axs[i // cols, i % cols] if rows > 1 else axs[i % cols]
        
        # Строим график на подграфике
        ax.plot(data[:, 0], data[:, 1], label=f'T={plot_label}')

        # Настраиваем оси и заголовок для подграфика
        ax.set_xlabel('H (mT)')
        ax.set_ylabel('Signal (V)')
        #ax.set_title(f'{file_name}')
        ax.legend()

        # Устанавливаем одинаковый масштаб по оси Y
        ax.set_ylim(-global_max_val, global_max_val)

    except Exception as e:
        print(f"Произошла ошибка при обработке файла {file_name}: {e}")

# Отключение пустых подграфиков, если они есть
for j in range(i + 1, rows * cols):
    fig.delaxes(axs[j // cols, j % cols] if rows > 1 else axs[j % cols])

# Настройка общих параметров фигуры
#plt.tight_layout()
plt.show()
