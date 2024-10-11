import platform
import subprocess
import tkinter as tk
from tkinter import Listbox, messagebox
from tkinter import PhotoImage
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
from PIL import Image, ImageTk
import time
import os
import psutil
import webbrowser
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities
from pycaw.pycaw import IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'Aplicaciones'))
# Función que se ejecuta después de mostrar la pantalla principal
def mostrar_alerta_Inicial():
    messagebox.showinfo("Recordatorio", "Hola Bienvenido al sistema operativo \nAngora OS")

# Ruta del archivo de credenciales
archivo_credenciales = "Credenciales/Credenciales.txt"
archivo_fondo = "fondo.txt"

# Función para cargar la ruta del fondo de pantalla desde un archivo
def cargar_fondo():
    if os.path.exists(archivo_fondo):
        with open(archivo_fondo, "r") as archivo:
            ruta_fondo = archivo.readline().strip()
            if os.path.exists(ruta_fondo):  # Verifica que el archivo exista
                return ruta_fondo
    return "FondosPantalla/Fondo.JPEG"  # Ruta predeterminada si no se encuentra el archivo

# Función para guardar la ruta del fondo de pantalla en un archivo
def guardar_fondo(ruta_fondo):
    with open(archivo_fondo, "w") as archivo:
        archivo.write(ruta_fondo)

# Función para cargar credenciales desde un archivo
def cargar_credenciales():
    if os.path.exists(archivo_credenciales):
        with open(archivo_credenciales, "r") as archivo:
            lineas = archivo.readlines()
            if len(lineas) >= 2:  # Asegurarse de que el archivo tenga al menos 2 líneas
                usuario = lineas[0].strip()
                contrasena = lineas[1].strip()
                return usuario, contrasena
            else:
                # Si el archivo está incompleto o vacío, se devuelven los valores por defecto
                return "admin", "123"
    else:
        return "admin", "123"  # Valores por defecto si no existe el archivo


# Función para guardar credenciales en un archivo
def guardar_credenciales(usuario, contrasena):
    with open(archivo_credenciales, "w") as archivo:
        archivo.write(f"{usuario}\n{contrasena}")

# Cargar las credenciales al iniciar la aplicación
usuario_actual, contrasena_actual = cargar_credenciales()


# Función que se ejecuta al hacer login
def iniciar_sesion():
    global usuario_actual, contrasena_actual
    
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if usuario == usuario_actual and contrasena == contrasena_actual:
        ventana_login.destroy()  # Cierra la ventana de login
        mostrar_pantalla_principal()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Función para mostrar la pantalla principal
def mostrar_pantalla_principal():
    global label_fondo_principal, ventana_principal, imagen_fondo_principal_tk
    global RecMedicamento, RecComida, lista_aplicaciones, aplicaciones
    ventana_principal = tk.Tk()
    ventana_principal.title("Pantalla Principal")
    ventana_principal.geometry("1280x720")
    
    
     # Cargar imagen de fondo para la pantalla principal desde el archivo
    ruta_fondo = cargar_fondo()
    imagen_fondo_principal = Image.open(ruta_fondo)
    imagen_fondo_principal = imagen_fondo_principal.resize((1280, 720), Image.LANCZOS)
    imagen_fondo_principal_tk = ImageTk.PhotoImage(imagen_fondo_principal)

    # Crear un Label para la imagen de fondo
    label_fondo_principal = tk.Label(ventana_principal, image=imagen_fondo_principal_tk)
    label_fondo_principal.place(x=0, y=0, relwidth=1, relheight=1)

    # Barra de tareas con botones centrados
    barra_tareas = tk.Frame(ventana_principal, bg="#99ACF5", height=50)
    barra_tareas.pack(side="top", fill="x")

    # Crear un Frame para contener los botones y centrarlo en la barra de tareas
    contenedor_botones = tk.Frame(barra_tareas, bg="#99ACF5")
    contenedor_botones.pack(side="left", padx=350)

    # Cargar las imágenes para los botones
    imagen1 = ImageTk.PhotoImage(Image.open("Imagenes/InstaFitBg.PNG").resize((30, 30), Image.LANCZOS))  # Cambia a la imagen que quieras
    imagen2 = ImageTk.PhotoImage(Image.open("Imagenes/ConfiguracionBg.PNG").resize((30, 30), Image.LANCZOS))
    imagen3 = ImageTk.PhotoImage(Image.open("Imagenes/LogoAngoraOsNBG.PNG").resize((40, 40), Image.LANCZOS))  # Botón central más grande
    imagen4 = ImageTk.PhotoImage(Image.open("Imagenes/GestorArchivosBg.PNG").resize((30, 30), Image.LANCZOS))
    imagen5 = ImageTk.PhotoImage(Image.open("Imagenes/NavegadorBg.PNG").resize((30, 30), Image.LANCZOS))
    icono1 = ImageTk.PhotoImage(Image.open("Imagenes/SonidoBg.PNG").resize((20, 20), Image.LANCZOS))  # Cambia a la imagen que quieras
    icono2 = ImageTk.PhotoImage(Image.open("Imagenes/WifiBg.PNG").resize((20, 20), Image.LANCZOS))
    icono3 = ImageTk.PhotoImage(Image.open("Imagenes/CargaBg.PNG").resize((20, 20), Image.LANCZOS))
    

    # Crear etiquetas con los textos solicitados
    label_color = "#a3b6ff"  # Color de fondo similar al de la imagen

    RecMedicamento = tk.Label(ventana_principal, text="No olvides tomarte tu medicamento (remdesivir)", bg="#a3b6ff", font=("Arial", 12), width=40, height=6)
    RecMedicamento.place(x=850, y=150)
    

    RecComida = tk.Label(ventana_principal, text="No olvides almorzar a las 2:00 pm", bg=label_color, font=("Arial", 12), width=40, height=6)
    RecComida.place(x=850, y=300)

    RecAgua = tk.Label(ventana_principal, text="No olvides hidratarte, toma agua", bg=label_color, font=("Arial", 12), width=40, height=6)
    RecAgua.place(x=850, y=450)

    # Crear botones sin texto, sólo con imágenes
    BInstafit = tk.Button(contenedor_botones, image=imagen1, bg="#99ACF5", width=30, height=30,command=abrir_pagina)
    BInstafit .pack(side="left", padx=10)

    BConfiguracion = tk.Button(contenedor_botones, image=imagen2, bg="#99ACF5", width=30, height=30, command=abrir_configuracion)
    BConfiguracion.pack(side="left", padx=10)

    boton_central = tk.Button(contenedor_botones, image=imagen3, bg="#99ACF5", width=40, height=40, command=abrir_pagina_opciones)
    boton_central.pack(side="left", padx=10)

    BGestorArchivos = tk.Button(contenedor_botones, image=imagen4, bg="#99ACF5", width=30, height=30, command=administrador_archivos)
    BGestorArchivos.pack(side="left", padx=10)

    BNavegador = tk.Button(contenedor_botones, image=imagen5, bg="#99ACF5", width=30, height=30, command=abrir_navegador)
    BNavegador.pack(side="left", padx=10)

    # Crear botones con imágenes en la parte izquierda
    imagen_word = ImageTk.PhotoImage(Image.open("Imagenes/Word.PNG").resize((50, 50), Image.LANCZOS))
    imagen_excel = ImageTk.PhotoImage(Image.open("Imagenes/Excel.PNG").resize((50, 50), Image.LANCZOS))
    imagen_powerpoint = ImageTk.PhotoImage(Image.open("Imagenes/PowerPoint.PNG").resize((50, 50), Image.LANCZOS))
    imagen_calculadora = ImageTk.PhotoImage(Image.open("Imagenes/Calculadora.PNG").resize((50, 50), Image.LANCZOS))

    # Crear los botones en la parte izquierda
    BWord = tk.Button(ventana_principal, image=imagen_word, bg="#c280c0", command=abrir_word)
    BWord.place(x=20, y=100)

    BExcel = tk.Button(ventana_principal, image=imagen_excel, bg="#c280c0",command=abrir_excel)
    BExcel.place(x=20, y=180)

    BPowerPoint = tk.Button(ventana_principal, image=imagen_powerpoint, bg="#c280c0",command=abrir_powerpoint)
    BPowerPoint.place(x=20, y=260)

    BCalculadora = tk.Button(ventana_principal, image=imagen_calculadora, bg="#c280c0",command=abrir_calculadora)
    BCalculadora.place(x=20, y=340)

    aplicaciones = ['Word', 'Excel', 'PowerPoint', 'Calculadora', 'Navegador']

    # Botón para abrir la ventana con la lista de aplicaciones
    btn_abrir_lista = tk.Button(ventana_principal, text="Abrir Lista de Aplicaciones", command=abrir_ventana_aplicaciones, bg="#99ACF5")
    btn_abrir_lista.place(x=10, y=2, width=150, height=45)

    # Mostrar la hora en tiempo real en la barra de tareas
    etiqueta_hora = tk.Label(barra_tareas, bg="#99ACF5", fg="black", font=("Arial", 12))
    etiqueta_hora.pack(side="right", padx=10)
    actualizar_recordatorio_medicamento()
    actualizar_horario_comida()
    
    

    # Función para actualizar la hora
    def actualizar_hora():
        hora_actual = time.strftime("%H:%M:%S")
        etiqueta_hora.config(text=hora_actual)
        ventana_principal.after(1000, actualizar_hora)

    actualizar_hora()  # Llamar la función por primera vez


    
    # Agregar tres iconos adicionales a la derecha de la barra de tareas
    Bonido = tk.Button(barra_tareas, image=icono1, bg="#99ACF5", width=20, height=20, command=volumen)
    Bonido.pack(side="right", padx=10)

    BWIfi = tk.Button(barra_tareas, image=icono2, bg="#99ACF5", width=20, height=20, command=Mostrar_wifi)
    BWIfi.pack(side="right", padx=10)

    BCarga = tk.Button(barra_tareas, image=icono3, bg="#99ACF5", width=20, height=20,command=revisar_bateria)
    BCarga.pack(side="right", padx=10)

    #ventana_principal.after(1000, mostrar_alerta_Inicial)  # Muestra la alerta después de 1 segundo
    ventana_principal.mainloop()

