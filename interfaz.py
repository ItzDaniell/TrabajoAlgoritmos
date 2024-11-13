import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Pedido:
    def __init__(self, nombre, prenda, talla, cantidad, precio, estado="Pendiente"):
        self.nombre = nombre
        self.prenda = prenda
        self.talla = talla
        self.cantidad = cantidad
        self.precio = precio
        self.total = cantidad * precio
        self.estado = estado
        self.fecha = datetime.now()  # Fecha y hora de creación del pedido

class TiendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Pedidos - Tienda de Ropa")
        self.pedidos = []

        self.crear_interfaz()

    def crear_interfaz(self):
        self.crear_formulario()
        self.crear_busqueda()
        self.crear_tabla()
        self.crear_botones()

    def crear_formulario(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.grid(row=0, column=0, sticky="w")

        campos = ["Nombre del Cliente", "Prenda", "Talla", "Cantidad", "Precio"]
        self.entradas = {}

        for i, campo in enumerate(campos):
            tk.Label(frame, text=f"{campo}:").grid(row=i, column=0)
            entrada = tk.Entry(frame)
            entrada.grid(row=i, column=1)
            self.entradas[campo.lower()] = entrada

        tk.Button(frame, text="Agregar Pedido", command=self.agregar_pedido).grid(row=len(campos), column=0, columnspan=2, pady=5)

    def crear_busqueda(self):
        frame = tk.Frame(self.root, padx=10, pady=5)
        frame.grid(row=1, column=0, sticky="w")

        tk.Label(frame, text="Buscar Pedido (Cliente o Prenda):").grid(row=0, column=0)
        self.buscar_entry = tk.Entry(frame)
        self.buscar_entry.grid(row=0, column=1)

        tk.Button(frame, text="Buscar", command=self.buscar_pedido).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Mostrar Todos", command=self.mostrar_todos_pedidos).grid(row=0, column=3)

    def crear_tabla(self):
        columnas = ["nombre", "prenda", "talla", "cantidad", "precio", "total", "estado"]
        self.tree = ttk.Treeview(self.root, columns=columnas, show="headings")

        for col in columnas:
            self.tree.heading(col, text=col.capitalize())

        self.tree.grid(row=2, column=0, padx=10, pady=10)

    def crear_botones(self):
        frame = tk.Frame(self.root)
        frame.grid(row=3, column=0, pady=10)

        acciones = [
            ("Confirmar Envío", self.confirmar_envio),
            ("Eliminar Pedido", self.eliminar_pedido),
            ("Editar Pedido", self.editar_pedido),
        ]

        for i, (text, command) in enumerate(acciones):
            tk.Button(frame, text=text, command=command).grid(row=0, column=i, padx=5)

    def agregar_pedido(self):
        try:
            datos = {campo: entrada.get() for campo, entrada in self.entradas.items()}
            datos["cantidad"] = int(datos["cantidad"])
            datos["precio"] = float(datos["precio"])

            if all(datos.values()) and datos["cantidad"] > 0 and datos["precio"] > 0:
                nuevo_pedido = Pedido(**datos)
                self.pedidos.append(nuevo_pedido)
                self.actualizar_tabla()
                self.limpiar_campos()
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor, verifica los campos: Cantidad y Precio deben ser números positivos.")

    def confirmar_envio(self):
        self.actualizar_estado_pedido("Enviado")

    def eliminar_pedido(self):
        self.actualizar_estado_pedido("Eliminar")

    def editar_pedido(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona un pedido para editar.")
            return

        item = self.tree.item(selected[0], "values")
        pedido = self.buscar_pedido_por_nombre(item[0])
        if pedido:
            for campo, valor in pedido.__dict__.items():
                if campo in self.entradas:
                    self.entradas[campo].delete(0, tk.END)
                    self.entradas[campo].insert(0, valor)
            self.pedidos.remove(pedido)
            self.actualizar_tabla()

    def buscar_pedido_por_nombre(self, nombre):
        return next((p for p in self.pedidos if p.nombre == nombre), None)

    def actualizar_estado_pedido(self, nuevo_estado):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona un pedido.")
            return

        for item in selected:
            valores = self.tree.item(item, "values")
            pedido = self.buscar_pedido_por_nombre(valores[0])

            if pedido:
                if nuevo_estado == "Eliminar":
                    self.pedidos.remove(pedido)
                else:
                    pedido.estado = nuevo_estado

        self.actualizar_tabla()

    def buscar_pedido(self):
        termino = self.buscar_entry.get().lower()
        pedidos_filtrados = [
            p for p in self.pedidos if termino in p.nombre.lower() or termino in p.prenda.lower()
        ]
        self.actualizar_tabla(pedidos_filtrados)

    def actualizar_tabla(self, pedidos=None):
        self.tree.delete(*self.tree.get_children())
        for pedido in pedidos or self.pedidos:
            self.tree.insert("", "end", values=(pedido.nombre, pedido.prenda, pedido.talla, pedido.cantidad, pedido.precio, pedido.total, pedido.estado))

    def mostrar_todos_pedidos(self):
        self.actualizar_tabla()

    def limpiar_campos(self):
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

# Inicializar aplicación
root = tk.Tk()
app = TiendaApp(root)
root.mainloop()