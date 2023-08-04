import serial
import tkinter as tk
from tkinter import messagebox,simpledialog
from tkinter import PhotoImage
from PIL import Image, ImageTk

import os

from datetime import datetime

#DEFINICIONES DE VARIABLES GLOBALES
# Nombre del archivo de registro-------------------------------------------------------------------------------------------------------------------------------------------------------------
archivo_registro = "registro.txt"

# Variable global para rastrear si el usuario es administrador
es_admin = False

# Variables para rastrear si el usuario ha ingresado correctamente y si ya ha enviado un comando
usuario_ingresado = False
contrasena_ingresada = False
comando_enviado = False

# Variables para los botones adicionales del menú del usuario "admin"
boton_ver_usuarios = None
boton_modificar_usuarios = None
boton_finalizar_operaciones = None
boton_ver_movimientos = None 

# Configurar el tamaño de la fuente para las etiquetas y cuadros de entrada
font_size = 12  # Tamaño de la fuente deseado
font_size_boton = 9  #Tamaño de fuente deseado para los botones

# Configura el puerto serie para comunicarse con el Arduino
ser = serial.Serial('COM3', 9600)  # Reemplaza 'COM3' con el puerto serie correcto
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Función para habilitar los botones de comandos para usuarios no administradores===============================================================================================================
def habilitar_botones_comandos():
    # Iterar a través de cada botón en la colección 'botones_comandos'
    for boton in botones_comandos:
        # Verificar si el usuario tiene privilegios de administrador y el texto del botón comienza con 'A'
        if es_admin and boton['text'].startswith('A'):
            # Si es un administrador y el botón comienza con 'A', deshabilitar el botón
            boton.config(state=tk.DISABLED)
        else:
            # Si no es un administrador o el botón no comienza con 'A', habilitar el botón permitiendo hacer clic en él
            boton.config(state=tk.NORMAL)
#================================================================================================================================================================================================            

# Función para finalizar las operaciones del usuario "admin" y volver al menú principal
def finalizar_operaciones_admin():
    # Establecer las siguientes variables globales como falsas, indicando el final de las operaciones administrativas
    global es_admin, usuario_ingresado, contrasena_ingresada, comando_enviado
    es_admin = False
    usuario_ingresado = False
    contrasena_ingresada = False
    comando_enviado = False
    
    # Llamar a la función habilitar_botones_comandos() para habilitar ciertos botones de comandos
    habilitar_botones_comandos()

    # Ocultar los botones específicos si existen
    if boton_ver_usuarios is not None:
        boton_ver_usuarios.pack_forget()
    if boton_modificar_usuarios is not None:
        boton_modificar_usuarios.pack_forget()
    if boton_finalizar_operaciones is not None:
        boton_finalizar_operaciones.pack_forget()
    if boton_ver_movimientos is not None:
        boton_ver_movimientos.pack_forget()

    # Habilitar las entradas de usuario y contraseña, y el botón de verificación
    entrada_usuario.config(state=tk.NORMAL)  # Habilita la entrada de usuario
    entrada_contrasena.config(state=tk.NORMAL)  # Habilita la entrada de contraseña
    boton_verificar.config(state=tk.NORMAL)  # Habilita el botón de verificación
    
    # Mostrar y habilitar todos los botones de comandos
    for boton in botones_comandos:
        boton.pack()
    
    # Borrar el contenido de las entradas de usuario y contraseña
    entrada_usuario.delete(0, tk.END)
    entrada_contrasena.delete(0, tk.END)
        
    # Llamar a la función deshabilitar_botones_comandos() para deshabilitar botones de comandos específicos
    deshabilitar_botones_comandos()
#================================================================================================================================================================================================

