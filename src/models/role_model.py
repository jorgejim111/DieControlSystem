from database.connection import MySQLConnection
from database.database_schema import Tables, Columns
from typing import List, Dict, Optional

class RoleModel:
    def __init__(self):
        self.db = MySQLConnection()
    
    def getAllRoles(self) -> List[Dict]:
        """Obtiene todos los roles"""
        query = """
            SELECT {id}, {role}
            FROM {roles}
            ORDER BY {role}
        """.format(
            id=Columns.Roles.ID,
            role=Columns.Roles.ROLE,
            roles=Tables.ROLES
        )
        return self.db.fetch_all(query)
    
    def getRoleById(self, roleId: int) -> Optional[Dict]:
        """Obtiene un rol por su ID"""
        query = """
            SELECT {id}, {role}
            FROM {roles}
            WHERE {id} = %s
        """.format(
            id=Columns.Roles.ID,
            role=Columns.Roles.ROLE,
            roles=Tables.ROLES
        )
        return self.db.fetch_one(query, (roleId,))
    
    def createRole(self, roleName: str) -> bool:
        """Crea un nuevo rol"""
        query = """
            INSERT INTO {roles} ({role})
            VALUES (%s)
        """.format(
            roles=Tables.ROLES,
            role=Columns.Roles.ROLE
        )
        return bool(self.db.execute_query(query, (roleName,)))
    
    def updateRole(self, roleId: int, roleName: str) -> bool:
        """Actualiza un rol existente"""
        query = """
            UPDATE {roles}
            SET {role} = %s
            WHERE {id} = %s
        """.format(
            roles=Tables.ROLES,
            role=Columns.Roles.ROLE,
            id=Columns.Roles.ID
        )
        return bool(self.db.execute_query(query, (roleName, roleId)))
    
    def deleteRole(self, roleId: int) -> bool:
        """Elimina un rol"""
        query = "DELETE FROM {roles} WHERE {id} = %s".format(
            roles=Tables.ROLES,
            id=Columns.Roles.ID
        )
        return bool(self.db.execute_query(query, (roleId,))) 