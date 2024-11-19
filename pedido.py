import tkinter as tk
from tkinter import ttk, messagebox


# Clase para representar un pedido
class Pedido:
    def __init__(self, modelo, marca, fecha_entrega, cantidad, precio, total, cliente, direccion, id=None):
        self.id = id
        self.modelo = modelo
        self.marca = marca
        self.fecha_entrega = fecha_entrega
        self.cantidad = cantidad
        self.precio = precio
        self.total = total
        self.cliente = cliente
        self.direccion = direccion

    def __str__(self):
        return f"ID: {self.id} | Modelo: {self.modelo} | Marca: {self.marca} | Fecha: {self.fecha_entrega} | Cantidad: {self.cantidad} | Precio: {self.precio} | Total: {self.total} | Cliente: {self.cliente} | Dirección: {self.direccion}"


# Clase para el nodo del árbol binario
class Binario:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data


# Insertar un nodo en el árbol binario
def insertNode(root, nodo):
    if root is None:
        root = nodo
    else:
        if root.data.cliente > nodo.data.cliente:  # Comparar por nombre de cliente
            if root.left is None:
                root.left = nodo
            else:
                insertNode(root.left, nodo)
        else:
            if root.right is None:
                root.right = nodo
            else:
                insertNode(root.right, nodo)


# Buscar un pedido por cliente en el árbol binario
def find(root, data, app):
    if root is None:
        return None

    # Si se encuentra el cliente, se muestra el pedido
    if data.lower() in root.data.cliente.lower():
        app.mostrar_pedido(root.data)

    # Recursión en el subárbol izquierdo o derecho
    if root.data.cliente > data:
        find(root.left, data, app)
    elif root.data.cliente < data:
        find(root.right, data, app)


# Mostrar un pedido en la interfaz
def mostrar_pedido(pedido, app):
    app.tree.insert("", "end", values=(pedido.id, pedido.modelo, pedido.marca, pedido.fecha_entrega,
                                       pedido.cantidad, pedido.precio, pedido.total, pedido.cliente, pedido.direccion))


# Clase para la cola dinámica
class ListaDinamica:
    def __init__(self, limite=5):
        self.cola = []
        self.limite = limite
        self.front = None
        self.rear = None
        self.size = 0

    def isEmpty(self):
        return self.size <= 0

    def enColar(self, item):
        if self.size >= self.limite:
            self.resize()
        self.cola.append(item)

        if self.front is None:
            self.front = self.rear = 0
        else:
            self.rear = self.size

        self.size += 1

    def desencolar(self):
        if self.isEmpty():
            return None
        dato = self.cola.pop(0)
        self.size -= 1
        if self.size == 0:
            self.front = self.rear = None
        else:
            self.rear = self.size - 1
        return dato

    def getSize(self):
        return self.size

    def resize(self):
        new_cola = list(self.cola)
        self.limite = 2 * self.limite
        self.cola = new_cola

    def getQue(self):
        return self.cola


