import os
import pandas as pd

# Путь к папке с изображениями
folder = "static/tarot"

# Получаем список всех .jpg файлов
file_list = [f for f in os.listdir(folder) if f.lower().endswith(".jpg")]

# Сохраняем в CSV
df = pd.DataFrame(file_list, columns=["filename"])
df.to_csv("current_filenames.csv", index=False)

print("Файл сохранён как current_filenames.csv")
