from database.connection import MySQLConnection

def check_tables():
    db = MySQLConnection()
    try:
        # Mostrar todas las bases de datos
        databases = db.fetch_all("SHOW DATABASES")
        print("\nBases de datos disponibles:")
        for database in databases:
            print(f"- {database['Database']}")

        # Mostrar todas las tablas en la base de datos actual
        print(f"\nTablas en la base de datos '{db.database}':")
        tables = db.fetch_all("SHOW TABLES")
        for table in tables:
            table_name = table[f"Tables_in_{db.database}"]
            print(f"- {table_name}")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    check_tables() 