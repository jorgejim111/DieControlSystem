from typing import List, Dict, Optional
from database.connection import MySQLConnection
from database.database_schema import Tables, Columns

class DRStatusModel:
    def __init__(self):
        """Inicializa el modelo de DR Status"""
        self.db = MySQLConnection()

    def getAllStatus(self) -> List[Dict]:
        """Obtiene todos los estados ordenados por Status

        Returns:
            List[Dict]: Lista de diccionarios con los datos de los estados
        """
        query = f"""
            SELECT * FROM {Tables.DR_STATUS}
            ORDER BY {Columns.DRStatus.STATUS}
        """
        return self.db.execute_query(query)

    def getStatusById(self, status_id: int) -> Optional[Dict]:
        """Obtiene un estado por su ID

        Args:
            status_id (int): ID del estado a buscar

        Returns:
            Optional[Dict]: Diccionario con los datos del estado o None si no existe
        """
        query = f"""
            SELECT * FROM {Tables.DR_STATUS}
            WHERE {Columns.DRStatus.ID} = %s
        """
        result = self.db.execute_query(query, (status_id,))
        return result[0] if result else None

    def createStatus(self, status_text: str) -> bool:
        """Crea un nuevo estado

        Args:
            status_text (str): Texto del estado a crear

        Returns:
            bool: True si se creó correctamente, False en caso contrario
        """
        if len(status_text) > 45:  # Validar longitud máxima
            return False
            
        # Verificar si ya existe un estado con el mismo texto
        check_query = f"SELECT {Columns.DRStatus.ID} FROM {Tables.DR_STATUS} WHERE {Columns.DRStatus.STATUS} = %s"
        if self.db.fetch_one(check_query, (status_text,)):
            return False
            
        query = f"""
            INSERT INTO {Tables.DR_STATUS}
            ({Columns.DRStatus.STATUS})
            VALUES (%s)
        """
        return bool(self.db.execute_query(query, (status_text,)))

    def updateStatus(self, status_id: int, status_text: str) -> bool:
        """Actualiza un estado existente

        Args:
            status_id (int): ID del estado a actualizar
            status_text (str): Nuevo texto del estado

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        if len(status_text) > 45:  # Validar longitud máxima
            return False
            
        # Verificar si ya existe otro estado con el mismo texto
        check_query = f"""
            SELECT {Columns.DRStatus.ID} 
            FROM {Tables.DR_STATUS} 
            WHERE {Columns.DRStatus.STATUS} = %s AND {Columns.DRStatus.ID} != %s
        """
        if self.db.fetch_one(check_query, (status_text, status_id)):
            return False
            
        query = f"""
            UPDATE {Tables.DR_STATUS}
            SET {Columns.DRStatus.STATUS} = %s
            WHERE {Columns.DRStatus.ID} = %s
        """
        return bool(self.db.execute_query(query, (status_text, status_id)))

    def deleteStatus(self, status_id: int) -> bool:
        """Elimina un estado

        Args:
            status_id (int): ID del estado a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        query = f"""
            DELETE FROM {Tables.DR_STATUS}
            WHERE {Columns.DRStatus.ID} = %s
        """
        return bool(self.db.execute_query(query, (status_id,))) 