import tkinter as tk
from tkinter import ttk, messagebox


# Nodo para lista enlazada
class NodoPedido:
    def __init__(self, pedido_id, nombre, prenda, talla, cantidad, precio, estado="Pendiente"):
        self.pedido_id = pedido_id
        self.nombre = nombre
        self.prenda = prenda
        self.talla = talla
        self.cantidad = cantidad
        self.precio = precio
        self.total = cantidad * precio
        self.estado = estado
        self.siguiente = None


# Lista enlazada para gestionar pedidos
class ListaEnlazadaPedidos:
    def __init__(self):
        self.cabeza = None
        self.id_actual = 1

    def agregar_pedido(self, nombre, prenda, talla, cantidad, precio):
        nuevo_pedido = NodoPedido(self.id_actual, nombre, prenda, talla, cantidad, precio)
        self.id_actual += 1
        if not self.cabeza:
            self.cabeza = nuevo_pedido
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_pedido

    def obtener_todos(self):
        pedidos = []
        actual = self.cabeza
        while actual:
            pedidos.append(actual)
            actual = actual.siguiente
        return pedidos

    def obtener_pedido(self, pedido_id):
        actual = self.cabeza
        while actual:
            if actual.pedido_id == pedido_id:
                return actual
            actual = actual.siguiente
        return None
    
# Clase para manejar la lista enlazada de resultados
class ListaResultados:
    def __init__(self):
        self.cabeza = None

    def agregar(self, pedido):
        nuevo_nodo = NodoPedido(
            pedido.pedido_id, pedido.nombre, pedido.prenda, pedido.talla,
            pedido.cantidad, pedido.precio, pedido.estado
        )
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener_todos(self):
        pedidos = []
        actual = self.cabeza
        while actual:
            pedidos.append(actual)
            actual = actual.siguiente
        return pedidos


# Nodo para árbol binario
class NodoArbol:
    def __init__(self, pedido):
        self.pedido = pedido
        self.izquierda = None
        self.derecha = None


# Árbol binario para búsquedas
class ArbolBinarioPedidos:
    def __init__(self):
        self.raiz = None

    def insertar(self, pedido):
        if not self.raiz:
            self.raiz = NodoArbol(pedido)
        else:
            self._insertar_recursivo(self.raiz, pedido)

    def _insertar_recursivo(self, nodo, pedido):
        if pedido.nombre < nodo.pedido.nombre:
            if nodo.izquierda:
                self._insertar_recursivo(nodo.izquierda, pedido)
            else:
                nodo.izquierda = NodoArbol(pedido)
        else:
            if nodo.derecha:
                self._insertar_recursivo(nodo.derecha, pedido)
            else:
                nodo.derecha = NodoArbol(pedido)

    def buscar_y_transferir(self, nombre, lista_resultados):
        """Busca todos los pedidos con el nombre especificado y los transfiere a la lista enlazada."""
        self._buscar_recursivo(self.raiz, nombre, lista_resultados)

    def _buscar_recursivo(self, nodo, nombre, lista_resultados):
        if not nodo:
            return
        if nodo.pedido.nombre == nombre:
            lista_resultados.agregar(nodo.pedido)
        self._buscar_recursivo(nodo.izquierda, nombre, lista_resultados)
        self._buscar_recursivo(nodo.derecha, nombre, lista_resultados)


# Nodo para la cola
class NodoCola:
    def __init__(self, pedido):
        self.pedido = pedido
        self.siguiente = None


# Cola para gestionar pedidos pendientes de cambio de estado
class ColaPedidos:
    def __init__(self):
        self.frente = None
        self.final = None

    def encolar(self, pedido):
        nuevo_nodo = NodoCola(pedido)
        if not self.final:
            self.frente = self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo

    def desencolar(self):
        if not self.frente:
            return None
        pedido = self.frente.pedido
        self.frente = self.frente.siguiente
        if not self.frente:
            self.final = None
        return pedido

    def vaciar(self):
        self.frente = self.final = None

    def obtener_todos(self):
        pedidos = []
        actual = self.frente
        while actual:
            pedidos.append(actual.pedido)
            actual = actual.siguiente
        return pedidos