# Función para mostrar el menú especial para el usuario "admin"
def mostrar_menu_admin():
    global es_admin, boton_ver_usuarios, boton_modificar_usuarios, boton_finalizar_operaciones, boton_ver_movimientos
    es_admin = True
    
    # Ocultar los botones de comandos anteriores
    for boton in botones_comandos:
        boton.pack_forget()  

    #-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
    # Crear botones adicionales para el menú especial del usuario "admin"
    # ventana: Este es el widget en el que se creará el botón. En el contexto de Tkinter, "ventana" se refiere a la ventana principal o al marco en el que se desea colocar el botón.
    # text: Este parámetro define el texto que se mostrará en el botón. En este caso, el texto es "a) Ver usuarios existentes".
    # command: Este parámetro especifica la función que se ejecutará cuando se haga clic en el botón. En este ejemplo, se asocia el botón con la función ver_usuarios_existentes, lo que significa que cuando se hace clic en el botón, se llamará a la función ver_usuarios_existentes.
    # bg: Este parámetro establece el color de fondo del botón. En este caso, se establece en "teal", que es un color verde azulado.
    # state: Este parámetro define el estado inicial del botón. tk.NORMAL indica que el botón estará en estado normal y se podrá hacer clic en él. Otro posible valor sería tk.DISABLED, que deshabilitaría el botón.
    #-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
    boton_ver_usuarios = tk.Button(ventana, text="a) Ver usuarios existentes", command=ver_usuarios_existentes, bg="teal", state=tk.NORMAL, width=50, font=("Helvetica", font_size_boton))
    boton_modificar_usuarios = tk.Button(ventana, text="b) Modificar usuarios existentes", command=mostrar_menu_modificar_usuarios, bg="lightblue", state=tk.NORMAL, width=50, font=("Helvetica", font_size_boton))
    boton_ver_movimientos = tk.Button(ventana, text="c) Ver movimientos registrados", command=ver_movimientos, bg="purple", state=tk.NORMAL, width=50, font=("Helvetica", font_size_boton))
    boton_finalizar_operaciones = tk.Button(ventana, text="d) Finalizar operaciones admin", command=finalizar_operaciones_admin, bg="red", state=tk.NORMAL, width=50, font=("Helvetica", font_size_boton))

    # Mostrar y habilitar los botones del menú administrativo en el orden especificado
    boton_ver_usuarios.pack()
    boton_modificar_usuarios.pack()
    boton_ver_movimientos.pack()
    boton_finalizar_operaciones.pack()
#================================================================================================================================================================================================
   
#muestra el registro de movimientos en pantalla al administrador (separado, visualmente)    
def ver_movimientos():
    try:
        #Intenta abrir el archivo "registro.txt" en modo lectura
        with open("registro.txt", "r") as file:
            movimientos = file.readlines()

        if movimientos:
            #Si hay movimientos registrados en el archivo --> Crea una ventana emergente para mostrar los movimientos
            ventana_movimientos = tk.Toplevel()
            ventana_movimientos.title("Movimientos Registrados")

            # Cuadro de texto para mostrar los movimientos
            cuadro_texto = tk.Text(ventana_movimientos, wrap=tk.WORD, width=80, height=20)
            
            # Formato de las líneas verticales divisorias
            divisorias = "-" * 20 + " | " + "-" * 20 + " | " + "-" * 20 + "\n"

            # Insertar los títulos en el cuadro de texto
            cuadro_texto.insert(tk.END, "Usuario".ljust(20) + " | " + "Movimiento".ljust(20) + " | " + "Fecha y Hora" + "\n")
            cuadro_texto.insert(tk.END, divisorias)

            # Insertar los movimientos en el cuadro de texto
            for movimiento in movimientos:
                usuario, accion, fecha_hora = movimiento.strip().split(",")
                #'usuario.ljust(20)' y 'accion.ljust(20)' ajustan el contenido de las variables 'usuario' y 'accion' para que ocupen al menos 20 caracteres, alineando a la izquierda
                cuadro_texto.insert(tk.END, usuario.ljust(20) + " | " + accion.ljust(20) + " | " + fecha_hora + "\n")

            cuadro_texto.config(state=tk.DISABLED)  # Hacemos el cuadro de texto de solo lectura
            cuadro_texto.pack(padx=10, pady=10)     # Empaquetar y mostrar el cuadro de texto en la ventana emergente

        else:
            # Si no hay movimientos registrados, muestra un mensaje informativo
            messagebox.showinfo("Movimientos Registrados", "No hay movimientos registrados.")
    except FileNotFoundError:
        # Si el archivo no se encuentra, muestra un mensaje de error
        messagebox.showerror("Error", "No se encontró el archivo 'registro.txt'.")
#================================================================================================================================================================================================

