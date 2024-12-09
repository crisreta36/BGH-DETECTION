import os

# Función para contar imágenes
def count_images(folder, extensions=None):
    if not os.path.exists(folder):
        print(f"Ruta no encontrada: {folder}")
        return 0
    images = {os.path.splitext(file)[0] for file in os.listdir(folder) if file.endswith(extensions)}
    return images

# Función para contar etiquetas
def count_labels(folder):
    if not os.path.exists(folder):
        print(f"Ruta no encontrada: {folder}")
        return 0
    labels = {os.path.splitext(file)[0] for file in os.listdir(folder) if file.endswith('.txt')}
    return labels

# Función para contar líneas en los archivos de etiquetas válidas
def count_instances(folder, valid_labels):
    instance_count = 0
    for file in os.listdir(folder):
        base_name, ext = os.path.splitext(file)
        if ext == '.txt' and base_name in valid_labels:
            with open(os.path.join(folder, file), 'r', encoding="utf-8") as f:
                instance_count += len(f.readlines())
    return instance_count

# Rutas actualizadas
paths = {
    "train_labels": r"C:\Users\sopor\OneDrive\Escritorio\FINAL-PRACTICA2\BGH-CONEXION\datasets\train\labels",
    "train_images": r"C:\Users\sopor\OneDrive\Escritorio\FINAL-PRACTICA2\BGH-CONEXION\datasets\train\images",
    "val_labels": r"C:\Users\sopor\OneDrive\Escritorio\FINAL-PRACTICA2\BGH-CONEXION\datasets\val\labels",
    "val_images": r"C:\Users\sopor\OneDrive\Escritorio\FINAL-PRACTICA2\BGH-CONEXION\datasets\val\images",
}

# Contar imágenes y etiquetas
results = {}
for key, path in paths.items():
    if "images" in key:
        images = count_images(path, extensions=('.jpg', '.png'))
        results[key] = len(images)
    elif "labels" in key:
        image_folder_key = key.replace("labels", "images")
        valid_images = count_images(paths[image_folder_key], extensions=('.jpg', '.png'))
        labels = count_labels(path)
        valid_labels = labels.intersection(valid_images)  # Solo etiquetas válidas
        results[key] = len(valid_labels)
        

# Mostrar resultados
print("Resultados:")
for key, count in results.items():
    print(f"{key}: {count}")
