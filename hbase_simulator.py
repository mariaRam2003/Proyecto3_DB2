import json
import os
import time

class HBaseSimulator:
    def __init__(self):
        self.tables = {}
        self.load_metadata()
    
    def load_metadata(self):
        # Cargar metadatos desde archivos JSON
        data_dir = "data"
        for file_name in os.listdir(data_dir):
            if file_name.startswith("metadata_"):
                table_name = file_name.split("_")[1].split(".")[0]
                with open(os.path.join(data_dir, file_name), 'r') as f:
                    metadata = json.load(f)
                    self.tables[table_name] = {
                        "is_enabled": metadata["is_enabled"],
                        "column_families": metadata["column_families"],
                        "data": {}
                    }
    
    def save_metadata(self):
        # Guardar metadatos en archivos JSON
        data_dir = "data"
        for table_name, table_info in self.tables.items():
            metadata = {
                "table_name": table_name,
                "is_enabled": table_info["is_enabled"],
                "column_families": table_info["column_families"]
            }
            file_name = f"metadata_{table_name}.json"
            with open(os.path.join(data_dir, file_name), 'w') as f:
                json.dump(metadata, f, indent=4)
    
    def save_data(self, table_name):
        # Guardar datos en archivos HFile
        table_info = self.tables[table_name]
        data_dir = "data"
        for cf_name in table_info["column_families"].keys():
            file_name = f"{table_name}_{cf_name}.hfile"
            cf_data = [
                {"row_key": row_key, "columns": columns}
                for row_key, row_data in table_info["data"].items()
                for cf, columns in row_data.items() if cf == cf_name
            ]
            with open(os.path.join(data_dir, file_name), 'w') as f:
                json.dump(cf_data, f, indent=4)
    
    def create(self, table_name, column_families):
        self.tables[table_name] = {
            "is_enabled": True,
            "column_families": column_families,
            "data": {}
        }
        self.save_metadata()
    
    def list_tables(self):
        return list(self.tables.keys())
    
    def disable(self, table_name):
        self.tables[table_name]["is_enabled"] = False
        self.save_metadata()
    
    def enable(self, table_name):
        self.tables[table_name]["is_enabled"] = True
        self.save_metadata()
    
    def is_enabled(self, table_name):
        return self.tables[table_name]["is_enabled"]
    
    def alter(self, table_name, column_families):
        self.tables[table_name]["column_families"] = column_families
        self.save_metadata()
    
    def drop(self, table_name):
        if self.is_enabled(table_name):
            raise ValueError(f"Table {table_name} is enabled. Disable the table before dropping it.")
        del self.tables[table_name]
        data_dir = "data"
        for file_name in os.listdir(data_dir):
            if file_name.startswith(table_name):
                os.remove(os.path.join(data_dir, file_name))
        metadata_file = f"metadata_{table_name}.json"
        os.remove(os.path.join(data_dir, metadata_file))
    
    def drop_all(self):
        for table_name in list(self.tables.keys()):
            if self.is_enabled(table_name):
                raise ValueError(f"Table {table_name} is enabled. Disable all tables before dropping them.")
            self.drop(table_name)
    
    def describe(self, table_name):
        table_info = self.tables.get(table_name)
        if table_info:
            return {
                "is_enabled": table_info["is_enabled"],
                "column_families": table_info["column_families"]
            }
        return None
    
    def put(self, table_name, row_key, column, value):
        if not self.is_enabled(table_name):
            raise ValueError(f"Table {table_name} is disabled.")
        cf, col = column.split(":")
        timestamp = int(time.time())
        if row_key not in self.tables[table_name]["data"]:
            self.tables[table_name]["data"][row_key] = {}
        if cf not in self.tables[table_name]["data"][row_key]:
            self.tables[table_name]["data"][row_key][cf] = {}
        self.tables[table_name]["data"][row_key][cf][col] = {"timestamp": timestamp, "value": value}
        self.save_data(table_name)
    
    def get(self, table_name, row_key):
        if row_key in self.tables[table_name]["data"]:
            return self.tables[table_name]["data"][row_key]
        return None
    
    def scan(self, table_name, start_row, end_row):
        scanned_data = {}
        for row_key in sorted(self.tables[table_name]["data"].keys()):
            if start_row <= row_key <= end_row:
                row_data = self.tables[table_name]["data"][row_key]
                row_metadata = {"timestamp": int(time.time())}
                scanned_data[row_key] = {"metadata": row_metadata, "columns": row_data}
        return scanned_data

    
    def delete(self, table_name, row_key, column):
        cf, col = column.split(":")
        if row_key in self.tables[table_name]["data"]:
            if cf in self.tables[table_name]["data"][row_key]:
                if col in self.tables[table_name]["data"][row_key][cf]:
                    del self.tables[table_name]["data"][row_key][cf][col]
                    if not self.tables[table_name]["data"][row_key][cf]:
                        del self.tables[table_name]["data"][row_key][cf]
                    if not self.tables[table_name]["data"][row_key]:
                        del self.tables[table_name]["data"][row_key]
                    self.save_data(table_name)
    
    def delete_all(self, table_name):
        self.tables[table_name]["data"].clear()
        self.save_data(table_name)
    
    def count(self, table_name):
        return len(self.tables[table_name]["data"])
    
    def truncate(self, table_name):
        print(f"Comenzando a truncar la tabla '{table_name}'...")
        
        print("Deshabilitando la tabla...")
        self.disable(table_name)
        print(f"Tabla '{table_name}' deshabilitada.")
        
        column_families = self.tables[table_name]["column_families"]
        print("Guardando información de las familias de columnas...")
        
        print("Eliminando la tabla...")
        self.drop(table_name)
        print(f"Tabla '{table_name}' eliminada.")
        
        print("Recreando la tabla...")
        self.create(table_name, column_families)
        print(f"Tabla '{table_name}' recreada.")
        
        print(f"Proceso de truncado de la tabla '{table_name}' completado.")