# Función para ver los usuarios existentes (solo para el usuario "admin")
def ver_usuarios_existentes():
    try:
        with open("usuarios.txt", "r") as file:
            usuarios = [line.strip().split(",")[0] for line in file]

        if usuarios:
            # Crear una ventana emergente para mostrar los usuarios existentes
            ventana_usuarios = tk.Toplevel()
            ventana_usuarios.title("Usuarios Existentes")

            # Cuadro de texto para mostrar los usuarios
            cuadro_texto = tk.Text(ventana_usuarios, wrap=tk.WORD, width=90, height=100)
            cuadro_texto.pack(padx=100, pady=100)

            # Insertar los usuarios en el cuadro de texto con divisiones horizontales
            for usuario in usuarios:
                cuadro_texto.insert(tk.END, usuario + "\n")
                cuadro_texto.insert(tk.END, "-" * 90 + "\n")  # División horizontal

            cuadro_texto.config(state=tk.DISABLED)  # Hacemos el cuadro de texto de solo lectura

        else:
            messagebox.showinfo("Usuarios existentes", "No hay usuarios registrados en el sistema.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo 'usuarios.txt'.")
#================================================================================================================================================================================================        

# Función para mostrar el menú de "Modificar usuarios existentes" (solo para el usuario "admin")
def mostrar_menu_modificar_usuarios():
    # Crear una ventana emergente para el menú de "Modificar usuarios existentes"
    ventana_modificar_usuarios = tk.Toplevel()
    ventana_modificar_usuarios.title("Modificar usuarios existentes")
    
    ventana_modificar_usuarios.geometry("250x200")  # Ajusta las dimensiones según tus necesidades
    # Botones para cada opción del menú
    boton_agregar_usuario = tk.Button(ventana_modificar_usuarios, text="Agregar usuario", command=lambda: crear_usuario(ventana_modificar_usuarios), bg="lime", fg="black", width=35, font=("Helvetica", font_size_boton))
    boton_cambiar_contrasena = tk.Button(ventana_modificar_usuarios, text="Cambiar contraseña de usuario existente", command=lambda: cambiar_contrasena(ventana_modificar_usuarios), bg="green", fg="black", width=35, font=("Helvetica", font_size_boton))
    boton_borrar_usuario = tk.Button(ventana_modificar_usuarios, text="Borrar usuario", command=lambda: borrar_usuario(ventana_modificar_usuarios), bg="teal", fg="black", width=35, font=("Helvetica", font_size_boton))

    boton_agregar_usuario.pack(pady=5)
    boton_cambiar_contrasena.pack(pady=5)
    boton_borrar_usuario.pack(pady=5)
#================================================================================================================================================================================================

# Funcion para crear usuario (SOLO PUEDE ACCEDER ADMIN)
def crear_usuario(ventana_modificar_usuarios):
    nuevo_usuario = simpledialog.askstring("Crear usuario", "Ingrese el nombre del nuevo usuario:")
    if nuevo_usuario:
        contrasena_nuevo_usuario = simpledialog.askstring("Crear usuario", f"Ingrese la contraseña para el usuario '{nuevo_usuario}':")
        if contrasena_nuevo_usuario:
            with open("usuarios.txt", "a") as file:
                file.write(f"{nuevo_usuario},{contrasena_nuevo_usuario}\n")
            messagebox.showinfo("Usuario creado", f"Se ha creado el usuario '{nuevo_usuario}'.")
    ventana_modificar_usuarios.destroy()  # Cerrar la ventana emergente
#================================================================================================================================================================================================

# Funcion para cambiar contraseña de algun usuario determinado (SOLO PUEDE ACCEDER ADMIN)
def cambiar_contrasena(ventana_modificar_usuarios):
    usuario_a_cambiar = simpledialog.askstring("Cambiar contraseña", "Ingrese el nombre del usuario cuya contraseña desea cambiar:")
    if usuario_a_cambiar:
        with open("usuarios.txt", "r") as file:
            usuarios = [line.strip().split(",")[0] for line in file]
        if usuario_a_cambiar in usuarios:
            nueva_contrasena = simpledialog.askstring("Cambiar contraseña", "Ingrese la nueva contraseña:")
            if nueva_contrasena:
                with open("usuarios.txt", "r") as file:
                    lineas = file.readlines()
                with open("usuarios.txt", "w") as file:
                    for linea in lineas:
                        usuario, contrasena = linea.strip().split(",")
                        if usuario == usuario_a_cambiar:
                            file.write(f"{usuario},{nueva_contrasena}\n")
                        else:
                            file.write(linea)
                messagebox.showinfo("Contraseña cambiada", f"La contraseña del usuario '{usuario_a_cambiar}' ha sido cambiada.")
        else:
            messagebox.showerror("Error", f"No se encontró el usuario '{usuario_a_cambiar}'.")
    ventana_modificar_usuarios.destroy()  # Cerrar la ventana emergente
