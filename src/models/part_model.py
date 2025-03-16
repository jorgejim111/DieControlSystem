from typing import List, Dict, Optional
from database.connection import MySQLConnection
from database.database_schema import Tables, Columns

class PartModel:
    def __init__(self):
        """Inicializa el modelo de parts"""
        self.db = MySQLConnection()
        self.table = Tables.PARTS

    def get_all_parts(self) -> List[Dict]:
        """Obtiene todas las parts registradas

        Returns:
            List[Dict]: Lista de diccionarios con los datos de las parts
        """
        query = f"""
            SELECT id_part, Part
            FROM {self.table}
            ORDER BY Part
        """
        return self.db.fetch_all(query)

    def get_part_by_id(self, part_id: int) -> Optional[Dict]:
        """Obtiene una part por su ID

        Args:
            part_id (int): ID de la part a buscar

        Returns:
            Optional[Dict]: Diccionario con los datos de la part o None si no existe
        """
        query = f"""
            SELECT id_part, Part
            FROM {self.table}
            WHERE id_part = %s
        """
        return self.db.fetch_one(query, (part_id,))

    def create_part(self, part_value: str) -> bool:
        """Crea una nueva part

        Args:
            part_value (str): Valor de la part (máximo 20 caracteres)

        Returns:
            bool: True si se creó correctamente, False en caso contrario
        """
        if len(part_value) > 20:
            return False
            
        query = f"""
            INSERT INTO {self.table} (Part)
            VALUES (%s)
        """
        return bool(self.db.execute_query(query, (part_value,)))

    def update_part(self, part_id: int, part_value: str) -> bool:
        """Actualiza una part existente

        Args:
            part_id (int): ID de la part a actualizar
            part_value (str): Nuevo valor de la part

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        if len(part_value) > 20:
            return False
            
        query = f"""
            UPDATE {self.table}
            SET Part = %s
            WHERE id_part = %s
        """
        return bool(self.db.execute_query(query, (part_value, part_id)))

    def delete_part(self, part_id: int) -> bool:
        """Elimina una part

        Args:
            part_id (int): ID de la part a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        query = f"""
            DELETE FROM {self.table}
            WHERE id_part = %s
        """
        return bool(self.db.execute_query(query, (part_id,))) 