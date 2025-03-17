from typing import List, Dict, Optional
from database.connection import MySQLConnection
from database.database_schema import Tables, Columns

class DRDescriptionModel:
    def __init__(self):
        """Inicializa el modelo de DR Description"""
        self.db = MySQLConnection()

    def getAllDescriptions(self) -> List[Dict]:
        """Obtiene todas las descripciones ordenadas por Description

        Returns:
            List[Dict]: Lista de diccionarios con los datos de las descripciones
        """
        query = f"""
            SELECT * FROM {Tables.DR_DESCRIPTION}
            ORDER BY {Columns.DRDescription.DESCRIPTION}
        """
        return self.db.execute_query(query)

    def getDescriptionById(self, description_id: int) -> Optional[Dict]:
        """Obtiene una descripción por su ID

        Args:
            description_id (int): ID de la descripción a buscar

        Returns:
            Optional[Dict]: Diccionario con los datos de la descripción o None si no existe
        """
        query = f"""
            SELECT * FROM {Tables.DR_DESCRIPTION}
            WHERE {Columns.DRDescription.ID} = %s
        """
        result = self.db.execute_query(query, (description_id,))
        return result[0] if result else None

    def createDescription(self, description_text: str) -> bool:
        """Crea una nueva descripción

        Args:
            description_text (str): Texto de la descripción a crear

        Returns:
            bool: True si se creó correctamente, False en caso contrario
        """
        if len(description_text) > 45:  # Validar longitud máxima
            return False
            
        # Verificar si ya existe una descripción con el mismo texto
        check_query = f"SELECT {Columns.DRDescription.ID} FROM {Tables.DR_DESCRIPTION} WHERE {Columns.DRDescription.DESCRIPTION} = %s"
        if self.db.fetch_one(check_query, (description_text,)):
            return False
            
        query = f"""
            INSERT INTO {Tables.DR_DESCRIPTION}
            ({Columns.DRDescription.DESCRIPTION})
            VALUES (%s)
        """
        return bool(self.db.execute_query(query, (description_text,)))

    def updateDescription(self, description_id: int, description_text: str) -> bool:
        """Actualiza una descripción existente

        Args:
            description_id (int): ID de la descripción a actualizar
            description_text (str): Nuevo texto de la descripción

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        if len(description_text) > 45:  # Validar longitud máxima
            return False
            
        # Verificar si ya existe otra descripción con el mismo texto
        check_query = f"""
            SELECT {Columns.DRDescription.ID} 
            FROM {Tables.DR_DESCRIPTION} 
            WHERE {Columns.DRDescription.DESCRIPTION} = %s AND {Columns.DRDescription.ID} != %s
        """
        if self.db.fetch_one(check_query, (description_text, description_id)):
            return False
            
        query = f"""
            UPDATE {Tables.DR_DESCRIPTION}
            SET {Columns.DRDescription.DESCRIPTION} = %s
            WHERE {Columns.DRDescription.ID} = %s
        """
        return bool(self.db.execute_query(query, (description_text, description_id)))

    def deleteDescription(self, description_id: int) -> bool:
        """Elimina una descripción

        Args:
            description_id (int): ID de la descripción a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        query = f"""
            DELETE FROM {Tables.DR_DESCRIPTION}
            WHERE {Columns.DRDescription.ID} = %s
        """
        return bool(self.db.execute_query(query, (description_id,))) 