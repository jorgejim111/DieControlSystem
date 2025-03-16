from typing import List, Dict, Optional
from database.connection import MySQLConnection
from database.database_schema import Tables, Columns

class InchModel:
    def __init__(self):
        """Inicializa el modelo de pulgadas"""
        self.db = MySQLConnection()
        self.table = Tables.INCHES

    def get_all_inches(self) -> List[Dict]:
        """Obtiene todas las pulgadas registradas

        Returns:
            List[Dict]: Lista de diccionarios con los datos de las pulgadas
        """
        query = f"""
            SELECT id_inch, Inch
            FROM {self.table}
            ORDER BY Inch
        """
        return self.db.fetch_all(query)

    def get_inch_by_id(self, inch_id: int) -> Optional[Dict]:
        """Obtiene una pulgada por su ID

        Args:
            inch_id (int): ID de la pulgada a buscar

        Returns:
            Optional[Dict]: Diccionario con los datos de la pulgada o None si no existe
        """
        query = f"""
            SELECT id_inch, Inch
            FROM {self.table}
            WHERE id_inch = %s
        """
        return self.db.fetch_one(query, (inch_id,))

    def create_inch(self, inch_value: str) -> bool:
        """Crea una nueva pulgada

        Args:
            inch_value (str): Valor de la pulgada (máximo 5 caracteres)

        Returns:
            bool: True si se creó correctamente, False en caso contrario
        """
        if len(inch_value) > 5:
            return False
            
        query = f"""
            INSERT INTO {self.table} (Inch)
            VALUES (%s)
        """
        return bool(self.db.execute_query(query, (inch_value,)))

    def update_inch(self, inch_id: int, inch_value: str) -> bool:
        """Actualiza una pulgada existente

        Args:
            inch_id (int): ID de la pulgada a actualizar
            inch_value (str): Nuevo valor de la pulgada

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        if len(inch_value) > 5:
            return False
            
        query = f"""
            UPDATE {self.table}
            SET Inch = %s
            WHERE id_inch = %s
        """
        return bool(self.db.execute_query(query, (inch_value, inch_id)))

    def delete_inch(self, inch_id: int) -> bool:
        """Elimina una pulgada

        Args:
            inch_id (int): ID de la pulgada a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        query = f"""
            DELETE FROM {self.table}
            WHERE id_inch = %s
        """
        return bool(self.db.execute_query(query, (inch_id,))) 