def revisar_bateria():
    # Obtener información de la batería
    bateria = psutil.sensors_battery()
    porcentaje = bateria.percent

    # Determinar el mensaje según el nivel de batería
    if porcentaje >= 60:
        mensaje = f"El nivel de batería es óptimo: {porcentaje}%. No se necesita cargar."
    elif 30 <= porcentaje < 60:
        mensaje = f"El nivel de batería es normal: {porcentaje}%. No se recomienda cargar todavía."
    else:
        mensaje = f"El nivel de batería es bajo: {porcentaje}%. Recomendamos comenzar a cargar lo más pronto posible."

    # Crear ventana emergente
    ventana = tk.Tk()
    ventana.withdraw()  # Ocultar ventana principal

    # Mostrar mensaje del nivel de batería
    messagebox.showinfo("Estado de la batería", mensaje)
    
    # Cerrar ventana después de 10 segundos
    ventana.after(10000, ventana.destroy)


# Función que abre la página de opciones con cuatro botones
def abrir_pagina_opciones():
    ventana_opciones = tk.Toplevel()
    ventana_opciones.title("Opciones")
    ventana_opciones.geometry("1280x720")
    ventana_opciones.configure(bg="#B5C2F4")

    # Etiqueta "Menu principal" más grande
    etiqueta_menu = tk.Label(ventana_opciones, text="Menu principal", bg="#B5C2F4", font=("Arial", 24, "bold"))
    etiqueta_menu.place(x=500, y=50)  # Centra la etiqueta un poco más en la parte superior

    # Tamaño ajustado para los botones normales
    button_width = 35
    button_height = 3

    # Tamaño ajustado para los botones con imágenes (más pequeños)
    image_button_width = 50
    image_button_height = 50

    # Botones con texto (más grandes)
    boton_agregar_datos = tk.Button(ventana_opciones, text="Agregar datos personales", bg="#99ACF5", command=abrir_formulario, width=button_width, height=button_height)
    boton_agregar_datos.place(x=300, y=150)

    boton_configurar_datos = tk.Button(ventana_opciones, text="Configurar datos personales", bg="#99ACF5", command=abrir_formulario_configurar, width=button_width, height=button_height)
    boton_configurar_datos.place(x=850 , y =150)

    boton_datos_especificos = tk.Button(ventana_opciones, text="Agregar Medicamentos", command=abrir_datos_especificos, bg="#99ACF5", width=button_width, height=button_height)
    boton_datos_especificos.place(x=300 , y =250)

    boton_ver_datos = tk.Button(ventana_opciones, text="Verificar datos", bg="#99ACF5", command=ver_datos_usuario_y_medicamentos, width=button_width, height=button_height)
    boton_ver_datos.place(x=850 , y =250)

    boton_agregar_horario = tk.Button(ventana_opciones, text="Agregar/Editar Horario de Comidas", bg="#99ACF5", command=abrir_formulario_horario, width=button_width, height=button_height)
    boton_agregar_horario.place(x=300 , y =350)

    boton_ver_horario = tk.Button(ventana_opciones, text="Ver Horario de Comidas", bg="#99ACF5", command=ver_horario_comidas, width=button_width, height=button_height)
    boton_ver_horario.place(x=850 , y =350)

    # Botones con imágenes más pequeños
    imagen1 = PhotoImage(file="Imagenes/AgregarDatosBg.PNG")
    boton_imagen_agregar_datos = tk.Button(ventana_opciones, image=imagen1, bg="#99ACF5", command=abrir_formulario, width=image_button_width, height=image_button_height)
    boton_imagen_agregar_datos.image = imagen1
    boton_imagen_agregar_datos.place(x=200, y=150)

    imagen2 = PhotoImage(file="Imagenes/CambiarDatosBg.PNG")
    boton_imagen_configurar_datos = tk.Button(ventana_opciones, image=imagen2, bg="#99ACF5", command=abrir_formulario_configurar, width=image_button_width, height=image_button_height)
    boton_imagen_configurar_datos.image = imagen2
    boton_imagen_configurar_datos.place(x=750, y=150)

    imagen3 = PhotoImage(file="Imagenes/AgregarMedicinasBg.PNG")
    boton_imagen_datos_especificos = tk.Button(ventana_opciones, image=imagen3, bg="#99ACF5", command=abrir_datos_especificos, width=image_button_width, height=image_button_height)
    boton_imagen_datos_especificos.image = imagen3
    boton_imagen_datos_especificos.place(x=200, y=250)

    imagen4 = PhotoImage(file="Imagenes/VerificarDatosBg.PNG")
    boton_imagen_ver_datos = tk.Button(ventana_opciones, image=imagen4, bg="#99ACF5", command=ver_datos_usuario_y_medicamentos, width=image_button_width, height=image_button_height)
    boton_imagen_ver_datos.image = imagen4
    boton_imagen_ver_datos.place(x=750, y=250)

    imagen5 = PhotoImage(file="Imagenes/HorariosComidaBg.PNG")
    boton_imagen_agregar_horario = tk.Button(ventana_opciones, image=imagen5, bg="#99ACF5", command=abrir_formulario_horario, width=image_button_width, height=image_button_height)
    boton_imagen_agregar_horario.image = imagen5
    boton_imagen_agregar_horario.place(x=200, y=350)

    imagen6 = PhotoImage(file="Imagenes/VerificarHorariosComidasBg.PNG")
    boton_imagen_ver_horario = tk.Button(ventana_opciones, image=imagen6, bg="#99ACF5", command=ver_horario_comidas, width=image_button_width, height=image_button_height)
    boton_imagen_ver_horario.image = imagen6
    boton_imagen_ver_horario.place(x=750, y=350)

