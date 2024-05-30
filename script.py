import os
import json

data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

metadata_files = {
    "metadata_Empleados.json": {
        "table_name": "Empleados",
        "is_enabled": True,
        "column_families": {
            "Info": ["Nombre", "Apellido"],
            "Contacto": ["Teléfono"],
            "Trabajo": ["Departamento", "Posición"]
        }
    },
    "metadata_Departamentos.json": {
        "table_name": "Departamentos",
        "is_enabled": True,
        "column_families": {
            "Detalles": ["NombreDepto"],
            "Personal": ["Empleado"]
        }
    },
    "metadata_Proyectos.json": {
        "table_name": "Proyectos",
        "is_enabled": True,
        "column_families": {
            "Info": ["NombreProyecto"],
            "Tiempo": ["Inicio", "Fin"]
        }
    }
}

data_files = {
    "Empleados_Info.hfile": [
        {"row_key": "1", "columns": {"Nombre": {1591649830: "Juan"}, "Apellido": { 1591649830: "Pérez"}}},
        {"row_key": "2", "columns": {"Nombre": {1591649830: "Ana"}, "Apellido": {1591649830: "García"}}}
    ],
    "Empleados_Contacto.hfile": [
        {"row_key": "1", "columns": {"Teléfono": {1591649830 : "555-1234"}}},
        {"row_key": "2", "columns": {"Teléfono": {1591649830 : "555-5678"}}}
    ],
    "Empleados_Trabajo.hfile": [
        {"row_key": "1", "columns": {"Departamento": {1591649830 : "TI"}, "Posición": { 1591649830 : "Desarrollador"}}},
        {"row_key": "2", "columns": {"Departamento": {1591649830 : "HR"}, "Posición": { 1591649830 : "Manager"}}}
    ],
    "Departamentos_Detalles.hfile": [
        {"row_key": "1", "columns": {"NombreDepto": {1591649830: "TI"}}},
        {"row_key": "2", "columns": {"NombreDepto": {1591649830: "HR"}}}
    ],
    "Departamentos_Personal.hfile": [
        {"row_key": "1", "columns": {"Empleado": { 1591649830: "Juan"}}},
        {"row_key": "2", "columns": {"Empleado": { 1591649830: "Ana"}}}
    ],
    "Proyectos_Info.hfile": [
        {"row_key": "1", "columns": {"NombreProyecto": {1591649830: "Proyecto A"}}},
        {"row_key": "2", "columns": {"NombreProyecto": {1591649830: "Proyecto B"}}}
    ],
    "Proyectos_Tiempo.hfile": [
        {"row_key": "1", "columns": {"Inicio": { 1591649830: "2024-01-01"}, "Fin": {1591649830 : "2024-06-01"}}},
        {"row_key": "2", "columns": {"Inicio": { 1591649830: "2024-02-01"}, "Fin": {1591649830 : "2024-07-01"}}}
    ]
}

# Guardar metadatos
for filename, content in metadata_files.items():
    with open(os.path.join(data_dir, filename), 'w') as f:
        json.dump(content, f, indent=4)

# Guardar datos
for filename, content in data_files.items():
    with open(os.path.join(data_dir, filename), 'w') as f:
        json.dump(content, f, indent=4)
