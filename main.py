"""
Universidad del Valle de Guatemala
Proyecto 3 - Bases de datos Columnares
Curso Base de datos 2

Autores:
- Maria Marta Ramirez
- Gustavo Gonzalez
- Diego Leiva
- Jose Pablo Orellana
- Gabriel Garcia
"""

import json
import time
import os
from hbase_simulator import HBaseSimulator

def load_initial_dataset(hbs):
    # Habilitar las tablas si están deshabilitadas
    for table_name in ["Empleados", "Departamentos", "Proyectos"]:
        if table_name in hbs.tables and not hbs.is_enabled(table_name):
            hbs.enable(table_name)
    
    # # Insertar datos en la tabla Empleados
    hbs.put("Empleados", "1", "Info:Nombre", "Juan")
    hbs.put("Empleados", "1", "Info:Apellido", "Pérez")
    hbs.put("Empleados", "1", "Contacto:Teléfono", "555-1234")
    hbs.put("Empleados", "1", "Trabajo:Departamento", "TI")
    hbs.put("Empleados", "1", "Trabajo:Posición", "Desarrollador")
    hbs.put("Empleados", "2", "Info:Nombre", "Ana")
    hbs.put("Empleados", "2", "Info:Apellido", "García")
    hbs.put("Empleados", "2", "Contacto:Teléfono", "555-5678")
    hbs.put("Empleados", "2", "Trabajo:Departamento", "HR")
    hbs.put("Empleados", "2", "Trabajo:Posición", "Manager")
    
    # Insertar datos en la tabla Departamentos
    hbs.put("Departamentos", "1", "Detalles:NombreDepto", "TI")
    hbs.put("Departamentos", "1", "Personal:Empleado", "Juan")
    hbs.put("Departamentos", "2", "Detalles:NombreDepto", "HR")
    hbs.put("Departamentos", "2", "Personal:Empleado", "Ana")
    
    # Insertar datos en la tabla Proyectos
    hbs.put("Proyectos", "1", "Info:NombreProyecto", "Proyecto A")
    hbs.put("Proyectos", "1", "Tiempo:Inicio", "2024-01-01")
    hbs.put("Proyectos", "1", "Tiempo:Fin", "2024-06-01")
    hbs.put("Proyectos", "2", "Info:NombreProyecto", "Proyecto B")
    hbs.put("Proyectos", "2", "Tiempo:Inicio", "2024-02-01")
    hbs.put("Proyectos", "2", "Tiempo:Fin", "2024-07-01")

def print_menu():
    print("\n--- Menú de HBase Simulator ---")
    print("1. Crear Tabla (Create)")
    print("2. Listar Tablas (List)")
    print("3. Deshabilitar Tabla (Disable)")
    print("4. Habilitar Tabla (Enable)")
    print("5. Verificar si una Tabla está Habilitada (Is_enabled)")
    print("6. Modificar Tabla (Alter)")
    print("7. Eliminar Tabla (Drop)")
    print("8. Eliminar Todas las Tablas (Drop All)")
    print("9. Describir Tabla (Describe)")
    print("10. Insertar/Actualizar Datos (Put)")
    print("11. Obtener Datos (Get)")
    print("12. Escanear Datos (Scan)")
    print("13. Eliminar Columna de una Fila (Delete)")
    print("14. Eliminar Todos los Datos de una Tabla (Delete All)")
    print("15. Contar Filas en una Tabla (Count)")
    print("16. Truncar Tabla (Truncate)")
    print("17. Salir")
    print("----------------------------")