# Función para abrir una ventana y mostrar los datos de usuario y medicamentos

def ver_datos_usuario_y_medicamentos():
    ventana_ver_datos = tk.Toplevel()
    ventana_ver_datos.title("Ver Datos")
    ventana_ver_datos.geometry("1280x720")
    ventana_ver_datos.configure(bg="#B5C2F4")

    # Mostrar datos de usuario
    try:
        with open("Credenciales/datos_usuario.txt", "r") as archivo_usuario:
            datos_usuario = archivo_usuario.read()
    except FileNotFoundError:
        datos_usuario = "No se encontraron datos de usuario."

    # Etiqueta de "Datos de Usuario"
    label_datos_usuario = tk.Label(ventana_ver_datos, text="Datos de Usuario", font=("Arial", 16, "bold"), bg="#8E9EC6", fg="black")
    label_datos_usuario.pack(pady=20)

    # Cuadro de texto para los datos de usuario
    texto_datos_usuario = tk.Text(ventana_ver_datos, height=10, width=80, font=("Arial", 12), bg="#8E9EC6", fg="black")
    texto_datos_usuario.insert("1.0", datos_usuario)
    texto_datos_usuario.config(state="disabled")
    texto_datos_usuario.pack(pady=10)

    # Mostrar medicamentos
    medicamentos = ""
    ruta_medicamentos = "Credenciales/"
    try:
        archivos_medicamentos = [f for f in os.listdir(ruta_medicamentos) if f.startswith("Med_") and f.endswith(".txt")]
    except FileNotFoundError:
        archivos_medicamentos = []

    if archivos_medicamentos:
        for archivo in archivos_medicamentos:
            try:
                with open(os.path.join(ruta_medicamentos, archivo), "r") as archivo_medicamento:
                    medicamentos += archivo_medicamento.read() + "\n"
            except FileNotFoundError:
                medicamentos += f"No se pudo leer el archivo {archivo}.\n"
    else:
        medicamentos = "No se encontraron medicamentos guardados."

    # Etiqueta de "Medicamentos"
    label_medicamentos = tk.Label(ventana_ver_datos, text="Medicamentos", font=("Arial", 16, "bold"), bg="#8E9EC6", fg="black")
    label_medicamentos.pack(pady=20)

    # Cuadro de texto para los medicamentos
    texto_medicamentos = tk.Text(ventana_ver_datos, height=10, width=80, font=("Arial", 12), bg="#8E9EC6", fg="black")
    texto_medicamentos.insert("1.0", medicamentos)
    texto_medicamentos.config(state="disabled")
    texto_medicamentos.pack(pady=10)

def guardar_horario(desayuno, almuerzo, cena, refrigerio):
    # Mapeo de opciones a los números correspondientes
    desayuno_valores = {'06:00': 1, '07:00': 2, '08:00': 3}
    almuerzo_valores = {'14:00': 4, '13:00': 5, '12:00': 6}
    cena_valores = {'20:00': 7, '19:00': 8, '18:00': 9}
    refrigerio_valores = {'15:00': 10, '10:00': 11}
    
    desayuno_num = desayuno_valores[desayuno.get()]
    almuerzo_num = almuerzo_valores[almuerzo.get()]
    cena_num = cena_valores[cena.get()]
    refrigerio_num = refrigerio_valores[refrigerio.get()]
    
    # Guardar la información en un archivo de texto
    with open('Credenciales/Horario_Comidas.txt', 'w') as file:
        file.write(f'Desayuno: {desayuno_num}\n')
        file.write(f'Almuerzo: {almuerzo_num}\n')
        file.write(f'Cena: {cena_num}\n')
        file.write(f'Refrigerio: {refrigerio_num}\n')

    messagebox.showinfo("Guardado", "Horario guardado con éxito")

def abrir_formulario_horario():
    # Crear una nueva ventana
    root = tk.Toplevel()
    root.title("Formulario Horario de Comidas")
    root.geometry("1280x720")  # Tamaño ajustado a 1280x720
    root.configure(bg="#B5C2F4")
    
    # Variables para almacenar la selección de radio buttons
    desayuno = tk.StringVar(value='06:00')
    almuerzo = tk.StringVar(value='14:00')
    cena = tk.StringVar(value='20:00')
    refrigerio = tk.StringVar(value='15:00')

    # Estilo para las etiquetas
    label_style = {"font": ("Arial", 16, "bold"), "bg": "#8E9EC6", "fg": "black"}

    # Campo para desayuno (ubicado a la izquierda)
    tk.Label(root, text="Desayuno", **label_style).place(x=100, y=100)
    tk.Radiobutton(root, text="06:00", variable=desayuno, value='06:00', bg="#B5C2F4").place(x=120, y=150)
    tk.Radiobutton(root, text="07:00", variable=desayuno, value='07:00', bg="#B5C2F4").place(x=120, y=180)
    tk.Radiobutton(root, text="08:00", variable=desayuno, value='08:00', bg="#B5C2F4").place(x=120, y=210)

    # Campo para almuerzo (ubicado a la izquierda)
    tk.Label(root, text="Almuerzo", **label_style).place(x=100, y=300)
    tk.Radiobutton(root, text="12:00", variable=almuerzo, value='12:00', bg="#B5C2F4").place(x=120, y=350)
    tk.Radiobutton(root, text="13:00", variable=almuerzo, value='13:00', bg="#B5C2F4").place(x=120, y=380)
    tk.Radiobutton(root, text="14:00", variable=almuerzo, value='14:00', bg="#B5C2F4").place(x=120, y=410)

    # Campo para cena (ubicado a la derecha)
    tk.Label(root, text="Cena", **label_style).place(x=800, y=100)
    tk.Radiobutton(root, text="18:00", variable=cena, value='18:00', bg="#B5C2F4").place(x=820, y=150)
    tk.Radiobutton(root, text="19:00", variable=cena, value='19:00', bg="#B5C2F4").place(x=820, y=180)
    tk.Radiobutton(root, text="20:00", variable=cena, value='20:00', bg="#B5C2F4").place(x=820, y=210)

    # Campo para refrigerio (ubicado a la derecha)
    tk.Label(root, text="Refrigerio", **label_style).place(x=800, y=300)
    tk.Radiobutton(root, text="10:00", variable=refrigerio, value='10:00', bg="#B5C2F4").place(x=820, y=350)
    tk.Radiobutton(root, text="15:00", variable=refrigerio, value='15:00', bg="#B5C2F4").place(x=820, y=380)

    # Botón para guardar la selección (centrado)
    tk.Button(root, text="Guardar", font=("Arial", 14), bg="#8E9EC6", command=lambda: guardar_horario(desayuno, almuerzo, cena, refrigerio)).place(x=580, y=500)

    root.mainloop()

