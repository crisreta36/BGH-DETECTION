import os

def check_labels(folder, num_classes):
    errors = []
    for file in os.listdir(folder):
        if file.endswith('.txt'):
            path = os.path.join(folder, file)
            with open(path, 'r') as f:
                for line in f:
                    cls = int(line.split()[0])  # Primera columna es la clase
                    if cls >= num_classes:
                        errors.append((file, cls))
    return errors

# Rutas ajustadas
train_correct_labels = r"C:\Users\sopor\OneDrive\Escritorio\FINAL-PRACTICA2\BGH-CONEXION\datasets\train\labels"
val_correct_labels = r"C:\Users\sopor\OneDrive\Escritorio\FINAL-PRACTICA2\BGH-CONEXION\datasets\val\labels"


num_classes = 5  # Según dataset.yaml

# Verificar errores en las carpetas train y val 
train_correct_errors = check_labels(train_correct_labels, num_classes)
val_correct_errors = check_labels(val_correct_labels, num_classes)


# Mostrar resultados
print("Errores en entrenamiento :", train_correct_errors)
print("Errores en validación :", val_correct_errors)

