from typing import List, Dict, Optional
from database.connection import MySQLConnection
from database.database_schema import Tables, Columns

class LineModel:
    def __init__(self):
        """Inicializa el modelo de line"""
        self.db = MySQLConnection()
        self.table = "line"  # Nombre de la tabla en la base de datos

    def getAllLines(self) -> List[Dict]:
        """Obtiene todas las líneas ordenadas por Line

        Returns:
            List[Dict]: Lista de diccionarios con los datos de las líneas
        """
        query = f"""
            SELECT id_line, Line
            FROM {self.table}
            ORDER BY Line
        """
        return self.db.fetch_all(query)

    def getLineById(self, line_id: int) -> Optional[Dict]:
        """Obtiene una línea por su ID

        Args:
            line_id (int): ID de la línea a buscar

        Returns:
            Optional[Dict]: Diccionario con los datos de la línea o None si no existe
        """
        query = f"""
            SELECT id_line, Line
            FROM {self.table}
            WHERE id_line = %s
        """
        return self.db.fetch_one(query, (line_id,))

    def createLine(self, line_name: str) -> bool:
        """Crea una nueva línea

        Args:
            line_name (str): Nombre de la línea a crear

        Returns:
            bool: True si se creó correctamente, False en caso contrario
        """
        if len(line_name) > 10:  # Validar longitud máxima
            return False
            
        # Verificar si ya existe una línea con el mismo nombre
        check_query = f"SELECT id_line FROM {self.table} WHERE Line = %s"
        if self.db.fetch_one(check_query, (line_name,)):
            return False
            
        query = f"""
            INSERT INTO {self.table} (Line)
            VALUES (%s)
        """
        return bool(self.db.execute_query(query, (line_name,)))

    def updateLine(self, line_id: int, line_name: str) -> bool:
        """Actualiza una línea existente

        Args:
            line_id (int): ID de la línea a actualizar
            line_name (str): Nuevo nombre de la línea

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        if len(line_name) > 10:  # Validar longitud máxima
            return False
            
        # Verificar si ya existe otra línea con el mismo nombre
        check_query = f"""
            SELECT id_line 
            FROM {self.table} 
            WHERE Line = %s AND id_line != %s
        """
        if self.db.fetch_one(check_query, (line_name, line_id)):
            return False
            
        query = f"""
            UPDATE {self.table}
            SET Line = %s
            WHERE id_line = %s
        """
        return bool(self.db.execute_query(query, (line_name, line_id)))

    def deleteLine(self, line_id: int) -> bool:
        """Elimina una línea

        Args:
            line_id (int): ID de la línea a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        query = f"""
            DELETE FROM {self.table}
            WHERE id_line = %s
        """
        return bool(self.db.execute_query(query, (line_id,))) 