def obtener_horario_comidas():
    try:
        with open('Credenciales/Horario_Comidas.txt', 'r') as file:
            lineas = file.readlines()
            desayuno_num = int(lineas[0].split(': ')[1].strip())
            almuerzo_num = int(lineas[1].split(': ')[1].strip())
            cena_num = int(lineas[2].split(': ')[1].strip())
            refrigerio_num = int(lineas[3].split(': ')[1].strip())
        return desayuno_num, almuerzo_num, cena_num, refrigerio_num
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo Horario_Comidas.txt no fue encontrado.")
        return None

def mapear_hora_comida(numero, rango):
    if rango == 'desayuno':
        return {1: "06:00", 2: "07:00", 3: "08:00"}.get(numero, "Desconocido")
    elif rango == 'almuerzo':
        return {6: "12:00", 5: "13:00", 4: "14:00"}.get(numero, "Desconocido")
    elif rango == 'cena':
        return {9: "18:00", 8: "19:00", 7: "20:00"}.get(numero, "Desconocido")
    elif rango == 'refrigerio':
        return {11: "10:00", 10: "15:00"}.get(numero, "Desconocido")

def ver_horario_comidas():
    # Simulación de la obtención de horarios
    horarios = obtener_horario_comidas()
    if horarios is None:
        return  # Si no se encontró el archivo, detener la ejecución de la función

    desayuno_hora = mapear_hora_comida(horarios[0], 'desayuno')
    almuerzo_hora = mapear_hora_comida(horarios[1], 'almuerzo')
    cena_hora = mapear_hora_comida(horarios[2], 'cena')
    refrigerio_hora = mapear_hora_comida(horarios[3], 'refrigerio')
    
    # Crear una nueva ventana para mostrar el horario
    root = tk.Toplevel()
    root.title("Ver Horario de Comidas")
    root.geometry("600x400")  # Tamaño más pequeño (600x400)
    root.configure(bg="#B5C2F4")

    # Estilo para las etiquetas
    label_style = {"font": ("Arial", 14, "bold"), "bg": "#8E9EC6", "fg": "black"}

    # Mostrar los horarios con etiquetas posicionadas a los lados
    # Desayuno y almuerzo a la izquierda
    tk.Label(root, text=f"Desayuno: {desayuno_hora}", **label_style).place(x=50, y=100)
    tk.Label(root, text=f"Almuerzo: {almuerzo_hora}", **label_style).place(x=50, y=200)

    # Cena y refrigerio a la derecha
    tk.Label(root, text=f"Cena: {cena_hora}", **label_style).place(x=350, y=100)
    tk.Label(root, text=f"Refrigerio: {refrigerio_hora}", **label_style).place(x=350, y=200)

    root.mainloop()


# Función que abre el formulario para agregar datos
def abrir_formulario():
    ventana_formulario = tk.Toplevel()
    ventana_formulario.title("Formulario de datos")
    ventana_formulario.geometry("1280x720")
    ventana_formulario.configure(bg="#B5C2F4")

    color_campos = "#8E9EC6"  # Color de fondo más oscuro para los campos de texto
    color_etiquetas = "#B5C2F4"  # Color para las etiquetas

    # Etiquetas y campos de entrada
    tk.Label(ventana_formulario, text="Nombre:", bg=color_etiquetas).place(x=500, y=100, width=120, height=30)
    entry_nombre = tk.Entry(ventana_formulario, bg=color_campos)
    entry_nombre.place(x=650, y=100, width=150, height=30)

    tk.Label(ventana_formulario, text="Edad:", bg=color_etiquetas).place(x=500, y=150, width=120, height=30)
    entry_edad = tk.Entry(ventana_formulario, bg=color_campos)
    entry_edad.place(x=650, y=150, width=150, height=30)

    tk.Label(ventana_formulario, text="Peso:", bg=color_etiquetas).place(x=500, y=200, width=120, height=30)
    entry_peso = tk.Entry(ventana_formulario, bg=color_campos)
    entry_peso.place(x=650, y=200, width=150, height=30)

    tk.Label(ventana_formulario, text="Estatura:", bg=color_etiquetas).place(x=500, y=250, width=120, height=30)
    entry_estatura = tk.Entry(ventana_formulario, bg=color_campos)
    entry_estatura.place(x=650, y=250, width=150, height=30)

    # Radio buttons para "¿Fuma?"
    tk.Label(ventana_formulario, text="¿Fuma?", bg=color_etiquetas).place(x=500, y=300, width=120, height=30)
    fuma_var = tk.StringVar(value="No")
    tk.Radiobutton(ventana_formulario, text="Sí", variable=fuma_var, value="Sí", bg="#B5C2F4").place(x=650, y=300)
    tk.Radiobutton(ventana_formulario, text="No", variable=fuma_var, value="No", bg="#B5C2F4").place(x=700, y=300)

    # Radio buttons para "¿Toma Alcohol?"
    tk.Label(ventana_formulario, text="¿Toma Alcohol?", bg=color_etiquetas).place(x=500, y=350, width=120, height=30)
    alcohol_var = tk.StringVar(value="No")
    tk.Radiobutton(ventana_formulario, text="Sí", variable=alcohol_var, value="Sí", bg="#B5C2F4").place(x=650, y=350)
    tk.Radiobutton(ventana_formulario, text="No", variable=alcohol_var, value="No", bg="#B5C2F4").place(x=700, y=350)
    

    # Función para guardar los datos
    def guardar_datos():
        if (not entry_nombre.get() or not entry_edad.get() or not entry_peso.get() or
                not entry_estatura.get()):
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
        else:
            nombre = entry_nombre.get()
            edad = entry_edad.get()
            peso = entry_peso.get()
            estatura = entry_estatura.get()
            alcohol = alcohol_var.get()
            fuma = fuma_var.get()

            datos = f"Nombre: {nombre}\nEdad: {edad}\nPeso: {peso}\nEstatura: {estatura}\nToma Alcohol: {alcohol}\nFuma: {fuma}\n"
            with open("Credenciales/datos_usuario.txt", "w") as archivo:
                archivo.write(datos)

            messagebox.showinfo("Datos guardados", "Los datos han sido guardados correctamente.")
            ventana_formulario.destroy()
    # Colocar el botón "Guardar" para que sea visible
    tk.Button(ventana_formulario, text="Guardar", command=guardar_datos, bg="#8E9EC6").place(x=600, y=400, width=100, height=30)

