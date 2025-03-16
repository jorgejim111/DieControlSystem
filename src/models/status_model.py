from typing import List, Dict, Optional
from database.connection import MySQLConnection
from database.database_schema import Tables, Columns

class StatusModel:
    def __init__(self):
        """Inicializa el modelo de status"""
        self.db = MySQLConnection()
        self.table = "status_seril"  # Nombre de la tabla en la base de datos

    def getAllStatus(self) -> List[Dict]:
        """Obtiene todos los status ordenados por Status

        Returns:
            List[Dict]: Lista de diccionarios con los datos de los status
        """
        query = f"""
            SELECT id_status, Status
            FROM {self.table}
            ORDER BY Status
        """
        return self.db.fetch_all(query)

    def getStatusById(self, status_id: int) -> Optional[Dict]:
        """Obtiene un status por su ID

        Args:
            status_id (int): ID del status a buscar

        Returns:
            Optional[Dict]: Diccionario con los datos del status o None si no existe
        """
        query = f"""
            SELECT id_status, Status
            FROM {self.table}
            WHERE id_status = %s
        """
        return self.db.fetch_one(query, (status_id,))

    def createStatus(self, status_name: str) -> bool:
        """Crea un nuevo status

        Args:
            status_name (str): Nombre del status a crear

        Returns:
            bool: True si se creó correctamente, False en caso contrario
        """
        if len(status_name) > 45:  # Validar longitud máxima
            return False
            
        # Verificar si ya existe un status con el mismo nombre
        check_query = f"SELECT id_status FROM {self.table} WHERE Status = %s"
        if self.db.fetch_one(check_query, (status_name,)):
            return False
            
        query = f"""
            INSERT INTO {self.table} (Status)
            VALUES (%s)
        """
        return bool(self.db.execute_query(query, (status_name,)))

    def updateStatus(self, status_id: int, status_name: str) -> bool:
        """Actualiza un status existente

        Args:
            status_id (int): ID del status a actualizar
            status_name (str): Nuevo nombre del status

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        if len(status_name) > 45:  # Validar longitud máxima
            return False
            
        # Verificar si ya existe otro status con el mismo nombre
        check_query = f"""
            SELECT id_status 
            FROM {self.table} 
            WHERE Status = %s AND id_status != %s
        """
        if self.db.fetch_one(check_query, (status_name, status_id)):
            return False
            
        query = f"""
            UPDATE {self.table}
            SET Status = %s
            WHERE id_status = %s
        """
        return bool(self.db.execute_query(query, (status_name, status_id)))

    def deleteStatus(self, status_id: int) -> bool:
        """Elimina un status

        Args:
            status_id (int): ID del status a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        query = f"""
            DELETE FROM {self.table}
            WHERE id_status = %s
        """
        return bool(self.db.execute_query(query, (status_id,))) 