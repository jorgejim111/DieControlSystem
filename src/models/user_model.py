from database.connection import MySQLConnection
from database.database_schema import Tables, Columns
from typing import List, Dict, Optional
import bcrypt

class UserModel:
    def __init__(self):
        self.db = MySQLConnection()
    
    def get_all_users(self) -> List[Dict]:
        """Obtiene todos los usuarios con sus trabajadores asociados"""
        query = """
            SELECT u.*, w.{name} as worker_name
            FROM {user} u
            LEFT JOIN {workers} w ON u.{worker_id} = w.{worker_pk}
            ORDER BY u.{username}
        """.format(
            user=Tables.USER,
            workers=Tables.WORKERS,
            name=Columns.Workers.NAME,
            worker_id=Columns.Users.WORKER_ID,
            worker_pk=Columns.Workers.ID,
            username=Columns.Users.USERNAME
        )
        return self.db.fetch_all(query)
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Obtiene un usuario por su ID"""
        query = """
            SELECT u.*, w.{name} as worker_name
            FROM {user} u
            LEFT JOIN {workers} w ON u.{worker_id} = w.{worker_pk}
            WHERE u.{id} = %s
        """.format(
            user=Tables.USER,
            workers=Tables.WORKERS,
            name=Columns.Workers.NAME,
            worker_id=Columns.Users.WORKER_ID,
            worker_pk=Columns.Workers.ID,
            id=Columns.Users.ID
        )
        return self.db.fetch_one(query, (user_id,))
    
    def create_user(self, user_id: int, username: str, email: str, password: str, worker_id: Optional[int] = None) -> bool:
        """Crea un nuevo usuario"""
        # Hash de la contraseña
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        query = """
            INSERT INTO {user} ({id}, {username}, {email}, {password}, {worker_id}, {create_time})
            VALUES (%s, %s, %s, %s, %s, NOW())
        """.format(
            user=Tables.USER,
            id=Columns.Users.ID,
            username=Columns.Users.USERNAME,
            email=Columns.Users.EMAIL,
            password=Columns.Users.PASSWORD,
            worker_id=Columns.Users.WORKER_ID,
            create_time=Columns.Users.CREATE_TIME
        )
        return bool(self.db.execute_query(query, (user_id, username, email, hashed, worker_id)))
    
    def update_user(self, user_id: int, username: str, email: str, worker_id: Optional[int] = None) -> bool:
        """Actualiza un usuario existente"""
        query = """
            UPDATE {user}
            SET {username} = %s,
                {email} = %s,
                {worker_id} = %s
            WHERE {id} = %s
        """.format(
            user=Tables.USER,
            username=Columns.Users.USERNAME,
            email=Columns.Users.EMAIL,
            worker_id=Columns.Users.WORKER_ID,
            id=Columns.Users.ID
        )
        return bool(self.db.execute_query(query, (username, email, worker_id, user_id)))
    
    def update_password(self, user_id: int, new_password: str) -> bool:
        """Actualiza la contraseña de un usuario"""
        # Hash de la nueva contraseña
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        query = """
            UPDATE {user}
            SET {password} = %s
            WHERE {id} = %s
        """.format(
            user=Tables.USER,
            password=Columns.Users.PASSWORD,
            id=Columns.Users.ID
        )
        return bool(self.db.execute_query(query, (hashed, user_id)))
    
    def delete_user(self, user_id: int) -> bool:
        """Elimina un usuario"""
        query = "DELETE FROM {user} WHERE {id} = %s".format(
            user=Tables.USER,
            id=Columns.Users.ID
        )
        return bool(self.db.execute_query(query, (user_id,)))
    
    def get_all_workers_not_assigned(self) -> List[Dict]:
        """Obtiene todos los trabajadores que no están asignados a un usuario"""
        query = """
            SELECT w.{worker_id}, w.{name}
            FROM {workers} w
            LEFT JOIN {user} u ON w.{worker_pk} = u.{user_worker_id}
            WHERE u.{user_id} IS NULL
            ORDER BY w.{name}
        """.format(
            workers=Tables.WORKERS,
            user=Tables.USER,
            worker_id=Columns.Workers.ID,
            name=Columns.Workers.NAME,
            worker_pk=Columns.Workers.ID,
            user_worker_id=Columns.Users.WORKER_ID,
            user_id=Columns.Users.ID
        )
        return self.db.fetch_all(query)
    
    def get_all_workers(self) -> List[Dict]:
        """Obtiene todos los trabajadores"""
        query = """
            SELECT {worker_id}, {name}
            FROM {workers}
            ORDER BY {name}
        """.format(
            workers=Tables.WORKERS,
            worker_id=Columns.Workers.ID,
            name=Columns.Workers.NAME
        )
        return self.db.fetch_all(query)
    
    def validate_login(self, username: str, password: str) -> Optional[Dict]:
        """Valida las credenciales de un usuario"""
        query = """
            SELECT {id}, {username}, {email}, {password}
            FROM {user}
            WHERE {username} = %s
        """.format(
            user=Tables.USER,
            id=Columns.Users.ID,
            username=Columns.Users.USERNAME,
            email=Columns.Users.EMAIL,
            password=Columns.Users.PASSWORD
        )
        user = self.db.fetch_one(query, (username,))
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[Columns.Users.PASSWORD].encode('utf-8')):
            return {
                Columns.Users.ID: user[Columns.Users.ID],
                Columns.Users.USERNAME: user[Columns.Users.USERNAME],
                Columns.Users.EMAIL: user[Columns.Users.EMAIL]
            }
        return None
    
    def get_user_roles(self, user_id: int) -> List[Dict]:
        """Obtiene todos los roles asignados a un usuario"""
        query = """
            SELECT r.{role_id}, r.{role_name}
            FROM {roles} r
            INNER JOIN {roles_user} ru ON r.{role_id} = ru.{role_id}
            WHERE ru.{user_id} = %s
            ORDER BY r.{role_name}
        """.format(
            roles=Tables.ROLES,
            roles_user=Tables.ROLES_USER,
            role_id=Columns.Roles.ID,
            role_name=Columns.Roles.ROLE,
            user_id=Columns.RolesUser.USER_ID
        )
        return self.db.fetch_all(query, (user_id,))
    
    def assign_role_to_user(self, user_id: int, role_id: int) -> bool:
        """Asigna un rol a un usuario"""
        query = """
            INSERT INTO {roles_user} ({user_id}, {role_id})
            VALUES (%s, %s)
        """.format(
            roles_user=Tables.ROLES_USER,
            user_id=Columns.RolesUser.USER_ID,
            role_id=Columns.RolesUser.ROLE_ID
        )
        return bool(self.db.execute_query(query, (user_id, role_id)))
    
    def remove_role_from_user(self, user_id: int, role_id: int) -> bool:
        """Elimina un rol de un usuario"""
        query = """
            DELETE FROM {roles_user}
            WHERE {user_id} = %s AND {role_id} = %s
        """.format(
            roles_user=Tables.ROLES_USER,
            user_id=Columns.RolesUser.USER_ID,
            role_id=Columns.RolesUser.ROLE_ID
        )
        return bool(self.db.execute_query(query, (user_id, role_id)))
    
    def remove_all_user_roles(self, user_id: int) -> bool:
        """Elimina todos los roles de un usuario"""
        query = """
            DELETE FROM {roles_user}
            WHERE {user_id} = %s
        """.format(
            roles_user=Tables.ROLES_USER,
            user_id=Columns.RolesUser.USER_ID
        )
        return bool(self.db.execute_query(query, (user_id,))) 