# Función que abre el formulario para configurar los datos existentes
def abrir_formulario_configurar():
    ventana_configurar = tk.Toplevel()
    ventana_configurar.title("Configurar datos")
    ventana_configurar.geometry("1280x720")
    ventana_configurar.configure(bg="#B5C2F4")

    try:
        with open("Credenciales/datos_usuario.txt", "r") as archivo:
            datos = archivo.readlines()
            nombre = datos[0].split(":")[1].strip()
            edad = datos[1].split(":")[1].strip()
            peso = datos[2].split(":")[1].strip()
            estatura = datos[3].split(":")[1].strip()
            alcohol = datos[4].split(":")[1].strip()
            fuma = datos[5].split(":")[1].strip()
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de datos.")
        ventana_configurar.destroy()
        return

    color_campos = "#8E9EC6"  # Color de fondo más oscuro para los campos de texto
    color_etiquetas = "#B5C2F4"  # Color para las etiquetas

    # Etiquetas y campos de entrada
    tk.Label(ventana_configurar, text="Nombre:", bg=color_etiquetas).place(x=500, y=100, width=120, height=30)
    entry_nombre = tk.Entry(ventana_configurar, bg=color_campos)
    entry_nombre.insert(0, nombre)
    entry_nombre.place(x=650, y=100, width=150, height=30)

    tk.Label(ventana_configurar, text="Edad:", bg=color_etiquetas).place(x=500, y=150, width=120, height=30)
    entry_edad = tk.Entry(ventana_configurar, bg=color_campos)
    entry_edad.insert(0, edad)
    entry_edad.place(x=650, y=150, width=150, height=30)

    tk.Label(ventana_configurar, text="Peso:", bg=color_etiquetas).place(x=500, y=200, width=120, height=30)
    entry_peso = tk.Entry(ventana_configurar, bg=color_campos)
    entry_peso.insert(0, peso)
    entry_peso.place(x=650, y=200, width=150, height=30)

    tk.Label(ventana_configurar, text="Estatura:", bg=color_etiquetas).place(x=500, y=250, width=120, height=30)
    entry_estatura = tk.Entry(ventana_configurar, bg=color_campos)
    entry_estatura.insert(0, estatura)
    entry_estatura.place(x=650, y=250, width=150, height=30)

    # Radio buttons para "¿Toma alcohol?"
    tk.Label(ventana_configurar, text="¿Toma Alcohol?", bg=color_etiquetas).place(x=500, y=300, width=120, height=30)
    alcohol_var = tk.StringVar(value=alcohol)
    tk.Radiobutton(ventana_configurar, text="Sí", variable=alcohol_var, value="Sí", bg="#B5C2F4").place(x=650, y=300)
    tk.Radiobutton(ventana_configurar, text="No", variable=alcohol_var, value="No", bg="#B5C2F4").place(x=700, y=300)

    # Radio buttons para "¿Fuma?"
    tk.Label(ventana_configurar, text="¿Fuma?", bg=color_etiquetas).place(x=500, y=350, width=120, height=30)
    fuma_var = tk.StringVar(value=fuma)
    tk.Radiobutton(ventana_configurar, text="Sí", variable=fuma_var, value="Sí", bg="#B5C2F4").place(x=650, y=350)
    tk.Radiobutton(ventana_configurar, text="No", variable=fuma_var, value="No", bg="#B5C2F4").place(x=700, y=350)

    # Función para guardar cambios
    def guardar_cambios():
        if (not entry_nombre.get() or not entry_edad.get() or not entry_peso.get() or
                not entry_estatura.get()):
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
        else:
            nombre_modificado = entry_nombre.get()
            edad_modificada = entry_edad.get()
            peso_modificado = entry_peso.get()
            estatura_modificada = entry_estatura.get()
            alcohol_modificado = alcohol_var.get()
            fuma_modificado = fuma_var.get()

            datos_modificados = (f"Nombre: {nombre_modificado}\nEdad: {edad_modificada}\n"
                                 f"Peso: {peso_modificado}\nEstatura: {estatura_modificada}\n"
                                 f"Toma Alcohol: {alcohol_modificado}\nFuma: {fuma_modificado}\n")
            with open("Credenciales/datos_usuario.txt", "w") as archivo:
                archivo.write(datos_modificados)

            messagebox.showinfo("Datos actualizados", "Los datos han sido guardados correctamente.")
            ventana_configurar.destroy()

    # Botón de guardar cambios
    tk.Button(ventana_configurar, text="Guardar cambios", command=guardar_cambios, bg="#8E9EC6").place(x=600, y=400, width=100, height=30)

# Función que maneja la pregunta de si toma medicamentos
def abrir_datos_especificos():
    ventana_datos = tk.Toplevel()
    ventana_datos.title("Datos Específicos")
    ventana_datos.geometry("400x400")  # Cambiamos el tamaño para que coincida más con la imagen
    ventana_datos.configure(bg="#B5C2F4")

    # Etiqueta con la pregunta, cambiando la fuente y el tamaño
    tk.Label(ventana_datos, text="¿Toma medicamentos?", font=("Arial", 16, "bold"), bg="#B5C2F4").pack(pady=40)

    respuesta_var = tk.StringVar()

    # Radio buttons para seleccionar sí o no, con colores personalizados
    tk.Radiobutton(ventana_datos, text="Sí", variable=respuesta_var, value="Sí", font=("Arial", 12), bg="#B5C2F4", activebackground="#8E9EC6", selectcolor="#8E9EC6").pack(pady=5)
    tk.Radiobutton(ventana_datos, text="No", variable=respuesta_var, value="No", font=("Arial", 12), bg="#B5C2F4", activebackground="#8E9EC6", selectcolor="#8E9EC6").pack(pady=5)

    # Función que valida la respuesta
    def validar_respuesta():
        if respuesta_var.get() == "Sí":
            ventana_datos.destroy()
            abrir_formulario_medicamentos()
        elif respuesta_var.get() == "No":
            ventana_datos.destroy()
        else:
            messagebox.showwarning("Advertencia", "Seleccione una opción")

    # Botón para confirmar la respuesta
    tk.Button(ventana_datos, text="Aceptar", command=validar_respuesta, font=("Arial", 12), bg="#8E9EC6", activebackground="#B5C2F4").pack(pady=30)

