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

        # Lista de pedidos
        self.pedidos = []

        # Frame de formulario
        frame_formulario = tk.Frame(root, padx=10, pady=10)
        frame_formulario.grid(row=0, column=0, sticky="w")

        # Campos de formulario
        tk.Label(frame_formulario, text="Nombre del Cliente:").grid(row=0, column=0)
        self.nombre_entry = tk.Entry(frame_formulario)
        self.nombre_entry.grid(row=0, column=1)

        tk.Label(frame_formulario, text="Prenda:").grid(row=1, column=0)
        self.prenda_entry = tk.Entry(frame_formulario)
        self.prenda_entry.grid(row=1, column=1)

        tk.Label(frame_formulario, text="Talla:").grid(row=2, column=0)
        self.talla_entry = tk.Entry(frame_formulario)
        self.talla_entry.grid(row=2, column=1)

        tk.Label(frame_formulario, text="Cantidad:").grid(row=3, column=0)
        self.cantidad_entry = tk.Entry(frame_formulario)
        self.cantidad_entry.grid(row=3, column=1)

        tk.Label(frame_formulario, text="Precio:").grid(row=4, column=0)
        self.precio_entry = tk.Entry(frame_formulario)
        self.precio_entry.grid(row=4, column=1)

        # Botones
        tk.Button(frame_formulario, text="Agregar Pedido", command=self.agregar_pedido).grid(row=5, column=0, columnspan=2, pady=5)

        # Frame de búsqueda
        frame_busqueda = tk.Frame(root, padx=10, pady=5)
        frame_busqueda.grid(row=1, column=0, sticky="w")

        tk.Label(frame_busqueda, text="Buscar Pedido (Cliente o Prenda):").grid(row=0, column=0)
        self.buscar_entry = tk.Entry(frame_busqueda)
        self.buscar_entry.grid(row=0, column=1)
        tk.Button(frame_busqueda, text="Buscar", command=self.buscar_pedido).grid(row=0, column=2, padx=5)
        tk.Button(frame_busqueda, text="Mostrar Todos", command=self.mostrar_todos_pedidos).grid(row=0, column=3)

        # Tabla de pedidos con columna de estado
        self.tree = ttk.Treeview(root, columns=("nombre", "prenda", "talla", "cantidad", "precio", "total", "estado"), show="headings")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("prenda", text="Prenda")
        self.tree.heading("talla", text="Talla")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("total", text="Total")
        self.tree.heading("estado", text="Estado")
        self.tree.grid(row=2, column=0, padx=10, pady=10)

        # Botones adicionales
        tk.Button(root, text="Confirmar Envío", command=self.confirmar_envio).grid(row=3, column=0, pady=10)
        tk.Button(root, text="Eliminar Pedido", command=self.eliminar_pedido).grid(row=3, column=1, pady=10)

    def agregar_pedido(self):
        nombre = self.nombre_entry.get()
        prenda = self.prenda_entry.get()
        talla = self.talla_entry.get()
        try:
            cantidad = int(self.cantidad_entry.get())
            precio = float(self.precio_entry.get())
            if nombre and prenda and talla and cantidad > 0 and precio > 0:
                pedido = Pedido(nombre, prenda, talla, cantidad, precio)
                self.pedidos.append(pedido)
                self.pedidos.sort(key=lambda p: p.fecha)  # Ordena por fecha
                self.actualizar_tabla()
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", "Por favor, llena todos los campos correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Cantidad y Precio deben ser numéricos.")

    def confirmar_envio(self):
        selected_item = self.tree.selection()
        if selected_item:
            for item in selected_item:
                pedido_values = self.tree.item(item, "values")
                nombre_cliente = pedido_values[0]
                pedido = next((p for p in self.pedidos if p.nombre == nombre_cliente and p.estado == "Pendiente"), None)
                if pedido:
                    pedido.estado = "Enviado"
                    self.actualizar_tabla()
        else:
            messagebox.showerror("Error", "Selecciona un pedido para confirmar el envío.")

    def eliminar_pedido(self):
        selected_item = self.tree.selection()
        if selected_item:
            for item in selected_item:
                pedido_values = self.tree.item(item, "values")
                nombre_cliente = pedido_values[0]
                pedido = next((p for p in self.pedidos if p.nombre == nombre_cliente), None)
                if pedido:
                    self.pedidos.remove(pedido)
                    self.actualizar_tabla()
        else:
            messagebox.showerror("Error", "Selecciona un pedido para eliminar.")

    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for pedido in self.pedidos:
            self.tree.insert("", "end", values=(pedido.nombre, pedido.prenda, pedido.talla, pedido.cantidad, pedido.precio, pedido.total, pedido.estado))

    def limpiar_campos(self):
        self.nombre_entry.delete(0, tk.END)
        self.prenda_entry.delete(0, tk.END)
        self.talla_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)

    def buscar_pedido(self):
        termino = self.buscar_entry.get().lower()
        if termino:
            for item in self.tree.get_children():
                self.tree.delete(item)
            for pedido in self.pedidos:
                if termino in pedido.nombre.lower() or termino in pedido.prenda.lower():
                    self.tree.insert("", "end", values=(pedido.nombre, pedido.prenda, pedido.talla, pedido.cantidad, pedido.precio, pedido.total, pedido.estado))

    def mostrar_todos_pedidos(self):
        self.actualizar_tabla()

# Inicialización de la aplicación
root = tk.Tk()
app = TiendaApp(root)
root.mainloop()