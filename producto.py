import tkinter as tk
from tkinter import ttk, messagebox

# Clase NodoTalla: Representa cada talla con su stock y precio
class NodoTalla:
    def __init__(self, talla, stock, precio):
        self.talla = talla
        self.stock = stock
        self.precio = precio
        self.siguiente = None  # Puntero al siguiente nodo

# Clase ListaTallas: Representa una lista enlazada de tallas
class ListaTallas:
    def __init__(self):
        self.cabeza = None  # Puntero inicial de la lista

    def agregar_talla(self, talla, stock, precio):
        nuevo_nodo = NodoTalla(talla, stock, precio)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener_tallas(self):
        """Devuelve una lista con los datos de las tallas."""
        tallas = []
        actual = self.cabeza
        while actual:
            tallas.append((actual.talla, actual.stock, actual.precio))
            actual = actual.siguiente
        return tallas

# Clase Modelo: Representa un modelo asociado a una lista de tallas
class Modelo:
    def __init__(self, nombre, prenda, marca):
        self.nombre = nombre
        self.prenda = prenda
        self.marca = marca
        self.tallas = ListaTallas()

# Clase Interfaz: Representa la interfaz gráfica
class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Modelos y Tallas")
        self.root.geometry("800x600")

        # Lista de modelos
        self.modelos = []

        # Tabla para modelos
        self.lbl_modelos = tk.Label(root, text="Modelos", font=("Arial", 12, "bold"))
        self.lbl_modelos.pack(pady=5)
        self.tree_modelos = ttk.Treeview(root, columns=("Nombre", "Prenda", "Marca"), show="headings", height=5)
        self.tree_modelos.heading("Nombre", text="Nombre")
        self.tree_modelos.heading("Prenda", text="Prenda")
        self.tree_modelos.heading("Marca", text="Marca")
        self.tree_modelos.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)
        self.tree_modelos.bind("<Double-1>", self.seleccionar_modelo)

        # Botón para crear nuevo modelo
        self.btn_nuevo_modelo = tk.Button(root, text="Crear Nuevo Modelo", command=self.crear_modelo)
        self.btn_nuevo_modelo.pack(pady=10)

        # Tabla para tallas
        self.lbl_tallas = tk.Label(root, text="Tallas del Modelo Seleccionado", font=("Arial", 12, "bold"))
        self.lbl_tallas.pack(pady=5)
        self.tree_tallas = ttk.Treeview(root, columns=("Talla", "Stock", "Precio"), show="headings", height=8)
        self.tree_tallas.heading("Talla", text="Talla")
        self.tree_tallas.heading("Stock", text="Stock")
        self.tree_tallas.heading("Precio", text="Precio")
        self.tree_tallas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Formulario para gestionar tallas
        self.frame_formulario = tk.Frame(root)
        self.frame_formulario.pack(pady=10)

        self.lbl_talla = tk.Label(self.frame_formulario, text="Talla:")
        self.lbl_talla.grid(row=0, column=0, padx=5)
        self.entry_talla = tk.Entry(self.frame_formulario)
        self.entry_talla.grid(row=0, column=1, padx=5)

        self.lbl_stock = tk.Label(self.frame_formulario, text="Stock:")
        self.lbl_stock.grid(row=0, column=2, padx=5)
        self.entry_stock = tk.Entry(self.frame_formulario)
        self.entry_stock.grid(row=0, column=3, padx=5)

        self.lbl_precio = tk.Label(self.frame_formulario, text="Precio:")
        self.lbl_precio.grid(row=0, column=4, padx=5)
        self.entry_precio = tk.Entry(self.frame_formulario)
        self.entry_precio.grid(row=0, column=5, padx=5)

        # Botones para gestionar tallas
        self.btn_agregar_talla = tk.Button(root, text="Agregar Talla", command=self.agregar_talla)
        self.btn_agregar_talla.pack(pady=5)

        self.modelo_seleccionado = None

    def crear_modelo(self):
        """Crea un nuevo modelo ingresando su nombre, marca y prenda."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Crear Nuevo Modelo")
        ventana.geometry("400x250")

        tk.Label(ventana, text="Prenda:").pack(pady=5)
        entry_prenda = tk.Entry(ventana)
        entry_prenda.pack(pady=5)

        tk.Label(ventana, text="Marca:").pack(pady=5)
        entry_marca = tk.Entry(ventana)
        entry_marca.pack(pady=5)

        tk.Label(ventana, text="Nombre del Modelo:").pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack(pady=5)

        def guardar_modelo():
            prenda = entry_prenda.get().strip()
            marca = entry_marca.get().strip()
            nombre = entry_nombre.get().strip()
            if not prenda or not marca or not nombre:
                messagebox.showerror("Error", "Complete todos los campos.")
                return

            modelo = Modelo(nombre, prenda, marca)
            self.modelos.append(modelo)
            self.tree_modelos.insert("", tk.END, values=(nombre, prenda, marca))
            messagebox.showinfo("Éxito", f"Modelo '{nombre}' creado correctamente.")
            ventana.destroy()

        btn_guardar = tk.Button(ventana, text="Guardar", command=guardar_modelo)
        btn_guardar.pack(pady=10)

    def seleccionar_modelo(self, event):
        """Selecciona un modelo de la tabla y muestra sus tallas."""
        item = self.tree_modelos.selection()
        if not item:
            return
        nombre_modelo = self.tree_modelos.item(item)["values"][0]
        for modelo in self.modelos:
            if modelo.nombre == nombre_modelo:
                self.modelo_seleccionado = modelo
                break
        self.mostrar_tallas()

    def mostrar_tallas(self):
        """Muestra las tallas del modelo seleccionado."""
        if not self.modelo_seleccionado:
            return

        for item in self.tree_tallas.get_children():
            self.tree_tallas.delete(item)

        tallas = self.modelo_seleccionado.tallas.obtener_tallas()
        for talla in tallas:
            self.tree_tallas.insert("", tk.END, values=talla)

    def agregar_talla(self):
        """Agrega una nueva talla al modelo seleccionado."""
        if not self.modelo_seleccionado:
            messagebox.showerror("Error", "Seleccione un modelo primero.")
            return

        talla = self.entry_talla.get().strip()
        try:
            stock = int(self.entry_stock.get().strip())
            precio = float(self.entry_precio.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Stock y Precio deben ser valores numéricos.")
            return

        if talla == "" or stock < 0 or precio < 0:
            messagebox.showerror("Error", "Ingrese datos válidos.")
            return

        self.modelo_seleccionado.tallas.agregar_talla(talla, stock, precio)
        self.mostrar_tallas()

        self.entry_talla.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)

# Programa principal
if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
