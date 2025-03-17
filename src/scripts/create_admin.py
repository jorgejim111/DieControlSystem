import sys
import os

# Agregar el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database.connection import MySQLConnection
from src.database.database_schema import Tables, Columns
from src.models.user_model import UserModel
import bcrypt

def create_admin_user():
    """Crea un nuevo usuario admin"""
    try:
        db = MySQLConnection()
        user_model = UserModel()
        
        # Obtener todos los trabajadores
        workers = user_model.get_all_workers()
        if not workers:
            print("No hay trabajadores disponibles. Por favor, cree un trabajador primero.")
            return False
            
        # Usar el primer trabajador disponible
        worker_id = workers[0]['idWorkers']
        
        # Crear el usuario admin
        username = "admin"
        email = "admin@example.com"
        password = "admin123"
        
        if user_model.createUser(username, email, password, worker_id):
            print(f"Usuario admin creado exitosamente")
            return True
        else:
            print("No se pudo crear el usuario admin")
            return False
            
    except Exception as e:
        print(f"Error creando usuario admin: {str(e)}")
        return False

def update_admin_password():
    """Actualiza la contraseña del usuario admin"""
    try:
        db = MySQLConnection()
        
        # Verificar si el usuario admin existe
        check_query = f"""
            SELECT {Columns.Users.ID}, {Columns.Users.USERNAME}
            FROM {Tables.USER}
            WHERE {Columns.Users.USERNAME} = 'admin'
        """
        user = db.execute_query(check_query)
        
        if not user:
            print("Usuario admin no encontrado")
            return False
            
        # Hash de la nueva contraseña
        new_password = "admin123"
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        # Actualizar la contraseña
        update_query = f"""
            UPDATE {Tables.USER}
            SET {Columns.Users.PASSWORD} = %s
            WHERE {Columns.Users.USERNAME} = 'admin'
        """
        
        if db.execute_query(update_query, (hashed_password,)):
            print("Contraseña actualizada exitosamente para el usuario admin")
            return True
        else:
            print("No se pudo actualizar la contraseña")
            return False
            
    except Exception as e:
        print(f"Error actualizando contraseña: {str(e)}")
        return False

if __name__ == "__main__":
    print("Creando usuario admin...")
    if create_admin_user():
        print("\nActualizando contraseña del usuario admin...")
        if update_admin_password():
            print("\nProceso completado exitosamente")
            print("Usuario: admin")
            print("Contraseña: admin123")
        else:
            print("\nEl proceso falló al actualizar la contraseña")
    else:
        print("\nEl proceso falló al crear el usuario") 