# Función para abrir el formulario de medicamentos
def abrir_formulario_medicamentos():
    ventana_medicamentos = tk.Toplevel()
    ventana_medicamentos.title("Formulario Medicamentos")
    ventana_medicamentos.geometry("400x400")  # Cambié el tamaño de la ventana para que coincida con la imagen
    ventana_medicamentos.configure(bg="#B5C2F4")

    # Etiqueta para el nombre del medicamento
    tk.Label(ventana_medicamentos, text="Nombre del medicamento", font=("Arial", 16, "bold"), bg="#8E9EC6", fg="black").pack(pady=20)

    # Entrada para el nombre del medicamento
    entry_nombre_medicamento = tk.Entry(ventana_medicamentos, font=("Arial", 12), bg="#8E9EC6", fg="black", width=30)
    entry_nombre_medicamento.pack(pady=5)

    # Etiqueta para el horario de toma
    tk.Label(ventana_medicamentos, text="Hora de la toma", font=("Arial", 16, "bold"), bg="#8E9EC6", fg="black").pack(pady=20)

    # Entrada para el horario
    entry_horario = tk.Entry(ventana_medicamentos, font=("Arial", 12), bg="#8E9EC6", fg="black", width=30)
    entry_horario.pack(pady=5)

    # Función para guardar los datos del medicamento en un archivo .txt
    def guardar_medicamento():
        nombre_medicamento = entry_nombre_medicamento.get()
        horario = entry_horario.get()

        if nombre_medicamento and horario:
            # Crear archivo .txt con el nombre del medicamento
            with open(f"Credenciales/Med_{nombre_medicamento}.txt", "w") as archivo:
                archivo.write(f"Medicamento: {nombre_medicamento}\nHorario: {horario}")

            messagebox.showinfo("Éxito", "Medicamento guardado correctamente")
            entry_nombre_medicamento.delete(0, tk.END)
            entry_horario.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Complete todos los campos")

    # Botón para guardar los datos
    tk.Button(ventana_medicamentos, text="Guardar", command=guardar_medicamento, font=("Arial", 12), bg="#8E9EC6", activebackground="#B5C2F4").pack(pady=30)

def abrir_pagina():
    # Abre la página en el navegador predeterminado
    webbrowser.open("https://instafit.com")

def mostrar_redes_wifi(texto_redes):
    # Comando para listar redes wifi en Windows
    comando = "netsh wlan show networks"
    
    # Ejecutar el comando en el sistema
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    
    # Mostrar el resultado en el campo de texto
    texto_redes.config(state="normal")  # Habilitar edición
    texto_redes.delete(1.0, tk.END)  # Limpiar el texto anterior
    texto_redes.insert(tk.END, resultado.stdout)  # Insertar el resultado del comando
    texto_redes.config(state="disabled")  # Deshabilitar edición para solo mostrar texto
    

def Mostrar_wifi():
    ventana = tk.Tk()
    ventana.title("Detector de Redes Wi-Fi")
    ventana.geometry("600x400")
    ventana.configure(bg="#c0c8e0")  # Color de fondo similar al mostrado en las imágenes
    
    # Fuentes
    fuente_titulo = font.Font(family="Helvetica", size=16, weight="bold")
    fuente_botones = font.Font(family="Helvetica", size=12)

    # Título
    label_titulo = tk.Label(ventana, text="Detector de Redes Wi-Fi", font=fuente_titulo, bg="#c0c8e0")
    label_titulo.pack(pady=10)
    
    # Campo de texto para mostrar las redes Wi-Fi
    texto_redes = tk.Text(ventana, wrap=tk.WORD, height=10, width=50, font="Helvetica 10")
    texto_redes.pack(pady=10)
    texto_redes.config(state="disabled", bg="#eef1f8", fg="#000")  # Fondo suave y texto oscuro

    # Botón para escanear redes Wi-Fi
    boton_escaneo = tk.Button(
        ventana, 
        text="Escanear Redes Wi-Fi", 
        command=lambda: mostrar_redes_wifi(texto_redes),
        bg="#6f86d6",  # Color de fondo del botón
        fg="white",  # Color del texto del botón
        font=fuente_botones,
        relief="flat",
        padx=10,
        pady=5
    )
    boton_escaneo.pack(pady=20)

    ventana.mainloop()

# Función para obtener el controlador de volumen del sistema
def get_volumen_control():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume

def set_volumen(val):
    volume = get_volumen_control()
    volume_level = float(val) / 100 * (volume.GetVolumeRange()[1] - volume.GetVolumeRange()[0]) + volume.GetVolumeRange()[0]
    volume.SetMasterVolumeLevel(volume_level, None)

# Función principal para la interfaz de control de volumen
def volumen():
    # Crear ventana de la interfaz
    root = tk.Tk()
    root.title("Control de Volumen")
    root.geometry("400x200")
    root.configure(bg="#c0c8e0")  # Fondo similar al mostrado en tus ejemplos

    # Estilo y fuentes
    style = ttk.Style()
    style.configure("TLabel", background="#c0c8e0", foreground="#3b4d8b", font=("Helvetica", 12))  # Etiqueta con azul oscuro
    style.configure("TScale", background="#3b4d8b", troughcolor="#3b4d8b", sliderthickness=15)  # Barra deslizante con azul más oscuro

    # Etiqueta para la barra deslizante
    label = ttk.Label(root, text="Control de volumen:")
    label.pack(pady=20)
    label.configure(background="#6f86d6")

    # Crear barra deslizante para el volumen
    slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', command=set_volumen)
    slider.set(50)  # Valor inicial
    slider.pack(pady=20, padx=40)
    

    # Ejecutar la aplicación
    root.mainloop()

def seleccionar_carpeta(lista_archivos):
    carpeta = filedialog.askdirectory()  # Abre el explorador para seleccionar una carpeta
    if carpeta:
        mostrar_contenido_carpeta(carpeta, lista_archivos)

# Función para mostrar el contenido de la carpeta seleccionada
def mostrar_contenido_carpeta(carpeta, lista_archivos):
    lista_archivos.delete(0, tk.END)  # Limpia la lista de archivos actual
    archivos = os.listdir(carpeta)  # Lista el contenido de la carpeta
    for archivo in archivos:
        lista_archivos.insert(tk.END, archivo)  # Agrega cada archivo/carpeta a la lista
    lista_archivos.carpeta_actual = carpeta  # Almacena la carpeta actual

# Función para abrir el archivo seleccionado
def abrir_archivo(event, lista_archivos):
    seleccionado = lista_archivos.get(lista_archivos.curselection())
    carpeta_actual = lista_archivos.carpeta_actual
    ruta_archivo = os.path.join(carpeta_actual, seleccionado)

    if platform.system() == "Windows":
        os.startfile(ruta_archivo)  # Windows
    elif platform.system() == "Darwin":
        subprocess.call(["open", ruta_archivo])  # macOS
    else:
        subprocess.call(["xdg-open", ruta_archivo])  # Linux

