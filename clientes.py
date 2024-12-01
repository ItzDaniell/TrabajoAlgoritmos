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