# Clase principal para la interfaz
class PlataformaPedidos:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Pedidos - Tienda de Ropa")
        self.root.geometry("900x600")

        # Estructuras de datos
        self.cola_pedidos = ListaDinamica()  # Cola dinámica
        self.arbol_pedidos = None  # Árbol binario de pedidos

        # Variables de control
        self.modelo = tk.StringVar()
        self.marca = tk.StringVar()
        self.fecha_entrega = tk.StringVar()
        self.cantidad = tk.IntVar()
        self.precio = tk.DoubleVar()
        self.cliente = tk.StringVar()
        self.direccion = tk.StringVar()
        self.buscar_texto = tk.StringVar()

        # Generador de ID para los pedidos
        self.id_generador = 1  # Variable que se incrementará automáticamente al agregar cada pedido

        # Sección para agregar pedidos
        frame_ingreso = tk.LabelFrame(self.root, text="Ingreso de Pedidos", padx=10, pady=10)
        frame_ingreso.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_ingreso, text="Modelo:").grid(row=0, column=0, padx=5, pady=2)
        tk.Entry(frame_ingreso, textvariable=self.modelo, width=25).grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_ingreso, text="Marca:").grid(row=1, column=0, padx=5, pady=2)
        tk.Entry(frame_ingreso, textvariable=self.marca, width=25).grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_ingreso, text="Fecha de Entrega:").grid(row=0, column=2, padx=5, pady=2)
        tk.Entry(frame_ingreso, textvariable=self.fecha_entrega, width=15).grid(row=0, column=3, padx=5, pady=2)

        tk.Label(frame_ingreso, text="Cantidad:").grid(row=1, column=2, padx=5, pady=2)
        tk.Entry(frame_ingreso, textvariable=self.cantidad, width=10).grid(row=1, column=3, padx=5, pady=2)

        tk.Label(frame_ingreso, text="Precio:").grid(row=0, column=4, padx=5, pady=2)
        tk.Entry(frame_ingreso, textvariable=self.precio, width=10).grid(row=0, column=5, padx=5, pady=2)

        tk.Label(frame_ingreso, text="Cliente:").grid(row=1, column=4, padx=5, pady=2)
        tk.Entry(frame_ingreso, textvariable=self.cliente, width=25).grid(row=1, column=5, padx=5, pady=2)

        tk.Label(frame_ingreso, text="Dirección:").grid(row=0, column=6, padx=5, pady=2)
        tk.Entry(frame_ingreso, textvariable=self.direccion, width=25).grid(row=0, column=7, padx=5, pady=2)

        tk.Button(frame_ingreso, text="Agregar Pedido", command=self.agregar_pedido).grid(row=1, column=6, columnspan=2, pady=5)

        # Añadir el campo de búsqueda
        frame_busqueda = tk.LabelFrame(self.root, text="Buscar Pedido", padx=10, pady=10)
        frame_busqueda.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_busqueda, text="Buscar por Cliente:").grid(row=0, column=0, padx=5, pady=2)
        tk.Entry(frame_busqueda, textvariable=self.buscar_texto, width=25).grid(row=0, column=1, padx=5, pady=2)

        tk.Button(frame_busqueda, text="Buscar Pedido", command=self.buscar_pedido).grid(row=0, column=2, padx=5, pady=2)

        # Tabla para mostrar pedidos
        self.tree = ttk.Treeview(self.root, columns=("ID", "Modelo", "Marca", "Fecha Entrega", "Cantidad", "Precio", "Total", "Cliente", "Dirección"))
        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("ID", text="ID", anchor="w")
        self.tree.heading("Modelo", text="Modelo", anchor="w")
        self.tree.heading("Marca", text="Marca", anchor="w")
        self.tree.heading("Fecha Entrega", text="Fecha Entrega", anchor="w")
        self.tree.heading("Cantidad", text="Cantidad", anchor="w")
        self.tree.heading("Precio", text="Precio", anchor="w")
        self.tree.heading("Total", text="Total", anchor="w")
        self.tree.heading("Cliente", text="Cliente", anchor="w")
        self.tree.heading("Dirección", text="Dirección", anchor="w")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor="w", width=50)
        self.tree.column("Modelo", anchor="w", width=120)
        self.tree.column("Marca", anchor="w", width=100)
        self.tree.column("Fecha Entrega", anchor="w", width=100)
        self.tree.column("Cantidad", anchor="w", width=80)
        self.tree.column("Precio", anchor="w", width=80)
        self.tree.column("Total", anchor="w", width=80)
        self.tree.column("Cliente", anchor="w", width=150)
        self.tree.column("Dirección", anchor="w", width=150)

        self.tree.pack(fill="both", padx=10, pady=10)

    # Método para agregar un pedido
    def agregar_pedido(self):
        modelo = self.modelo.get()
        marca = self.marca.get()
        fecha_entrega = self.fecha_entrega.get()
        cantidad = self.cantidad.get()
        precio = self.precio.get()
        total = cantidad * precio
        cliente = self.cliente.get()
        direccion = self.direccion.get()

        pedido = Pedido(modelo, marca, fecha_entrega, cantidad, precio, total, cliente, direccion, id=self.id_generador)

        # Generar un ID único para el pedido
        self.id_generador += 1

        # Agregar a la cola
        self.cola_pedidos.enColar(pedido)

        # Insertar en el árbol binario
        nodo = Binario(pedido)
        if self.arbol_pedidos is None:
            self.arbol_pedidos = nodo
        else:
            insertNode(self.arbol_pedidos, nodo)

        messagebox.showinfo("Éxito", "Pedido agregado correctamente.")

        # Limpiar los campos
        self.modelo.set("")
        self.marca.set("")
        self.fecha_entrega.set("")
        self.cantidad.set(0)
        self.precio.set(0.0)
        self.cliente.set("")
        self.direccion.set("")

    # Método para buscar pedidos por cliente
    def buscar_pedido(self):
        cliente = self.buscar_texto.get()
        self.tree.delete(*self.tree.get_children())  # Limpiar la tabla de la búsqueda previa

        # Buscar en el árbol binario y mostrar los pedidos encontrados
        find(self.arbol_pedidos, cliente, self)


# Crear la ventana de la aplicación
root = tk.Tk()
app = PlataformaPedidos(root)
root.mainloop()
