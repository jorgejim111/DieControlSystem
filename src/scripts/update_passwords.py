from database.connection import MySQLConnection
from database.database_schema import Tables, Columns
import bcrypt

def update_passwords():
    """Actualiza las contraseñas existentes al formato correcto de bcrypt"""
    db = MySQLConnection()
    
    # Obtener todos los usuarios
    query = f"""
        SELECT {Columns.Users.ID}, {Columns.Users.USERNAME}, {Columns.Users.PASSWORD}
        FROM {Tables.USER}
    """
    users = db.execute_query(query)
    
    print(f"Encontrados {len(users)} usuarios")
    
    # Contraseña por defecto para actualizar
    default_password = "admin123"
    hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
    
    # Actualizar cada usuario
    for user in users:
        try:
            # Verificar si la contraseña actual es válida
            current_password = user[Columns.Users.PASSWORD]
            if current_password and isinstance(current_password, str):
                try:
                    # Intentar verificar si es un hash bcrypt válido
                    bcrypt.checkpw(default_password.encode('utf-8'), current_password.encode('utf-8'))
                    print(f"Usuario {user[Columns.Users.USERNAME]} ya tiene un hash bcrypt válido")
                    continue
                except ValueError:
                    # Si no es válido, actualizar
                    update_query = f"""
                        UPDATE {Tables.USER}
                        SET {Columns.Users.PASSWORD} = %s
                        WHERE {Columns.Users.ID} = %s
                    """
                    db.execute_query(update_query, (hashed_password.decode('utf-8'), user[Columns.Users.ID]))
                    print(f"Contraseña actualizada para usuario {user[Columns.Users.USERNAME]}")
        except Exception as e:
            print(f"Error actualizando usuario {user[Columns.Users.USERNAME]}: {str(e)}")

if __name__ == "__main__":
    update_passwords() 