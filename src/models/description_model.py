from typing import List, Dict, Optional
from database.connection import MySQLConnection
from database.database_schema import Tables, Columns

class DescriptionModel:
    def __init__(self):
        """Inicializa el modelo de description"""
        self.db = MySQLConnection()
        self.table = Tables.DESCRIPTION

    def get_all_descriptions(self) -> List[Dict]:
        """Obtiene todas las descriptions registradas

        Returns:
            List[Dict]: Lista de diccionarios con los datos de las descriptions
        """
        query = f"""
            SELECT id_description, Description
            FROM {self.table}
            ORDER BY Description
        """
        return self.db.fetch_all(query)

    def get_description_by_id(self, description_id: int) -> Optional[Dict]:
        """Obtiene una description por su ID

        Args:
            description_id (int): ID de la description a buscar

        Returns:
            Optional[Dict]: Diccionario con los datos de la description o None si no existe
        """
        query = f"""
            SELECT id_description, Description
            FROM {self.table}
            WHERE id_description = %s
        """
        return self.db.fetch_one(query, (description_id,))

    def create_description(self, description_value: str) -> bool:
        """Crea una nueva description

        Args:
            description_value (str): Valor de la description (máximo 5 caracteres)

        Returns:
            bool: True si se creó correctamente, False en caso contrario
        """
        if len(description_value) > 5:
            return False
            
        query = f"""
            INSERT INTO {self.table} (Description)
            VALUES (%s)
        """
        return bool(self.db.execute_query(query, (description_value,)))

    def update_description(self, description_id: int, description_value: str) -> bool:
        """Actualiza una description existente

        Args:
            description_id (int): ID de la description a actualizar
            description_value (str): Nuevo valor de la description

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        if len(description_value) > 5:
            return False
            
        query = f"""
            UPDATE {self.table}
            SET Description = %s
            WHERE id_description = %s
        """
        return bool(self.db.execute_query(query, (description_value, description_id)))

    def delete_description(self, description_id: int) -> bool:
        """Elimina una description

        Args:
            description_id (int): ID de la description a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        query = f"""
            DELETE FROM {self.table}
            WHERE id_description = %s
        """
        return bool(self.db.execute_query(query, (description_id,))) 