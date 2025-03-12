from database.connection import MySQLConnection, test_connection

def test_crud_operations():
    """Prueba operaciones básicas CRUD"""
    try:
        db = MySQLConnection()
        
        # Test de inserción
        db.begin_transaction()
        try:
            db.execute_query("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50)
                )
            """)
            
            db.execute_query(
                "INSERT INTO test_table (name) VALUES (%s)",
                ("Test Item",)
            )
            db.commit()
            print("✓ Inserción exitosa")
            
            # Test de lectura
            result = db.fetch_one("SELECT * FROM test_table WHERE name = %s", ("Test Item",))
            if result and result['name'] == "Test Item":
                print("✓ Lectura exitosa")
            
            # Test de actualización
            db.execute_query(
                "UPDATE test_table SET name = %s WHERE name = %s",
                ("Updated Item", "Test Item")
            )
            db.commit()
            print("✓ Actualización exitosa")
            
            # Test de eliminación
            db.execute_query("DROP TABLE test_table")
            print("✓ Eliminación exitosa")
            
        except Exception as e:
            db.rollback()
            raise e
            
    except Exception as e:
        print(f"✗ Error en pruebas CRUD: {str(e)}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    print("Probando conexión a la base de datos...")
    if test_connection():
        print("\nProbando operaciones CRUD...")
        test_crud_operations() 