import cv2  # Librería para procesamiento de imágenes y video.
import tkinter as tk  # Interfaz gráfica para la aplicación.
from tkinter import messagebox, Button  # Widgets de tkinter para mostrar mensajes y botones.
from ultralytics import YOLO  # Librería YOLO para la detección de objetos.
from threading import Thread  # Para ejecutar procesos en segundo plano.

# Ruta al modelo YOLO entrenado.
MODEL_PATH = "best.pt"

# Diccionario con colores asociados a cada etiqueta.
COLOR_CODES = {
    "Amarillo-CN31": (0, 255, 255),  # Amarillo
    "Rojo-L-OUT": (0, 0, 255),       # Rojo
    "Negro-N_IN(Arriba)": (0, 0, 0), # Negro
    "Azul-N_IN(Abajo)": (255, 0, 0), # Azul
    "Marron-L-IN": (19, 69, 139)     # Marrón
}

# Conexiones esperadas: etiquetas necesarias para considerar una conexión válida.
EXPECTED_CONNECTIONS = set(COLOR_CODES.keys())

# Variable global para detener la cámara.
detener_camara = False

def visualize_predictions(frame, results, names):
    detected_labels = set()  # Conjunto para almacenar etiquetas detectadas en el frame actual.
    y_offset = 60  # Posición inicial para los mensajes de texto.

    # Iterar sobre las detecciones del modelo.
    for result in results[0].boxes.data.tolist():
        x1, y1, x2, y2, confidence, cls = result  # Coordenadas y clase de la detección.
        label = names[int(cls)]  # Nombre de la etiqueta basada en su índice.
        detected_labels.add(label)  # Agregar la etiqueta al conjunto de detectadas.
        color = COLOR_CODES.get(label, (255, 255, 255))  # Obtener el color asignado.

        # Dibujar el bounding box en el frame.
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        # Dibujar el texto con la etiqueta y la confianza.
        cv2.putText(frame, f"{label} {confidence:.2f}", (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)

    # Verificar si las conexiones detectadas coinciden con las esperadas.
    if detected_labels == EXPECTED_CONNECTIONS:
        cv2.putText(frame, "CONEXION CORRECTA", (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)
    else:
        # Mostrar las etiquetas faltantes.
        missing_labels = EXPECTED_CONNECTIONS - detected_labels
        for label in missing_labels:
            y_offset += 30  # Incrementar posición del texto.
            color = COLOR_CODES.get(label, (0, 0, 255))

            # Agregar un recuadro blanco con borde negro detrás del texto.
            text = f"Falta: {label}"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            text_x, text_y = 20, y_offset
            # Dibujar un borde negro más grande.
            cv2.rectangle(frame, (text_x - 6, text_y - text_size[1] - 6),
                          (text_x + text_size[0] + 6, text_y + 6), (0, 0, 0), -1)  # Borde negro
            # Dibujar el recuadro blanco encima del borde negro.
            cv2.rectangle(frame, (text_x - 5, text_y - text_size[1] - 5),
                          (text_x + text_size[0] + 5, text_y + 5), (255, 255, 255), -1)  # Relleno blanco
            # Dibujar el texto encima del recuadro.
            cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)


# Función para iniciar la cámara.
def iniciar_camara():
    global detener_camara
    detener_camara = False

    # Crear una ventana secundaria para la cámara.
    cam_window = tk.Toplevel()
    cam_window.title("BGH Detection - Cámara")
    cam_window.geometry("800x600")  # Tamaño de la ventana.

    # Función para detener la cámara desde el botón.
    def detener_desde_boton():
        global detener_camara
        detener_camara = True
        cam_window.destroy()

    # Botón para detener la cámara.
    btn_detener = Button(cam_window, text="Detener Cámara", font=("Arial", 16), command=detener_desde_boton)
    btn_detener.pack(pady=20)

    # Función para procesar video en segundo plano.
    def procesar_video():
        global detener_camara
        try:
            model = YOLO(MODEL_PATH)  # Cargar el modelo YOLO.
            names = {0: "Amarillo-CN31", 1: "Rojo-L-OUT", 2: "Negro-N_IN(Arriba)", 3: "Azul-N_IN(Abajo)", 4: "Marron-L-IN"}
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
            return

        # Acceder a la cámara.
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 30)  # Configurar FPS.
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Ancho.
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Alto.

        # Procesar frames mientras no se detenga la cámara.
        while not detener_camara:
            ret, frame = cap.read()
            if not ret:
                print("Error al capturar el frame.")
                break

            results = model.predict(frame, conf=0.3)  # Realizar predicciones.
            visualize_predictions(frame, results, names)  # Dibujar predicciones.

            resized_frame = cv2.resize(frame, (1280, 720))  # Ajustar tamaño.
            cv2.imshow("BGH Detection - Detección de Cables", resized_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Detener si se presiona 'q'.
                detener_camara = True
                break

        cap.release()
        cv2.destroyAllWindows()

    # Iniciar el procesamiento de video en un hilo separado.
    Thread(target=procesar_video).start()
    cam_window.mainloop()

# Función para cerrar sesión.
def cerrar_sesion(menu):
    if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de cerrar la sesión?"):
        menu.destroy()

# Menú principal.
def mostrar_menu():
    menu = tk.Tk()
    menu.title("BGH Detection - Menú Principal")
    menu.geometry("600x400")

    # Botón para iniciar la cámara.
    btn_iniciar_cam = tk.Button(menu, text="Iniciar Cámara", font=("Arial", 14), command=iniciar_camara)
    btn_iniciar_cam.pack(pady=10)

    # Botón para ver registros fallidos.
    btn_fallidos = tk.Button(menu, text="Registros Fallidos", font=("Arial", 14), command=lambda: messagebox.showinfo("Registros", "Funcionalidad en desarrollo"))
    btn_fallidos.pack(pady=10)

    # Botón para ver detecciones correctas.
    btn_correctos = tk.Button(menu, text="Detecciones Correctas", font=("Arial", 14), command=lambda: messagebox.showinfo("Registros", "Funcionalidad en desarrollo"))
    btn_correctos.pack(pady=10)

    # Botón para cerrar sesión.
    btn_cerrar_sesion = tk.Button(menu, text="Cerrar Sesión y Salir", font=("Arial", 14), command=lambda: cerrar_sesion(menu))
    btn_cerrar_sesion.pack(pady=20)

    menu.mainloop()

# Validar login.
def validate_login():
    username = entry_user.get()
    password = entry_pass.get()
    if username == "BGH" and password == "12345":
        messagebox.showinfo("Login Correcto", "Bienvenido a BGH Detection")
        root.destroy()
        mostrar_menu()
    else:
        messagebox.showerror("Error", "Credenciales Incorrectas")

# Crear ventana de login.
root = tk.Tk()
root.title("BGH Detection - Login")
root.geometry("400x300")

# Elementos del login.
label_user = tk.Label(root, text="Usuario", font=("Arial", 14))
label_user.pack(pady=10)
entry_user = tk.Entry(root, font=("Arial", 14), width=20)
entry_user.pack(pady=10)

label_pass = tk.Label(root, text="Contraseña", font=("Arial", 14))
label_pass.pack(pady=10)
entry_pass = tk.Entry(root, show="*", font=("Arial", 14), width=20)
entry_pass.pack(pady=10)

btn_login = tk.Button(root, text="Iniciar Sesión", font=("Arial", 14), command=validate_login)
btn_login.pack(pady=20)

# Iniciar la aplicación con el bucle principal de Tkinter.
root.mainloop()