def main():
    hbs = HBaseSimulator()
    load_initial_dataset(hbs)
    
    while True:
        try:
            print_menu()
            choice = input("Seleccione una opción: ")

            if choice == '1':
                table_name = input("Nombre de la tabla: ").strip()
                if not table_name:
                    print("Error: El nombre de la tabla no puede estar vacío. No se puede crear una tabla sin nombre.")
                    continue
                if table_name in hbs.tables:
                    print(f"Error: La tabla '{table_name}' ya existe.")
                    continue
                column_families = input("Familias de columnas (separadas por coma): ").strip().split(",")
                if not column_families or all(cf.strip() == '' for cf in column_families):
                    print("Error: Debe proporcionar al menos una familia de columnas.")
                    continue
                cf_dict = {cf.strip(): {} for cf in column_families if cf.strip()}
                hbs.create(table_name, cf_dict)
                print(f"Tabla '{table_name}' creada.")
            
            elif choice == '2':
                tables = hbs.list_tables()
                if tables:
                    print("Tablas disponibles:")
                    for table in tables:
                        print(f"- {table}")
                else:
                    print("No hay tablas disponibles.")
            
            elif choice == '3':
                table_name = input("Nombre de la tabla a deshabilitar: ").strip()
                if not table_name:
                    print("Error: El nombre de la tabla no puede estar vacío.")
                    continue
                if table_name not in hbs.tables:
                    print(f"Error: La tabla '{table_name}' no existe.")
                    continue
                hbs.disable(table_name)
                print(f"Tabla '{table_name}' deshabilitada.")
            
            elif choice == '4':
                table_name = input("Nombre de la tabla a habilitar: ").strip()
                if not table_name:
                    print("Error: El nombre de la tabla no puede estar vacío.")
                    continue
                if table_name not in hbs.tables:
                    print(f"Error: La tabla '{table_name}' no existe.")
                    continue
                hbs.enable(table_name)
                print(f"Tabla '{table_name}' habilitada.")
            
            elif choice == '5':
                table_name = input("Nombre de la tabla: ").strip()
                if not table_name:
                    print("Error: El nombre de la tabla no puede estar vacío.")
                    continue
                if table_name not in hbs.tables:
                    print(f"Error: La tabla '{table_name}' no existe.")
                    continue
                status = hbs.is_enabled(table_name)
                print(f"La tabla '{table_name}' está {'habilitada' if status else 'deshabilitada'}.")
            
            elif choice == '6':
                table_name = input("Nombre de la tabla: ").strip()
                if not table_name:
                    print("Error: El nombre de la tabla no puede estar vacío.")
                    continue
                if table_name not in hbs.tables:
                    print(f"Error: La tabla '{table_name}' no existe.")
                    continue
                column_families = input("Nuevas familias de columnas (separadas por coma): ").strip().split(",")
                if not column_families or all(cf.strip() == '' for cf in column_families):
                    print("Error: Debe proporcionar al menos una familia de columnas.")
                    continue
                cf_dict = {cf.strip(): {} for cf in column_families if cf.strip()}
                hbs.alter(table_name, cf_dict)
                print(f"Tabla '{table_name}' modificada.")
            
            elif choice == '7':
                table_name = input("Nombre de la tabla a eliminar: ").strip()
                if not table_name:
                    print("Error: El nombre de la tabla no puede estar vacío.")
                    continue
                if table_name not in hbs.tables:
                    print(f"Error: La tabla '{table_name}' no existe.")
                    continue
                try:
                    hbs.drop(table_name)
                    print(f"Tabla '{table_name}' eliminada.")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '8':
                try:
                    hbs.drop_all()
                    print("Todas las tablas han sido eliminadas.")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '9':
                table_name = input("Nombre de la tabla: ").strip()
                if not table_name:
                    print("Error: El nombre de la tabla no puede estar vacío.")
                    continue
                if table_name not in hbs.tables:
                    print(f"Error: La tabla '{table_name}' no existe.")
                    continue
                description = hbs.describe(table_name)
                if description:
                    print(f"Descripción de la tabla '{table_name}':")
                    print(f"  Habilitada: {description['is_enabled']}")
                    print(f"  Familias de columnas: {', '.join(description['column_families'].keys())}")
                else:
                    print(f"No se encontró la tabla '{table_name}'.")
            
            elif choice == '10':
                table_name = input("Nombre de la tabla: ").strip()
                if not table_name:
                    print("Error: El nombre de la tabla no puede estar vacío.")
                    continue
                if table_name not in hbs.tables:
                    print(f"Error: La tabla '{table_name}' no existe.")
                    continue
                if not hbs.is_enabled(table_name):  # Añadimos la verificación de si la tabla está habilitada
                    print(f"Error: La tabla '{table_name}' está deshabilitada. No se pueden insertar o actualizar datos.")
                    continue
                row_key = input("Row Key: ").strip()
                if not row_key:
                    print("Error: El Row Key no puede estar vacío.")
                    continue
                column = input("Columna (familia:columna): ").strip()
                if ':' not in column:
                    print("Error: La columna debe estar en el formato 'familia:columna'.")
                    continue
                value = input("Valor: ").strip()
                hbs.put(table_name, row_key, column, value)
                print("Datos insertados/actualizados.")

            
            elif choice == '11':
                table_name = input("Nombre de la tabla: ").strip()
                if not table_name:
                    print("Error: El nombre de la tabla no puede estar vacío.")
                    continue
                if table_name not in hbs.tables:
                    print(f"Error: La tabla '{table_name}' no existe.")
                    continue
                row_key = input("Row Key: ").strip()
                if not row_key:
                    print("Error: El Row Key no puede estar vacío.")
                    continue
                column = input("Columna (familia:columna): ").strip()
                if not column or column == '':
                    data = hbs.get(table_name, row_key)
                    if data:
                        print(f"Datos de la fila '{row_key}' en la tabla '{table_name}':")
                        print(json.dumps(data, indent=4))
                    else:
                        print(f"No se encontró la fila '{row_key}' en la tabla '{table_name}'.")
                elif ':' not in column:
                    print("Error: La columna debe estar en el formato 'familia:columna'.")
                    continue
                else:
                    data = hbs.get(table_name, row_key, column)
                    if data:
                        print(f"Datos de la fila '{row_key}' en la tabla '{table_name}':")
                        print(json.dumps(data, indent=4))
                    else:
                        print(f"No se encontró la fila '{row_key}' en la tabla '{table_name}'.")
            
            elif choice == '12':
                table_name = input("Nombre de la tabla: ").strip()
                if not table_name:
                    print("Error: El nombre de la tabla no puede estar vacío.")
                    continue
                if table_name not in hbs.tables:
                    print(f"Error: La tabla '{table_name}' no existe.")
                    continue
                start_row = input("Row Key de inicio: ").strip()
                end_row = input("Row Key de fin: ").strip()
                data = hbs.scan(table_name, start_row, end_row)
                print(f"Datos escaneados en la tabla '{table_name}' entre '{start_row}' y '{end_row}':")
                print(json.dumps(data, indent=4))
            
            elif choice == '13':
                table_name = input("Nombre de la tabla: ").strip()
                if not table_name:
                    print("Error: El nombre de la tabla no puede estar vacío.")
                    continue
                if table_name not in hbs.tables:
                    print(f"Error: La tabla '{table_name}' no existe.")
                    continue
                row_key = input("Row Key: ").strip()
                if not row_key:
                    print("Error: El Row Key no puede estar vacío.")
                    continue
                column = input("Columna (familia:columna): ").strip()
                if ':' not in column:
                    print("Error: La columna debe estar en el formato 'familia:columna'.")
                    continue
                hbs.delete(table_name, row_key, column)
                print(f"Columna '{column}' de la fila '{row_key}' en la tabla '{table_name}' eliminada.")
            
            elif choice == '14':
                table_name = input("Nombre de la tabla: ").strip()
                if not table_name:
                    print("Error: El nombre de la tabla no puede estar vacío.")
                    continue
                if table_name not in hbs.tables:
                    print(f"Error: La tabla '{table_name}' no existe.")
                    continue
                hbs.delete_all(table_name)
                print(f"Todos los datos de la tabla '{table_name}' han sido eliminados.")
            
            elif choice == '15':
                table_name = input("Nombre de la tabla: ").strip()
                if not table_name:
                    print("Error: El nombre de la tabla no puede estar vacío.")
                    continue
                if table_name not in hbs.tables:
                    print(f"Error: La tabla '{table_name}' no existe.")
                    continue
                count = hbs.count(table_name)
                print(f"La tabla '{table_name}' tiene {count} filas.")
            
            elif choice == '16':
                table_name = input("Nombre de la tabla: ").strip()
                if not table_name:
                    print("Error: El nombre de la tabla no puede estar vacío.")
                    continue
                if table_name not in hbs.tables:
                    print(f"Error: La tabla '{table_name}' no existe.")
                    continue
                try:
                    hbs.truncate(table_name)
                    print(f"La tabla '{table_name}' ha sido truncada.")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '17':
                print("Saliendo...")
                break
            
            else:
                print("Opción no válida. Por favor, seleccione una opción del menú.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