#================================================================================================================================================================================================

# Funcion para borrar algún usuario determinado (SOLO PUEDE ACCEDER ADMIN)
def borrar_usuario(ventana_modificar_usuarios):
    usuario_a_borrar = simpledialog.askstring("Borrar usuario", "Ingrese el nombre del usuario a borrar:")
    if usuario_a_borrar:
        with open("usuarios.txt", "r") as file:
            usuarios = [line.strip().split(",")[0] for line in file]
        if usuario_a_borrar in usuarios:
            respuesta = messagebox.askyesno("Confirmar borrado", f"¿Está seguro de que desea borrar el usuario '{usuario_a_borrar}'?")
            if respuesta:
                with open("usuarios.txt", "r") as file:
                    lineas = file.readlines()
                with open("usuarios.txt", "w") as file:
                    for linea in lineas:
                        usuario, _ = linea.strip().split(",")
                        if usuario != usuario_a_borrar:
                            file.write(linea)
                messagebox.showinfo("Usuario borrado", f"El usuario '{usuario_a_borrar}' ha sido borrado del sistema.")
        else:
            messagebox.showerror("Error", f"No se encontró el usuario '{usuario_a_borrar}'.")
    ventana_modificar_usuarios.destroy()  # Cerrar la ventana emergente
#================================================================================================================================================================================================

# Función para leer los usuarios y contraseñas desde el archivo "usuarios.txt"
# Además, determina si el usuario es "admin" y muestra el menú especial en ese caso
def leer_usuarios_desde_archivo():
    usuarios = {}
    try:
        with open("usuarios.txt", "r") as file:
            for line in file:
                usuario, contrasena = line.strip().split(",")
                usuarios[usuario] = contrasena
                if usuario == "admin":
                    mostrar_menu_admin()
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo 'usuarios.txt'.")
    return usuarios
#================================================================================================================================================================================================

# Función para deshabilitar los botones de comandos después de enviar un comando
def deshabilitar_botones_comandos():
    for boton in botones_comandos:
        boton.config(state=tk.DISABLED)
#================================================================================================================================================================================================

# Función para mostrar o ocultar la contraseña ingresada
def mostrar_contrasena():
    if var_mostrar_contrasena.get():
        entrada_contrasena.config(show="")
    else:
        entrada_contrasena.config(show="*")
#================================================================================================================================================================================================

# Función para leer los usuarios y contraseñas desde el archivo "usuarios.txt"
def leer_usuarios_desde_archivo():
    usuarios = {}
    try:
        with open("usuarios.txt", "r") as file:
            for line in file:
                usuario, contrasena = line.strip().split(",")
                usuarios[usuario] = contrasena
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo 'usuarios.txt'.")
    return usuarios
#================================================================================================================================================================================================

# Función para verificar el usuario y la contraseña ingresados
def verificar_credenciales():
    global usuario_ingresado, contrasena_ingresada, comando_enviado, es_admin
    usuarios = leer_usuarios_desde_archivo()
    if entrada_usuario.get() in usuarios and entrada_contrasena.get() == usuarios[entrada_usuario.get()]:
        usuario_ingresado = True
        contrasena_ingresada = True
        comando_enviado = False
        entrada_contrasena.delete(0, tk.END)  # Borra el contenido de la entrada de contraseña
        entrada_usuario.config(state=tk.NORMAL)  # Habilita la entrada de usuario
        entrada_contrasena.config(state=tk.NORMAL)  # Habilita la entrada de contraseña
        boton_verificar.config(state=tk.NORMAL)  # Habilita el botón de verificación
        if entrada_usuario.get() == "admin":
            mostrar_menu_admin()
        else:
            es_admin = False
            habilitar_botones_comandos()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos. Inténtalo nuevamente.")
