import os

def validate_annotations(label_dir, num_classes):
    errors = []
    for root, _, files in os.walk(label_dir):
        for file in files:
            if file.endswith('.txt'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) != 5:
                            errors.append(f"{filepath}: Invalid format -> {line.strip()}")
                            continue
                        class_id = int(parts[0])
                        if class_id < 0 or class_id >= num_classes:
                            errors.append(f"{filepath}: Invalid class ID -> {class_id}")
                        for val in map(float, parts[1:]):
                            if val < 0 or val > 1:
                                errors.append(f"{filepath}: Value out of range -> {line.strip()}")
    return errors

# Configuración
num_classes = 5  # Número de clases (debe coincidir con dataset.yaml)
base_path = r"C:\Users\sopor\OneDrive\Escritorio\FINAL-PRACTICA2\BGH-CONEXION\datasets"

# Validar anotaciones
for split in ["train", "val", "test"]:
    label_dir = os.path.join(base_path, split, "labels")
    errors = validate_annotations(label_dir, num_classes)
    if errors:
        print(f"Errores en {split}:")
        for error in errors:
            print(error)
    else:
        print(f"Anotaciones de {split} válidas.")
