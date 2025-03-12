from database.connection import MySQLConnection

def print_table_info(table_name: str, db: MySQLConnection):
    """Imprime la información detallada de una tabla"""
    print(f"\n{'='*50}")
    print(f"Tabla: {table_name}")
    print(f"{'='*50}")
    
    # Obtener y mostrar la estructura de la tabla
    print("\nEstructura de la tabla:")
    print("-" * 100)
    print(f"{'Columna':<20} {'Tipo':<20} {'Nulo':<10} {'Llave':<10} {'Default':<20} {'Extra':<20}")
    print("-" * 100)
    
    columns = db.get_table_schema(table_name)
    for column in columns:
        print(
            f"{column['column_name']:<20} "
            f"{column['data_type']:<20} "
            f"{column['is_nullable']:<10} "
            f"{column['key_type'] or '-':<10} "
            f"{str(column['default_value'] or '-'):<20} "
            f"{column['extra'] or '-':<20}"
        )
    
    # Obtener y mostrar las relaciones
    relationships = db.get_table_relationships(table_name)
    if relationships:
        print("\nRelaciones:")
        print("-" * 80)
        print(f"{'Constraint':<20} {'Columna Local':<20} {'Tabla Referenciada':<20} {'Columna Referenciada':<20}")
        print("-" * 80)
        for rel in relationships:
            print(
                f"{rel['constraint_name']:<20} "
                f"{rel['column_name']:<20} "
                f"{rel['referenced_table']:<20} "
                f"{rel['referenced_column']:<20}"
            )

def main():
    try:
        db = MySQLConnection()
        tables = db.get_all_tables()
        
        print("\nTablas encontradas en la base de datos:")
        for table in tables:
            print_table_info(table, db)
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    main() 