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

    def eliminar_pedido(self, pedido_id):
        actual = self.cabeza
        anterior = None
        while actual:
            if actual.pedido_id == pedido_id:
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def obtener_pedido(self, pedido_id):
        actual = self.cabeza
        while actual:
            if actual.pedido_id == pedido_id:
                return actual
            actual = actual.siguiente
        return None

    def obtener_todos(self):
        pedidos = []
        actual = self.cabeza
        while actual:
            pedidos.append(actual)
            actual = actual.siguiente
        return pedidos


# Cola para gestionar pedidos pendientes de envío
class ColaPedidos:
    def __init__(self):
        self.frente = None
        self.final = None

    def encolar(self, pedido):
        if not self.final:
            self.frente = self.final = pedido
        else:
            self.final.siguiente = pedido
            self.final = pedido

    def desencolar(self):
        if not self.frente:
            return None
        pedido = self.frente
        self.frente = self.frente.siguiente
        if not self.frente:
            self.final = None
        return pedido


# Nodo para árbol binario
class NodoArbol:
    def __init__(self, pedido):
        self.pedido = pedido
        self.izquierda = None
        self.derecha = None


# Árbol binario para buscar pedidos
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

    def buscar(self, nombre):
        return self._buscar_recursivo(self.raiz, nombre)

    def _buscar_recursivo(self, nodo, nombre):
        if not nodo:
            return None
        if nodo.pedido.nombre == nombre:
            return nodo.pedido
        if nombre < nodo.pedido.nombre:
            return self._buscar_recursivo(nodo.izquierda, nombre)
        return self._buscar_recursivo(nodo.derecha, nombre)


# Interfaz gráfica con Tkinter
class PlataformaPedidos:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Pedidos - Tienda de Ropa")
        self.root.geometry("900x500")

        # Estructuras de datos
        self.lista_pedidos = ListaEnlazadaPedidos()
        self.cola_pedidos = ColaPedidos()
        self.arbol_pedidos = ArbolBinarioPedidos()

        # Variables de control
        self.nombre_cliente = tk.StringVar()
        self.prenda = tk.StringVar()
        self.talla = tk.StringVar()
        self.cantidad = tk.IntVar()
        self.precio = tk.DoubleVar()
        self.buscar_texto = tk.StringVar()

        # Sección para agregar pedidos
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

        # Añadir el campo de búsqueda
        frame_busqueda = tk.LabelFrame(self.root, text="Buscar Pedido", padx=10, pady=10)
        frame_busqueda.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_busqueda, text="Buscar por Nombre del Cliente:").grid(row=0, column=0, padx=5, pady=2)
        tk.Entry(frame_busqueda, textvariable=self.buscar_texto, width=25).grid(row=0, column=1, padx=5, pady=2)

        tk.Button(frame_busqueda, text="Buscar Pedido", command=self.buscar_pedido).grid(row=0, column=2, padx=5, pady=2)


        # Tabla para mostrar pedidos
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

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Acciones
        frame_acciones = tk.Frame(self.root)
        frame_acciones.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_acciones, text="Confirmar Envío", command=self.confirmar_envio).pack(side="left", padx=5, pady=5)
        tk.Button(frame_acciones, text="Eliminar Pedido", command=self.eliminar_pedido).pack(side="left", padx=5, pady=5)
        tk.Button(frame_acciones, text="Buscar Pedido", command=self.buscar_pedido).pack(side="left", padx=5, pady=5)

    def agregar_pedido(self):
        """Agrega un pedido a la lista enlazada y lo inserta en el árbol binario."""
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
        messagebox.showinfo("Éxito", "Pedido agregado correctamente.")

    def mostrar_todos(self):
        """Muestra todos los pedidos en la tabla."""
        self.tree.delete(*self.tree.get_children())
        for pedido in self.lista_pedidos.obtener_todos():
            self.tree.insert("", "end", values=(
                pedido.pedido_id, pedido.nombre, pedido.prenda, pedido.talla,
                pedido.cantidad, pedido.precio, pedido.total, pedido.estado
            ))

    def confirmar_envio(self):
        """Confirma el envío del pedido seleccionado."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Seleccione un pedido para confirmar el envío.")
            return

        item = seleccion[0]
        pedido_id = int(self.tree.item(item, "values")[0])
        pedido = self.lista_pedidos.obtener_pedido(pedido_id)
        if pedido and pedido.estado == "Pendiente":
            pedido.estado = "Enviado"
            self.cola_pedidos.encolar(pedido)
            messagebox.showinfo("Éxito", f"Pedido {pedido_id} enviado correctamente.")
        else:
            messagebox.showwarning("Error", "El pedido ya ha sido enviado.")

        self.mostrar_todos()

    def eliminar_pedido(self):
        """Elimina el pedido seleccionado de la lista enlazada."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Seleccione un pedido para eliminar.")
            return

        item = seleccion[0]
        pedido_id = int(self.tree.item(item, "values")[0])
        if self.lista_pedidos.eliminar_pedido(pedido_id):
            messagebox.showinfo("Éxito", f"Pedido {pedido_id} eliminado correctamente.")
            self.mostrar_todos()
        else:
            messagebox.showwarning("Error", "No se pudo eliminar el pedido.")

    def buscar_pedido(self):
        """Busca un pedido en el árbol binario y lo muestra en la tabla."""
        nombre = self.buscar_texto.get().strip()  # Obtener el nombre del cliente ingresado
        if not nombre:
            messagebox.showwarning("Error", "Ingrese un nombre para buscar.")
            return

        # Realizar la búsqueda en el árbol binario
        pedido = self.arbol_pedidos.buscar(nombre)
        self.tree.delete(*self.tree.get_children())  # Limpiar la tabla antes de mostrar el resultado
        if pedido:
            # Insertar el pedido encontrado en la tabla
            self.tree.insert("", "end", values=(
                pedido.pedido_id, pedido.nombre, pedido.prenda, pedido.talla,
                pedido.cantidad, pedido.precio, pedido.total, pedido.estado
            ))
        else:
            # Mostrar mensaje en la tabla indicando que no hay resultados
            messagebox.showinfo("Resultado", "No se encontró un pedido con ese nombre.")



# Crear ventana principal
root = tk.Tk()
app = PlataformaPedidos(root)
root.mainloop()