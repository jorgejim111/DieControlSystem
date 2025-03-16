from typing import List, Dict, Optional
from database.connection import MySQLConnection
from database.database_schema import Tables, Columns

class DieDescriptionModel:
    def __init__(self):
        """Inicializa el modelo de die_description"""
        self.db = MySQLConnection()
        self.table = Tables.DIE_DESCRIPTION

    def get_all_die_descriptions(self) -> List[Dict]:
        """Obtiene todas las die descriptions con sus relaciones

        Returns:
            List[Dict]: Lista de diccionarios con los datos de las die descriptions
        """
        query = f"""
            SELECT 
                dd.id_die_description,
                dd.Die_Description,
                dd.Obsolet,
                dd.Circulation,
                dd.New,
                dd.create_time,
                dd.updat_time,
                i.Inch,
                d.Description,
                p.Part,
                dd.id_inch,
                dd.id_part,
                dd.id_description
            FROM {self.table} dd
            JOIN inches i ON dd.id_inch = i.id_inch
            JOIN parts p ON dd.id_part = p.id_part
            JOIN description d ON dd.id_description = d.id_description
            ORDER BY i.Inch, d.Description, p.Part
        """
        return self.db.fetch_all(query)

    def get_die_description_by_id(self, die_description_id: int) -> Optional[Dict]:
        """Obtiene una die description por su ID

        Args:
            die_description_id (int): ID de la die description a buscar

        Returns:
            Optional[Dict]: Diccionario con los datos de la die description o None si no existe
        """
        query = f"""
            SELECT 
                dd.id_die_description,
                dd.Die_Description,
                dd.Obsolet,
                dd.Circulation,
                dd.New,
                dd.create_time,
                dd.updat_time,
                i.Inch,
                d.Description,
                p.Part,
                dd.id_inch,
                dd.id_part,
                dd.id_description
            FROM {self.table} dd
            JOIN inches i ON dd.id_inch = i.id_inch
            JOIN parts p ON dd.id_part = p.id_part
            JOIN description d ON dd.id_description = d.id_description
            WHERE dd.id_die_description = %s
        """
        return self.db.fetch_one(query, (die_description_id,))

    def check_duplicate_die_description(self, die_description: str, exclude_id: int = None) -> bool:
        """Verifica si ya existe una Die Description con el mismo valor

        Args:
            die_description (str): El valor de Die Description a verificar
            exclude_id (int, optional): ID a excluir de la búsqueda (para actualizaciones)

        Returns:
            bool: True si existe un duplicado, False en caso contrario
        """
        query = f"SELECT id_die_description FROM {self.table} WHERE Die_Description = %s"
        params = [die_description]
        
        if exclude_id is not None:
            query += " AND id_die_description != %s"
            params.append(exclude_id)
            
        result = self.db.fetch_one(query, tuple(params))
        return result is not None

    def create_die_description(self, data: Dict) -> bool:
        """Crea una nueva die description

        Args:
            data (Dict): Diccionario con los datos de la die description

        Returns:
            bool: True si se creó correctamente, False en caso contrario
        """
        if len(data['Die_Description']) > 45:
            return False
            
        # Verificar duplicados
        if self.check_duplicate_die_description(data['Die_Description']):
            return False
            
        query = f"""
            INSERT INTO {self.table} (
                Die_Description,
                id_inch,
                id_part,
                id_description,
                Obsolet,
                Circulation,
                New
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['Die_Description'],
            data['id_inch'],
            data['id_part'],
            data['id_description'],
            data['Obsolet'],
            data['Circulation'],
            data['New']
        )
        return bool(self.db.execute_query(query, values))

    def update_die_description(self, die_description_id: int, data: Dict) -> bool:
        """Actualiza una die description existente

        Args:
            die_description_id (int): ID de la die description a actualizar
            data (Dict): Diccionario con los datos a actualizar

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        if len(data['Die_Description']) > 45:
            return False
            
        # Verificar duplicados excluyendo el ID actual
        if self.check_duplicate_die_description(data['Die_Description'], die_description_id):
            return False
            
        query = f"""
            UPDATE {self.table}
            SET Die_Description = %s,
                id_inch = %s,
                id_part = %s,
                id_description = %s,
                Obsolet = %s,
                Circulation = %s,
                New = %s,
                updat_time = CURRENT_TIMESTAMP
            WHERE id_die_description = %s
        """
        values = (
            data['Die_Description'],
            data['id_inch'],
            data['id_part'],
            data['id_description'],
            data['Obsolet'],
            data['Circulation'],
            data['New'],
            die_description_id
        )
        return bool(self.db.execute_query(query, values))

    def delete_die_description(self, die_description_id: int) -> bool:
        """Elimina una die description

        Args:
            die_description_id (int): ID de la die description a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        query = f"""
            DELETE FROM {self.table}
            WHERE id_die_description = %s
        """
        return bool(self.db.execute_query(query, (die_description_id,)))

    def get_related_data(self) -> Dict[str, List[Dict]]:
        """Obtiene los datos relacionados necesarios para el formulario

        Returns:
            Dict[str, List[Dict]]: Diccionario con las listas de inches, parts y descriptions
        """
        # Obtener inches ordenados
        inches_query = "SELECT id_inch, Inch FROM inches ORDER BY Inch"
        inches = self.db.fetch_all(inches_query)
        
        # Obtener descriptions ordenados
        descriptions_query = "SELECT id_description, Description FROM description ORDER BY Description"
        descriptions = self.db.fetch_all(descriptions_query)
        
        # Obtener parts ordenados
        parts_query = "SELECT id_part, Part FROM parts ORDER BY Part"
        parts = self.db.fetch_all(parts_query)
        
        return {
            'inches': inches,
            'descriptions': descriptions,
            'parts': parts
        } 