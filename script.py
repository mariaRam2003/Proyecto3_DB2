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
        {"row_key": "1", "columns": {"Nombre": {"timestamp": 1591649830, "value": "Juan"}, "Apellido": {"timestamp": 1591649830, "value": "Pérez"}}},
        {"row_key": "2", "columns": {"Nombre": {"timestamp": 1591649830, "value": "Ana"}, "Apellido": {"timestamp": 1591649830, "value": "García"}}}
    ],
    "Empleados_Contacto.hfile": [
        {"row_key": "1", "columns": {"Teléfono": {"timestamp": 1591649830, "value": "555-1234"}}},
        {"row_key": "2", "columns": {"Teléfono": {"timestamp": 1591649830, "value": "555-5678"}}}
    ],
    "Empleados_Trabajo.hfile": [
        {"row_key": "1", "columns": {"Departamento": {"timestamp": 1591649830, "value": "TI"}, "Posición": {"timestamp": 1591649830, "value": "Desarrollador"}}},
        {"row_key": "2", "columns": {"Departamento": {"timestamp": 1591649830, "value": "HR"}, "Posición": {"timestamp": 1591649830, "value": "Manager"}}}
    ],
    "Departamentos_Detalles.hfile": [
        {"row_key": "1", "columns": {"NombreDepto": {"timestamp": 1591649830, "value": "TI"}}},
        {"row_key": "2", "columns": {"NombreDepto": {"timestamp": 1591649830, "value": "HR"}}}
    ],
    "Departamentos_Personal.hfile": [
        {"row_key": "1", "columns": {"Empleado": {"timestamp": 1591649830, "value": "Juan"}}},
        {"row_key": "2", "columns": {"Empleado": {"timestamp": 1591649830, "value": "Ana"}}}
    ],
    "Proyectos_Info.hfile": [
        {"row_key": "1", "columns": {"NombreProyecto": {"timestamp": 1591649830, "value": "Proyecto A"}}},
        {"row_key": "2", "columns": {"NombreProyecto": {"timestamp": 1591649830, "value": "Proyecto B"}}}
    ],
    "Proyectos_Tiempo.hfile": [
        {"row_key": "1", "columns": {"Inicio": {"timestamp": 1591649830, "value": "2024-01-01"}, "Fin": {"timestamp": 1591649830, "value": "2024-06-01"}}},
        {"row_key": "2", "columns": {"Inicio": {"timestamp": 1591649830, "value": "2024-02-01"}, "Fin": {"timestamp": 1591649830, "value": "2024-07-01"}}}
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
