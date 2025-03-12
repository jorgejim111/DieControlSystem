from database.connection import MySQLConnection

def main():
    try:
        db = MySQLConnection()
        auth_tables = ['users', 'roles_user', 'rols']
        
        for table in auth_tables:
            print(f"\n=== Tabla: {table} ===")
            # Obtener estructura
            columns = db.fetch_all(f"SHOW COLUMNS FROM {table}")
            print("\nColumnas:")
            for col in columns:
                print(f"- {col['Field']} ({col['Type']})")
            
            # Obtener llaves foráneas
            fk_query = """
                SELECT 
                    COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = DATABASE()
                    AND TABLE_NAME = %s
                    AND REFERENCED_TABLE_NAME IS NOT NULL
            """
            foreign_keys = db.fetch_all(fk_query, (table,))
            
            if foreign_keys:
                print("\nRelaciones:")
                for fk in foreign_keys:
                    print(f"- {fk['COLUMN_NAME']} -> {fk['REFERENCED_TABLE_NAME']}.{fk['REFERENCED_COLUMN_NAME']}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    main() 