def administrador_archivos():
    # Crear ventana de la interfaz
    root = tk.Tk()
    root.title("Explorador de Archivos")
    root.geometry("500x400")
    root.configure(bg="#c0c8e0")  # Fondo con tono suave

    # Estilo y fuentes
    style = ttk.Style()
    style.configure("TButton", background="#6f86d6", foreground="white", font=("Helvetica", 12))  # Botón estilizado
    style.configure("TLabel", background="#c0c8e0", foreground="#3b4d8b", font=("Helvetica", 12))  # Etiqueta en azul más oscuro

    # Crear lista para mostrar archivos y carpetas
    lista_archivos = tk.Listbox(root, height=15, width=50, bg="#eef1f8", fg="#000", font=("Helvetica", 10))
    lista_archivos.pack(pady=10)

    # Crear botón para seleccionar carpeta
    btn_seleccionar = ttk.Button(root, text="Seleccionar carpeta", command=lambda: seleccionar_carpeta(lista_archivos))
    btn_seleccionar.pack(pady=10)

    # Vincular evento de doble clic para abrir el archivo
    lista_archivos.bind('<Double-1>', lambda event: abrir_archivo(event, lista_archivos))

    # Ejecutar la aplicación
    root.mainloop()

def abrir_navegador():
    
    # Abre el navegador predeterminado
    webbrowser.open("http://www.google.com")
    

