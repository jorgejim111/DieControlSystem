import sys
import os

# Agregar el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database.connection import MySQLConnection
from src.database.database_schema import Tables, Columns
import bcrypt

def update_user_password(username: str, new_password: str):
    """Actualiza la contraseña de un usuario específico"""
    try:
        db = MySQLConnection()
        
        # Verificar si el usuario existe
        check_query = f"""
            SELECT {Columns.Users.ID}, {Columns.Users.USERNAME}
            FROM {Tables.USER}
            WHERE {Columns.Users.USERNAME} = %s
        """
        user = db.execute_query(check_query, (username,))
        
        if not user:
            print(f"Usuario no encontrado: {username}")
            return False
            
        # Hash de la nueva contraseña - usando el mismo método que createUser
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        # Actualizar la contraseña
        update_query = f"""
            UPDATE {Tables.USER}
            SET {Columns.Users.PASSWORD} = %s
            WHERE {Columns.Users.USERNAME} = %s
        """
        
        if db.execute_query(update_query, (hashed_password, username)):
            print(f"Contraseña actualizada exitosamente para el usuario: {username}")
            return True
        else:
            print(f"No se pudo actualizar la contraseña para el usuario: {username}")
            return False
            
    except Exception as e:
        print(f"Error actualizando contraseña: {str(e)}")
        return False

if __name__ == "__main__":
    # Aquí puedes especificar el usuario y la nueva contraseña
    username = input("Ingrese el nombre de usuario: ")
    new_password = input("Ingrese la nueva contraseña: ")
    
    if update_user_password(username, new_password):
        print("Proceso completado exitosamente")
    else:
        print("El proceso falló") 