# Plataforma de gestión con Tkinter
class PlataformaPedidos:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Pedidos")
        self.root.geometry("950x700")

        # Estructuras de datos
        self.lista_pedidos = ListaEnlazadaPedidos()
        self.arbol_pedidos = ArbolBinarioPedidos()
        self.cola_pedidos = ColaPedidos()

        # Variables de control
        self.nombre_cliente = tk.StringVar()
        self.prenda = tk.StringVar()
        self.talla = tk.StringVar()
        self.cantidad = tk.IntVar()
        self.precio = tk.DoubleVar()
        self.buscar_texto = tk.StringVar()

        frame_ingreso = tk.LabelFrame(self.root, text="Ingreso de Pedidos", padx=10, pady=10)
        frame_ingreso.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_ingreso, text="Nombre del Cliente:").grid(row=0, column=0, padx=5, pady=2)
        tk.Entry(frame_ingreso, textvariable=self.nombre_cliente, width=25).grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_ingreso, text="Prenda:").grid(row=1, column=0, padx=5, pady=2)
        tk.Entry(frame_ingreso, textvariable=self.prenda, width=25).grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_ingreso, text="Talla:").grid(row=0, column=2, padx=5, pady=2)
        tk.Entry(frame_ingreso, textvariable=self.talla, width=10).grid(row=0, column=3, padx=5, pady=2)

        tk.Label(frame_ingreso, text="Cantidad:").grid(row=1, column=2, padx=5, pady=2)
        tk.Entry(frame_ingreso, textvariable=self.cantidad, width=10).grid(row=1, column=3, padx=5, pady=2)

        tk.Label(frame_ingreso, text="Precio:").grid(row=0, column=4, padx=5, pady=2)
        tk.Entry(frame_ingreso, textvariable=self.precio, width=10).grid(row=0, column=5, padx=5, pady=2)

        tk.Button(frame_ingreso, text="Agregar Pedido", command=self.agregar_pedido).grid(
            row=1, column=4, columnspan=2, pady=5
        )

        frame_busqueda = tk.LabelFrame(self.root, text="Buscar Pedido", padx=10, pady=10)
        frame_busqueda.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_busqueda, text="Buscar por nombre:").grid(row=0, column=0, padx=5, pady=2)
        tk.Entry(frame_busqueda, textvariable=self.buscar_texto, width=25).grid(row=0, column=1, padx=5, pady=2)

        tk.Button(frame_busqueda, text="Buscar Pedido", command=self.buscar_pedido).grid(row=0, column=2, padx=5, pady=2)
        tk.Button(frame_busqueda, text="Mostrar Todos", command=self.mostrar_todos).grid(row=0, column=3, padx=5, pady=2)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Nombre", "Prenda", "Talla", "Cantidad", "Precio", "Total", "Estado"))
        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("ID", text="ID", anchor="w")
        self.tree.heading("Nombre", text="Nombre", anchor="w")
        self.tree.heading("Prenda", text="Prenda", anchor="w")
        self.tree.heading("Talla", text="Talla", anchor="w")
        self.tree.heading("Cantidad", text="Cantidad", anchor="w")
        self.tree.heading("Precio", text="Precio", anchor="w")
        self.tree.heading("Total", text="Total", anchor="w")
        self.tree.heading("Estado", text="Estado", anchor="w")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor="w", width=50)
        self.tree.column("Nombre", anchor="w", width=150)
        self.tree.column("Prenda", anchor="w", width=100)
        self.tree.column("Talla", anchor="w", width=80)
        self.tree.column("Cantidad", anchor="w", width=80)
        self.tree.column("Precio", anchor="w", width=80)
        self.tree.column("Total", anchor="w", width=80)
        self.tree.column("Estado", anchor="w", width=100)

        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        frame_acciones = tk.Frame(self.root)
        frame_acciones.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_acciones, text="Cambiar Estado", command=self.cambiar_estado).pack(side="left", padx=5, pady=5)

        frame_confirmar = tk.Frame(self.root)
        frame_confirmar.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_confirmar, text="Aceptar", command=self.aceptar_cambios).pack(side="left", padx=5, pady=5)
        tk.Button(frame_confirmar, text="Cancelar", command=self.cancelar_cambios).pack(side="right", padx=5, pady=5)

    def agregar_pedido(self):
        if not self.nombre_cliente.get() or not self.prenda.get() or not self.cantidad.get() or not self.precio.get():
            messagebox.showwarning("Error", "Todos los campos deben ser llenados.")
            return

        self.lista_pedidos.agregar_pedido(
            self.nombre_cliente.get(),
            self.prenda.get(),
            self.talla.get(),
            self.cantidad.get(),
            self.precio.get(),
        )
        ultimo_pedido = self.lista_pedidos.obtener_todos()[-1]
        self.arbol_pedidos.insertar(ultimo_pedido)
        self.mostrar_todos()

    def mostrar_todos(self):
        self.tree.delete(*self.tree.get_children())
        for pedido in self.lista_pedidos.obtener_todos():
            self.tree.insert("", "end", values=(
                pedido.pedido_id, pedido.nombre, pedido.prenda, pedido.talla,
                pedido.cantidad, pedido.precio, pedido.total, pedido.estado
            ))

    def buscar_pedido(self):
        texto = self.buscar_texto.get().strip()
        self.tree.delete(*self.tree.get_children())

        # Crear una lista enlazada para almacenar los resultados
        lista_resultados = ListaResultados()

        # Buscar en el árbol binario y transferir a la lista enlazada
        self.arbol_pedidos.buscar_y_transferir(texto, lista_resultados)

        # Mostrar los resultados desde la lista enlazada
        resultados = lista_resultados.obtener_todos()

        if resultados:
            for pedido in resultados:
                self.tree.insert("", "end", values=(
                    pedido.pedido_id, pedido.nombre, pedido.prenda, pedido.talla,
                    pedido.cantidad, pedido.precio, pedido.total, pedido.estado
                ))
        else:
            messagebox.showinfo("Resultado", "No se encontraron pedidos con ese criterio.")


    def cambiar_estado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Seleccione un pedido para cambiar el estado.")
            return

        for item in seleccion:
            pedido_id = int(self.tree.item(item, "values")[0])
            pedido = self.lista_pedidos.obtener_pedido(pedido_id)
            if pedido:
                self.cola_pedidos.encolar(pedido)

        messagebox.showinfo("Cambiar Estado", "Pedidos agregados a la cola para cambiar estado.")
        while True:
            pedido = self.cola_pedidos.desencolar()
            if not pedido:
                break
            if pedido.estado == "Pendiente":
                pedido.estado = "Enviado"
            elif pedido.estado == "Enviado":
                pedido.estado = "Pendiente"

        self.mostrar_todos()
        messagebox.showinfo("Éxito", "Se han aplicado los cambios a los estados de los pedidos.")
    
    def aceptar_cambios(self):
        while True:
            pedido = self.cola_pedidos.desencolar()
            if not pedido:
                break
            if pedido.estado == "Pendiente":
                pedido.estado = "Enviado"
            elif pedido.estado == "Enviado":
                pedido.estado = "Pendiente"

        self.mostrar_todos()
        messagebox.showinfo("Éxito", "Se han aplicado los cambios a los estados de los pedidos.")

    def cancelar_cambios(self):
        self.cola_pedidos.vaciar()
        messagebox.showinfo("Cancelado", "Todos los cambios han sido descartados.")


# Crear ventana principal
root = tk.Tk()
app = PlataformaPedidos(root)
root.mainloop()
