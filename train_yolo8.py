from ultralytics import YOLO

def main():
    model = YOLO('yolov8m.pt')  # Carga el modelo YOLO
    model.train(
        data='dataset.yaml',  # Archivo de configuración del dataset
        epochs=100,            # Número de épocas
        batch=16,             # Tamaño del batch
        imgsz=640,            # Tamaño de las imágenes
        save=True,            # Asegura que los pesos se guarden
        save_period=1,        # Guarda los pesos después de cada época
        project="runs/detect", # Carpeta de salida
        name='cable_detector'
    )

if __name__ == "__main__":
    main()
