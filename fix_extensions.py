import os

folder = 'static/tarot'

for filename in os.listdir(folder):
    if filename.endswith('.JPG'):
        base = os.path.splitext(filename)[0]
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, base + '.jpg')
        os.rename(old_path, new_path)
        print(f'Renamed: {filename} -> {base}.jpg')