def abrir_configuracion():
    ventana_config = tk.Toplevel()
    ventana_config.title("Configuración")
    ventana_config.geometry("1280x720")
    
    def cambiar_fondo():
        global imagen_fondo_principal_tk
        archivo_imagen = filedialog.askopenfilename(title="Selecciona un fondo de pantalla", filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg")])
        if archivo_imagen:
            guardar_fondo(archivo_imagen)  # Guardar la ruta seleccionada en el archivo
            
            # Cargar la nueva imagen de fondo y actualizarla en la interfaz
            nueva_imagen_fondo = Image.open(archivo_imagen)
            nueva_imagen_fondo = nueva_imagen_fondo.resize((1280, 720), Image.LANCZOS)
            imagen_fondo_principal_tk = ImageTk.PhotoImage(nueva_imagen_fondo)
            label_fondo_principal.config(image=imagen_fondo_principal_tk)  # Actualizar el Label con la nueva imagen
            messagebox.showinfo("Éxito", "Fondo de pantalla cambiado y actualizado.")

    # Cambiar nombre de usuario y contraseña
    def cambiar_credenciales():
        global usuario_actual, contrasena_actual
        nuevo_usuario = entry_nuevo_usuario.get()
        nueva_contrasena = entry_nueva_contrasena.get()

        if nuevo_usuario and nueva_contrasena:
            usuario_actual = nuevo_usuario
            contrasena_actual = nueva_contrasena
            guardar_credenciales(usuario_actual, contrasena_actual)  # Guardar en el archivo
            messagebox.showinfo("Éxito", "Usuario y contraseña actualizados.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")

    # Modificar el brillo
    def cambiar_brillo(valor):
        # Cambia el brillo del computador
        try:
            sbc.set_brightness(int(valor))
        except Exception as e:
            print(f"Error al ajustar el brillo: {e}")

    def get_volumen_control():
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return volume

    # Función para ajustar el volumen según el valor de la barra deslizante
    def set_volumen(val):
        volume = get_volumen_control()
        # El rango de la API es entre -65.25 (silencio) y 0 (volumen máximo)
        volume_level = float(val) / 100 * (volume.GetVolumeRange()[1] - volume.GetVolumeRange()[0]) + volume.GetVolumeRange()[0]
        volume.SetMasterVolumeLevel(volume_level, None)

    def abrir_seguridad_sistema():
        ventana_seguridad = tk.Toplevel()
        ventana_seguridad.title("Seguridad del Sistema")
        ventana_seguridad.geometry("600x400")

        # Añadir las opciones como en la imagen
        opciones = [
            ("Protección contra virus y amenazas", "No se requieren acciones."),
            ("Protección de cuentas", "No se requieren acciones."),
            ("Firewall y protección de red", "No se requieren acciones."),
            ("Control de aplicaciones y exploradores", "Acciones recomendadas."),
            ("Seguridad del dispositivo", "Acciones recomendadas."),
            ("Rendimiento y estado del dispositivo", "Informes sobre el estado del dispositivo."),
            ("Opciones de familia", "Administra la forma en que tu familia usa los dispositivos.")
        ]

        for opcion, estado in opciones:
            frame = tk.Frame(ventana_seguridad)
            frame.pack(fill="x", pady=5)
            
            label_opcion = tk.Label(frame, text=opcion, anchor="w")
            label_opcion.pack(side="left", padx=10)

            label_estado = tk.Label(frame, text=estado, anchor="e")
            label_estado.pack(side="right", padx=10)

        messagebox.showinfo("Seguridad del Sistema", "Interfaz de seguridad del sistema abierta.")

    # Botón para abrir Seguridad del Sistema
    boton_seguridad_sistema = tk.Button(ventana_config, text="Seguridad del Sistema", command=abrir_seguridad_sistema)
    boton_seguridad_sistema.pack(pady=10)

    # Añadir un control deslizante (slider) para el volumen en la ventana de configuración
    tk.Label(ventana_config, text="Control de Volumen:").pack(pady=5)
    slider_volumen = tk.Scale(ventana_config, from_=0, to=100, orient='horizontal', command=set_volumen)
    slider_volumen.set(50)  # Valor inicial
    slider_volumen.pack(pady=10)

    # Botón para cambiar el fondo de pantalla
    boton_fondo = tk.Button(ventana_config, text="Cambiar Fondo de Pantalla", command=cambiar_fondo)
    boton_fondo.pack(pady=10)
    
    # Campos para cambiar el nombre de usuario y contraseña
    tk.Label(ventana_config, text="Nuevo Usuario:").pack(pady=5)
    entry_nuevo_usuario = tk.Entry(ventana_config)
    entry_nuevo_usuario.pack(pady=5)

    tk.Label(ventana_config, text="Nueva Contraseña:").pack(pady=5)
    entry_nueva_contrasena = tk.Entry(ventana_config, show="*")
    entry_nueva_contrasena.pack(pady=5)

    boton_guardar = tk.Button(ventana_config, text="Guardar Credenciales", command=cambiar_credenciales)
    boton_guardar.pack(pady=10)
    
    # Control de brillo
    tk.Label(ventana_config, text="Ajustar Brillo:").pack(pady=5)
    slider_brillo = tk.Scale(ventana_config, from_=0, to=100, orient="horizontal", command=cambiar_brillo)
    slider_brillo.pack(pady=10)

def ejecutar_steam():
    # Cambiar la ruta según tu proyecto
    ruta_steam = os.path.join(os.getcwd(), "Aplicaciones", "steam.exe")
    os.startfile(ruta_steam)


def actualizar_recordatorio_medicamento():
    global RecMedicamento  # Declarar la variable global para que se pueda usar en esta función
    ruta_carpeta = os.path.join(os.getcwd(), "Credenciales")  # Ruta de la carpeta Credenciales
    prefijo = "Med_"
    
    medicamentos = []
    
    # Leer archivos en la carpeta con el prefijo "Med_"
    for archivo in os.listdir(ruta_carpeta):
        if archivo.startswith(prefijo) and archivo.endswith('.txt'):
            ruta_archivo = os.path.join(ruta_carpeta, archivo)
            
            # Leer el archivo (suponiendo que los medicamentos están en la primera línea, horario en la segunda)
            with open(ruta_archivo, 'r') as f:
                nombre_medicamento = f.readline().strip()  # Nombre del medicamento
                horario = f.readline().strip()  # Horario de toma
                
                # Agregar a la lista de medicamentos y horarios
                medicamentos.append(f"{nombre_medicamento} en el {horario}")
    
    # Formatear el mensaje de recordatorio
    if medicamentos:
        mensaje = "No olvides tomarte tu medicamento(s):\n" + "\n".join(medicamentos)
    else:
        mensaje = "No hay medicamentos para recordar."
    
    # Actualizar la etiqueta en la ventana principal
    RecMedicamento.config(text=mensaje)
    
    ventana_principal.after(60000, actualizar_recordatorio_medicamento)

def actualizar_horario_comida():
    try:
        # Ruta al archivo Horario_Comidas.txt
        ruta_archivo = os.path.join("Credenciales", "Horario_Comidas.txt")
        with open(ruta_archivo, "r") as archivo:
            contenido = archivo.readlines()  # Leer el archivo línea por línea
        
        # Diccionario para almacenar los horarios
        horarios_interpretados = {
            'Desayuno': '',
            'Almuerzo': '',
            'Cena': '',
            'Refrigerio': ''
        }

        # Procesar cada línea del archivo
        for linea in contenido:
            partes = linea.strip().split(":")
            if len(partes) == 2:
                tipo_comida = partes[0].strip()  # Desayuno, Almuerzo, Cena, Refrigerio
                try:
                    numero_hora = int(partes[1].strip())  # Obtener el número de la hora
                except ValueError:
                    continue  # Saltar si no es un número válido

                # Mapear la hora según el tipo de comida
                if tipo_comida in horarios_interpretados:
                    horarios_interpretados[tipo_comida] = mapear_hora_comida(numero_hora, tipo_comida.lower())

        # Crear el texto final para la etiqueta
        texto_final = f"Desayuno: {horarios_interpretados['Desayuno']} \n "
        texto_final += f"Almuerzo: {horarios_interpretados['Almuerzo']} \n "
        texto_final += f"Cena: {horarios_interpretados['Cena']} \n "
        texto_final += f"Refrigerio: {horarios_interpretados['Refrigerio']}"

        # Actualizar el texto de la etiqueta RecComida
        RecComida.config(text=texto_final)

    except FileNotFoundError:
        RecComida.config(text="Horario de comidas no disponible")

    # Volver a llamar a esta función después de 60 segundos
    ventana_principal.after(60000, actualizar_horario_comida)

# Función para abrir una aplicación al hacer doble clic
def ejecutar_aplicacion(event):
    seleccion = lista_aplicaciones.get(lista_aplicaciones.curselection())
    
    # Diccionario con las rutas de las aplicaciones (cambia las rutas según tu sistema)
    rutas = {
        'Word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
        'Excel': r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
        'PowerPoint': r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE',
        'Calculadora': r'C:\Windows\System32\calc.exe',
        'Navegador': None  # Usaremos webbrowser para abrir la página de Google
    }

    # Si selecciona "Navegador", abre Google automáticamente
    if seleccion == 'Navegador':
        webbrowser.open("https://www.google.com")
    else:
        # Verificar si la aplicación está en el diccionario
        if seleccion in rutas:
            ruta_app = rutas[seleccion]
            if ruta_app and os.path.exists(ruta_app):
                subprocess.Popen(ruta_app)
            else:
                messagebox.showerror("Error", f"No se encontró {seleccion} en el sistema.")
        else:
            messagebox.showerror("Error", "Aplicación no encontrada.")

# Función para abrir una nueva ventana con la lista de aplicaciones
def abrir_ventana_aplicaciones():
    ventana_aplicaciones = tk.Toplevel(ventana_principal)
    ventana_aplicaciones.title("Aplicaciones")
    ventana_aplicaciones.geometry("400x300")
    
    # Fuente personalizada
    fuente = font.Font(family="Helvetica", size=14)
    
    # Crear la lista con las aplicaciones
    global lista_aplicaciones
    lista_aplicaciones = Listbox(ventana_aplicaciones, height=10, font=fuente)
    for app in aplicaciones:
        lista_aplicaciones.insert(tk.END, app)

    # Asignar la función de doble clic a la lista
    lista_aplicaciones.bind('<Double-Button-1>', ejecutar_aplicacion)
    
    # Posicionar la lista con place
    lista_aplicaciones.place(x=50, y=50, width=300, height=200)

def abrir_word():
    # Ruta de instalación de Microsoft Word
    ruta_word = r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE'  # Cambia esta ruta si es necesario
    os.startfile(ruta_word)

def abrir_excel():
    # Ruta de instalación de Microsoft Excel
    ruta_excel = r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'  # Cambia esta ruta si es necesario
    os.startfile(ruta_excel)

def abrir_calculadora():
    os.system('calc')

def abrir_powerpoint():
    # Ruta de instalación de Microsoft PowerPoint
    ruta_powerpoint = r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE'  # Cambia esta ruta si es necesario
    os.startfile(ruta_powerpoint)

# Crear la ventana de login
ventana_login = tk.Tk()
ventana_login.title("Login")
ventana_login.geometry("1280x720")

# Cargar la imagen de fondo para la pantalla de login
imagen_fondo_login = Image.open("Imagenes/Fondo_1.PNG")  # Asegúrate de ajustar la ruta
imagen_fondo_login = imagen_fondo_login.resize((1280, 720), Image.LANCZOS)
imagen_fondo_login_tk = ImageTk.PhotoImage(imagen_fondo_login)

# Crear un Label para la imagen de fondo
label_fondo_login = tk.Label(ventana_login, image=imagen_fondo_login_tk)
label_fondo_login.place(x=0, y=0, relwidth=1, relheight=1)

# Cargar la imagen encima del campo de usuario
imagen_usuario = Image.open("Imagenes/Logo Angora os.PNG")  # Ajusta la ruta de la imagen
imagen_usuario = imagen_usuario.resize((184, 144), Image.LANCZOS)
imagen_usuario_tk = ImageTk.PhotoImage(imagen_usuario)

# Etiqueta con la imagen del usuario
label_imagen_usuario = tk.Label(ventana_login, image=imagen_usuario_tk, bg="#e6c4ee", bd=0)
label_imagen_usuario.place(x=530, y=150)

label_usuario = tk.Label(ventana_login, text="Usuario:", font=("Arial", 14), bg="#6f84c7", fg="white")
label_usuario.place(x=400, y=350)
entry_usuario = tk.Entry(ventana_login, font=("Arial", 14),bg="#dfd6fb")
entry_usuario.place(x=510, y=350)

label_contrasena = tk.Label(ventana_login, text="Contraseña:", font=("Arial", 14), bg="#7985cb", fg="white")
label_contrasena.place(x=400, y=400)
entry_contrasena = tk.Entry(ventana_login, show="*", font=("Arial", 14),bg="#e8d3f8")
entry_contrasena.place(x=510, y=400)

# Botón de login sobre la imagen de fondo
boton_login = tk.Button(ventana_login, text="Iniciar sesión", command=iniciar_sesion, font=("Arial", 14), bg="#7985cb")
boton_login.place(x=552, y=450)



ventana_login.mainloop()
