import tkinter as tk
from tkinter import messagebox
from pedido import PlataformaPedidos 
from producto import Interfaz 

# Función para manejar el inicio de sesión
def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    if usuario == "admin" and contrasena == "admin123":
        ventana_login.destroy()
        abrir_menu_principal()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Función para salir de la aplicación
def salir():
    ventana_login.destroy()

# Función para abrir el menú principal
def abrir_menu_principal():
    ventana_menu = tk.Tk()
    ventana_menu.title("Menú Principal")
    ventana_menu.geometry("500x350")
    ventana_menu.configure(bg="#2c3e50")
    
    label_bienvenida = tk.Label(
        ventana_menu, text="Bienvenido, Administrador", 
        font=("Arial", 16, "bold"), bg="#2c3e50", fg="white"
    )
    label_bienvenida.pack(pady=20)
    
    # Botón para agregar productos
    btn_agregar_productos = tk.Button(
        ventana_menu, text="Agregar Productos", 
        font=("Arial", 12, "bold"), width=20, bg="#27ae60", fg="white", 
        command=ventana_agregar_productos, relief="flat", cursor="hand2"
    )
    btn_agregar_productos.pack(pady=10)
    
    # Botón para gestionar pedidos
    btn_gestionar_pedidos = tk.Button(
        ventana_menu, text="Gestionar Pedidos", 
        font=("Arial", 12, "bold"), width=20, bg="#27ae60", fg="white", 
        command=ventana_agregar_pedidos, relief="flat", cursor="hand2"
    )
    btn_gestionar_pedidos.pack(pady=10)
    
    # Botón para agregar clientes nuevos
    btn_gestionar_pedidos = tk.Button(
        ventana_menu, text="Agregar Clientes", 
        font=("Arial", 12, "bold"), width=20, bg="#27ae60", fg="white", 
        command=ventana_agregar_clientes, relief="flat", cursor="hand2"
    )
    btn_gestionar_pedidos.pack(pady=10)
    
    # Botón para salir del menú principal
    btn_salir_menu = tk.Button(
        ventana_menu, text="Salir", 
        font=("Arial", 12, "bold"), width=20, bg="#e74c3c", fg="white", 
        command=ventana_menu.destroy, relief="flat", cursor="hand2"
    )
    btn_salir_menu.pack(pady=20)
    
    ventana_menu.mainloop()
    
def ventana_agregar_productos():
    ventana_producto = tk.Toplevel() 
    Interfaz(ventana_producto)
# Función para agregar pedidos
def ventana_agregar_pedidos():
    ventana_pedidos = tk.Toplevel()  
    PlataformaPedidos(ventana_pedidos)
def ventana_agregar_clientes():
     messagebox.showinfo("Agregar Clientes", "Esta funcionalidad estará disponible pronto.")


# Crear ventana de inicio de sesión
ventana_login = tk.Tk()
ventana_login.title("Inicio de Sesión")
ventana_login.geometry("400x500")
ventana_login.configure(bg="#34495e")

# Marco para el diseño del formulario
frame_formulario = tk.Frame(ventana_login, bg="#2c3e50", bd=5, relief="ridge")
frame_formulario.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400)

label_titulo = tk.Label(
    frame_formulario, text="Inicio de Sesión", 
    font=("Arial", 18, "bold"), bg="#2c3e50", fg="white"
)
label_titulo.pack(pady=20)

# Campo de usuario
label_usuario = tk.Label(
    frame_formulario, text="Usuario", 
    font=("Arial", 12), bg="#2c3e50", fg="white"
)
label_usuario.pack(pady=5)
entry_usuario = tk.Entry(frame_formulario, font=("Arial", 12), width=25, bd=2)
entry_usuario.pack(pady=5)

# Campo de contraseña
label_contrasena = tk.Label(
    frame_formulario, text="Contraseña", 
    font=("Arial", 12), bg="#2c3e50", fg="white"
)
label_contrasena.pack(pady=5)
entry_contrasena = tk.Entry(frame_formulario, font=("Arial", 12), width=25, bd=2, show="*")
entry_contrasena.pack(pady=5)

# Botón para iniciar sesión
btn_login = tk.Button(
    frame_formulario, text="Iniciar Sesión", 
    font=("Arial", 12, "bold"), bg="#27ae60", fg="white", 
    command=iniciar_sesion, relief="flat", cursor="hand2"
)
btn_login.pack(pady=15)

# Botón para salir
btn_salir = tk.Button(
    frame_formulario, text="Salir", 
    font=("Arial", 12, "bold"), bg="#e74c3c", fg="white", 
    command=salir, relief="flat", cursor="hand2"
)
btn_salir.pack(pady=10)

ventana_login.mainloop()

