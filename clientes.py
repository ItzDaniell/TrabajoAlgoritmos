import tkinter as tk
from tkinter import ttk, messagebox

class Cliente:
    def __init__(self, nombre, apellido, correo, telefono, direccion, dni, id=None):
        self.id = id
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Apellido: {self.apellido}, DNI: {self.dni}, Correo: {self.correo}, Teléfono: {self.telefono}, Dirección: {self.direccion}"

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

# Función para agregar un nodo al final de la lista
def agregar_al_final(nodo_inicial, dato):
    nuevo_nodo = Nodo(dato)
    if nodo_inicial is None:
        nodo_inicial = nuevo_nodo
        return nodo_inicial
    temporal = nodo_inicial
    while temporal.siguiente:
        temporal = temporal.siguiente
    temporal.siguiente = nuevo_nodo
    return nodo_inicial

# Función para agregar un nodo al inicio de la lista
def agregar_al_inicio(nodo_inicial, dato):
    nuevo_nodo = Nodo(dato)
    nuevo_nodo.siguiente = nodo_inicial
    return nuevo_nodo

# Función para imprimir la lista enlazada
def imprimir_lista(nodo):
    while nodo is not None:
        print(f"Cliente: {nodo.dato}")
        nodo = nodo.siguiente

# Función para verificar si un cliente existe en la lista
def existe(nodo, busqueda):
    while nodo is not None:
        if nodo.dato.dni == busqueda:
            return True
        nodo = nodo.siguiente
    return False

# Función para eliminar un cliente por su DNI
def eliminar(nodo, cliente_dni):
    if nodo is None:
        return None
    if nodo.dato.dni == cliente_dni:
        return nodo.siguiente
    temporal = nodo
    while temporal.siguiente is not None:
        if temporal.siguiente.dato.dni == cliente_dni:
            if temporal.siguiente.siguiente is not None:
                temporal.siguiente = temporal.siguiente.siguiente
            else:
                temporal.siguiente = None
            return nodo
        temporal = temporal.siguiente
    return nodo

# Función para buscar un cliente por su DNI
def buscar(nodo, cliente_dni):
    while nodo is not None:
        if nodo.dato.dni == cliente_dni:
            return nodo.dato
        nodo = nodo.siguiente
    return None

# Función para contar los elementos de la lista
def contar_elementos(nodo_inicial):
    count = 0
    while nodo_inicial:
        count += 1
        nodo_inicial = nodo_inicial.siguiente
    return count

class ClienteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Clientes")
        self.root.geometry("760x650")  # Ajustar el tamaño inicial de la ventana
        
        self.lista_clientes = None  # Lista enlazada inicial
        self.crear_interfaz()

    def crear_interfaz(self):
        # Campo para agregar cliente
        frame_agregar = tk.LabelFrame(self.root, text="Ingreso de Clientes", padx=10, pady=10)
        frame_agregar.pack(pady=10, padx=10, fill="x")

        ancho_entrada = 25  # Ancho estándar para todas las entradas

        tk.Label(frame_agregar, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombre = tk.Entry(frame_agregar, width=ancho_entrada)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_agregar, text="Apellido:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_apellido = tk.Entry(frame_agregar, width=ancho_entrada)
        self.entry_apellido.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_agregar, text="Correo:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.entry_correo = tk.Entry(frame_agregar, width=ancho_entrada)
        self.entry_correo.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(frame_agregar, text="Teléfono:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_telefono = tk.Entry(frame_agregar, width=ancho_entrada)
        self.entry_telefono.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_agregar, text="Dirección:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_direccion = tk.Entry(frame_agregar, width=ancho_entrada)
        self.entry_direccion.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(frame_agregar, text="DNI:").grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.entry_dni = tk.Entry(frame_agregar, width=ancho_entrada)
        self.entry_dni.grid(row=1, column=5, padx=5, pady=5)

        tk.Button(frame_agregar, text="Agregar Cliente", command=self.agregar_cliente).grid(row=2, column=0, columnspan=6, pady=10)

        # Campo de búsqueda
        frame_buscar = tk.LabelFrame(self.root, text="Buscar Cliente", padx=10, pady=10)
        frame_buscar.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_buscar, text="Buscar por DNI:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_buscar = tk.Entry(frame_buscar, width=ancho_entrada)
        self.entry_buscar.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame_buscar, text="Buscar", command=self.buscar_cliente).grid(row=0, column=2, padx=5, pady=5)

        # Tabla de clientes
        frame_tabla = tk.Frame(self.root)
        frame_tabla.pack(pady=10, padx=10, fill="both", expand=True)

        columnas = ("Nombre", "Apellido", "Correo", "Teléfono", "Dirección", "DNI")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        self.tabla.pack(side="left", fill="both", expand=True)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, minwidth=100, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar.set)

        # Botón para eliminar cliente
        tk.Button(self.root, text="Eliminar Cliente", command=self.eliminar_cliente).pack(pady=10)

    def agregar_cliente(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        correo = self.entry_correo.get()
        telefono = self.entry_telefono.get()
        direccion = self.entry_direccion.get()
        dni = self.entry_dni.get()

        if not (nombre and apellido and correo and telefono and direccion and dni):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        if existe(self.lista_clientes, dni):
            messagebox.showerror("Error", "El cliente con este DNI ya existe.")
            return

        nuevo_cliente = Cliente(nombre, apellido, correo, telefono, direccion, dni)
        self.lista_clientes = agregar_al_final(self.lista_clientes, nuevo_cliente)

        self.actualizar_tabla()
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Cliente agregado correctamente.")

    def eliminar_cliente(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar.")
            return

        cliente_dni = self.tabla.item(seleccionado[0], "values")[5]  # Obtiene el DNI de la fila seleccionada
        self.lista_clientes = eliminar(self.lista_clientes, cliente_dni)

        self.actualizar_tabla()
        messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")


    def buscar_cliente(self):
        dni = self.entry_buscar.get()

        # Limpiar la tabla antes de mostrar los resultados de la búsqueda
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        if not dni:  # Si el campo de búsqueda está vacío, muestra todos los clientes
            nodo_actual = self.lista_clientes
            while nodo_actual:
                cliente = nodo_actual.dato
                self.tabla.insert("", "end", values=(cliente.nombre, cliente.apellido, cliente.correo, cliente.telefono, cliente.direccion, cliente.dni))
                nodo_actual = nodo_actual.siguiente
        else:
            # Buscar y mostrar solo los clientes que coincidan con el DNI
            nodo_actual = self.lista_clientes
            while nodo_actual:
                cliente = nodo_actual.dato
                if cliente.dni == dni:
                    self.tabla.insert("", "end", values=(cliente.nombre, cliente.apellido, cliente.correo, cliente.telefono, cliente.direccion, cliente.dni))
                nodo_actual = nodo_actual.siguiente

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        nodo_actual = self.lista_clientes
        while nodo_actual:
            cliente = nodo_actual.dato
            self.tabla.insert("", "end", values=(cliente.nombre, cliente.apellido, cliente.correo, cliente.telefono, cliente.direccion, cliente.dni))
            nodo_actual = nodo_actual.siguiente

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.entry_dni.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteApp(root)
    root.mainloop()