#================================================================================================================================================================================================
        
# Función para enviar el comando seleccionado al Arduino y registrar el movimiento en el archivo de registro
def enviar_comando(comando):
    global comando_enviado
    try:
        ser.write(comando.encode())  # Envía el comando como bytes al Arduino
        comando_enviado = True
        deshabilitar_botones_comandos()

        # Registrar el movimiento en el archivo de registro
        with open(archivo_registro, "a") as file:
            usuario = entrada_usuario.get()
            entrada_usuario.delete(0, tk.END)  # Borra el contenido de la entrada de usuario
            opcion_elegida = comando
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            registro = f"{usuario},{opcion_elegida},{fecha_hora}\n"
            file.write(registro)

    except serial.SerialException:
        messagebox.showerror("Error", "No se pudo enviar el comando. Asegúrate de que el Arduino esté conectado correctamente.")
#================================================================================================================================================================================================


#**************************************************************************** MAIN **************************************************************************************************************
# Crea la ventana principal de la aplicación
ventana = tk.Tk()
ventana.title("Aplicación de control Arduino")

# Cambiar el tamaño y color de la ventana principal
ventana.geometry("1000x800")  # Ajusta las dimensiones según tus necesidades

Image.MAX_IMAGE_PIXELS = None
# Cargar la imagen .png
imagen_png = Image.open("mantenimiento.png")

# Redimensionar la imagen para que no exceda un tamaño máximo (por ejemplo, 800x600 píxeles)
max_tamano = (350, 500)
imagen_png = imagen_png.resize(max_tamano, Image.LANCZOS)

imagen_tk = ImageTk.PhotoImage(imagen_png)

# Crear una etiqueta para mostrar la imagen en la ventana principal
etiqueta_imagen = tk.Label(ventana, image=imagen_tk)
etiqueta_imagen.pack()

# Etiqueta para indicar al usuario que ingrese el usuario y la contraseña
etiqueta_usuario = tk.Label(ventana, text="Usuario:", font=("Helvetica", font_size))
etiqueta_usuario.pack(pady=5)

# Cuadro de entrada para el usuario
entrada_usuario = tk.Entry(ventana, state=tk.NORMAL)  # Inicialmente habilitado
entrada_usuario.pack()

# Etiqueta para indicar al usuario que ingrese la contraseña
etiqueta_contrasena = tk.Label(ventana, text="Contraseña:", font=("Helvetica", font_size)) #font = fuente y tamaño
etiqueta_contrasena.pack(pady=5)

# Cuadro de entrada para la contraseña
entrada_contrasena = tk.Entry(ventana, show="*", state=tk.NORMAL)  # Inicialmente habilitado
entrada_contrasena.pack()

# Casilla de verificación para mostrar la contraseña
var_mostrar_contrasena = tk.BooleanVar()
casilla_mostrar_contrasena = tk.Checkbutton(ventana, text="Mostrar contraseña", variable=var_mostrar_contrasena, command=mostrar_contrasena)
casilla_mostrar_contrasena.pack()

# Botón para verificar el usuario y la contraseña
boton_verificar = tk.Button(ventana, text="Verificar", command=verificar_credenciales, state=tk.NORMAL)  # Inicialmente habilitado
boton_verificar.pack()

# Lista de comandos disponibles con sus colores de fondo
comandos = [
    ("A - Encender LED Rojo 1 vez", "red"),
    ("B - Encender LED Rojo 2 veces", "darkred"),
    ("C - Encender LED Verde 1 vez", "green"),
    ("D - Encender LED Verde 2 veces", "darkgreen")
]  # Agrega aquí los comandos que desees enviar al Arduino

botones_comandos = []

# Crea botones para cada comando con su color de fondo (inicialmente deshabilitados)
for texto, color in comandos:
    boton = tk.Button(ventana, text=texto, bg=color, command=lambda c=texto.split()[0]: enviar_comando(c), state=tk.DISABLED, width=30, font=("Helvetica", font_size_boton))
    boton.pack()
    botones_comandos.append(boton)

# Ejecuta la aplicación
ventana.mainloop()
#***********************************************************************************************************************************************************************************************
