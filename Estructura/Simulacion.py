import os
import json

# Funcionalidades
## Funciones DDL (Data Definition Language)

### Crear Tabla
def crear_tabla(nombre_tabla, familias_columnas, configuraciones):
    """
    Crea una nueva tabla con las familias de columnas especificadas y las configuraciones dadas.

    Args:
    nombre_tabla (str): El nombre de la tabla a crear.
    familias_columnas (list): Lista de nombres de las familias de columnas.
    configuraciones (dict): Diccionario con configuraciones específicas de la tabla (por ejemplo, max_versions).
    """
    if nombre_tabla not in metadatos["tablas"]:
        # Actualizar los metadatos para incluir la nueva tabla
        metadatos["tablas"][nombre_tabla] = {
            "familias_columnas": familias_columnas,
            "configuraciones": configuraciones
        }
        # Crear archivos vacíos para cada familia de columnas
        for familia in familias_columnas:
            with open(f"{nombre_tabla}_{familia}.hfile.json", "w") as f:
                f.write("{}")
    else:
        print(f"Tabla {nombre_tabla} ya existe.")

### Eliminar Tabla
def eliminar_tabla(nombre_tabla):
    """
    Elimina una tabla existente junto con sus archivos de datos.

    Args:
    nombre_tabla (str): El nombre de la tabla a eliminar.
    """
    if nombre_tabla in metadatos["tablas"]:
        # Eliminar archivos de datos correspondientes a la tabla
        for familia in metadatos["tablas"][nombre_tabla]["familias_columnas"]:
            os.remove(f"{nombre_tabla}_{familia}.hfile.json")
        # Eliminar la entrada en los metadatos
        del metadatos["tablas"][nombre_tabla]
    else:
        print(f"Tabla {nombre_tabla} no existe.")

## Funciones DML (Data Manipulation Language)

### Insertar Datos
def insertar_dato(nombre_tabla, row_key, familia_columna, columna, valor, timestamp):
    """
    Inserta un dato en una tabla específica.

    Args:
    nombre_tabla (str): El nombre de la tabla.
    row_key (str): La clave de la fila donde se insertará el dato.
    familia_columna (str): El nombre de la familia de columnas.
    columna (str): El nombre de la columna.
    valor (any): El valor a insertar.
    timestamp (int): El timestamp asociado con el valor.
    """
    archivo = f"{nombre_tabla}_{familia_columna}.hfile.json"
    if not os.path.exists(archivo):
        print(f"Archivo {archivo} no encontrado.")
        return

    # Cargar los datos del archivo correspondiente
    with open(archivo, "r") as f:
        datos = json.load(f)

    # Inicializar la estructura de datos si es necesario
    if row_key not in datos:
        datos[row_key] = {}
    if columna not in datos[row_key]:
        datos[row_key][columna] = []

    # Añadir el nuevo dato con su timestamp
    datos[row_key][columna].append({"timestamp": timestamp, "valor": valor})
    # Ordenar los datos por timestamp en orden descendente
    datos[row_key][columna] = sorted(datos[row_key][columna], key=lambda x: x["timestamp"], reverse=True)

    # Guardar los datos actualizados en el archivo
    with open(archivo, "w") as f:
        json.dump(datos, f, indent=4)

### Consultar Datos
def consultar_dato(nombre_tabla, row_key, familia_columna, columna):
    """
    Consulta un dato específico de una tabla.

    Args:
    nombre_tabla (str): El nombre de la tabla.
    row_key (str): La clave de la fila a consultar.
    familia_columna (str): El nombre de la familia de columnas.
    columna (str): El nombre de la columna.

    Returns:
    list: Una lista de versiones del dato, cada una con su timestamp y valor, o None si no se encuentra el dato.
    """
    archivo = f"{nombre_tabla}_{familia_columna}.hfile.json"
    if not os.path.exists(archivo):
        print(f"Archivo {archivo} no encontrado.")
        return None

    # Cargar los datos del archivo correspondiente
    with open(archivo, "r") as f:
        datos = json.load(f)

    # Devolver los datos solicitados si existen
    if row_key in datos and columna in datos[row_key]:
        return datos[row_key][columna]
    else:
        print(f"Datos no encontrados para row_key: {row_key}, columna: {columna}")
        return None

### Eliminar Dato
def eliminar_dato(nombre_tabla, row_key, familia_columna, columna):
    """
    Elimina un dato específico de una tabla.

    Args:
    nombre_tabla (str): El nombre de la tabla.
    row_key (str): La clave de la fila donde se eliminará el dato.
    familia_columna (str): El nombre de la familia de columnas.
    columna (str): El nombre de la columna.
    """
    archivo = f"{nombre_tabla}_{familia_columna}.hfile.json"
    if not os.path.exists(archivo):
        print(f"Archivo {archivo} no encontrado.")
        return

    # Cargar los datos del archivo correspondiente
    with open(archivo, "r") as f:
        datos = json.load(f)

    # Eliminar el dato si existe
    if row_key in datos and columna in datos[row_key]:
        del datos[row_key][columna]

        # Guardar los datos actualizados en el archivo
        with open(archivo, "w") as f:
            json.dump(datos, f, indent=4)
    else:
        print(f"Datos no encontrados para row_key: {row_key}, columna: {columna}")

# Definir metadatos iniciales
metadatos = {
    "tablas": {
        "usuarios": {
            "familias_columnas": ["info_personal", "actividad"],
            "configuraciones": {"max_versions": 3}
        }
    }
}

# Crear tabla y cargar datos
crear_tabla("usuarios", ["info_personal", "actividad"], {"max_versions": 3})
insertar_dato("usuarios", "user1", "info_personal", "nombre", "Juan", 1622547800)
insertar_dato("usuarios", "user1", "info_personal", "edad", 30, 1622547900)
insertar_dato("usuarios", "user1", "actividad", "ultima_visita", "2024-05-14", 1622548000)
