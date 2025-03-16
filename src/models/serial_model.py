from typing import List, Dict, Optional
from database.connection import MySQLConnection
from database.database_schema import Tables, Columns

class SerialModel:
    def __init__(self):
        """Inicializa el modelo de serials"""
        self.db = MySQLConnection()
        self.table = "serials"

    def getAllSerials(self) -> List[Dict]:
        """Obtiene todos los serials ordenados por Die Description y Serial

        Returns:
            List[Dict]: Lista de diccionarios con los datos de los serials
        """
        query = f"""
            SELECT s.id_serial, s.Serial, s.id_die_description, s.`inner`, s.`outer`,
                   s.id_status, d.Die_Description as DieDescription,
                   st.Status as StatusName
            FROM {self.table} s
            LEFT JOIN die_description d ON s.id_die_description = d.id_die_description
            LEFT JOIN status_seril st ON s.id_status = st.id_status
            ORDER BY d.Die_Description ASC, s.Serial ASC
        """
        return self.db.fetch_all(query)

    def getSerialById(self, serial_id: int) -> Optional[Dict]:
        """Obtiene un serial por su ID

        Args:
            serial_id (int): ID del serial a buscar

        Returns:
            Optional[Dict]: Diccionario con los datos del serial o None si no existe
        """
        query = f"""
            SELECT s.id_serial, s.Serial, s.id_die_description, s.`inner`, s.`outer`,
                   s.id_status, d.Die_Description as DieDescription,
                   st.Status as StatusName
            FROM {self.table} s
            LEFT JOIN die_description d ON s.id_die_description = d.id_die_description
            LEFT JOIN status_seril st ON s.id_status = st.id_status
            WHERE s.id_serial = %s
        """
        return self.db.fetch_one(query, (serial_id,))

    def createSerial(self, serial_number: str, die_description_id: int, inner: float, 
                    outer: float, status_id: int) -> bool:
        """Crea un nuevo serial

        Args:
            serial_number (str): Número de serial
            die_description_id (int): ID de la descripción del die asociado
            inner (float): Medida interior
            outer (float): Medida exterior
            status_id (int): ID del status

        Returns:
            bool: True si se creó correctamente, False en caso contrario
        """
        # Convertir a mayúsculas y eliminar espacios
        serial_number = serial_number.strip().upper()
        
        if len(serial_number) > 15:  # Validar longitud máxima
            return False
            
        # Verificar si ya existe un serial con el mismo número
        check_query = f"SELECT id_serial FROM {self.table} WHERE Serial = %s"
        if self.db.fetch_one(check_query, (serial_number,)):
            return False
            
        query = f"""
            INSERT INTO {self.table} (Serial, id_die_description, `inner`, `outer`, id_status)
            VALUES (%s, %s, %s, %s, %s)
        """
        return bool(self.db.execute_query(query, (serial_number, die_description_id, 
                                                inner, outer, status_id)))

    def updateSerial(self, serial_id: int, serial_number: str, die_description_id: int, 
                    inner: float, outer: float, status_id: int) -> bool:
        """Actualiza un serial existente

        Args:
            serial_id (int): ID del serial a actualizar
            serial_number (str): Nuevo número de serial
            die_description_id (int): Nuevo ID de la descripción del die
            inner (float): Nueva medida interior
            outer (float): Nueva medida exterior
            status_id (int): Nuevo ID del status

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        # Convertir a mayúsculas y eliminar espacios
        serial_number = serial_number.strip().upper()
        
        if len(serial_number) > 15:  # Validar longitud máxima
            return False
            
        # Verificar si ya existe otro serial con el mismo número
        check_query = f"""
            SELECT id_serial 
            FROM {self.table} 
            WHERE Serial = %s AND id_serial != %s
        """
        if self.db.fetch_one(check_query, (serial_number, serial_id)):
            return False
            
        query = f"""
            UPDATE {self.table}
            SET Serial = %s, id_die_description = %s, `inner` = %s, `outer` = %s, id_status = %s
            WHERE id_serial = %s
        """
        return bool(self.db.execute_query(query, (serial_number, die_description_id, 
                                                inner, outer, status_id, serial_id)))

    def deleteSerial(self, serial_id: int) -> bool:
        """Elimina un serial

        Args:
            serial_id (int): ID del serial a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        query = f"""
            DELETE FROM {self.table}
            WHERE id_serial = %s
        """
        return bool(self.db.execute_query(query, (serial_id,)))

    def getAllDieDescriptions(self) -> List[Dict]:
        """Obtiene todas las descripciones de dies disponibles

        Returns:
            List[Dict]: Lista de diccionarios con los datos de las descripciones
        """
        query = """
            SELECT d.id_die_description,
                   d.Die_Description as Description
            FROM die_description d
            WHERE d.Obsolet = 0
            ORDER BY d.Die_Description
        """
        return self.db.fetch_all(query)

    def getAllStatus(self) -> List[Dict]:
        """Obtiene todos los status disponibles

        Returns:
            List[Dict]: Lista de diccionarios con los datos de los status
        """
        query = """
            SELECT id_status, Status
            FROM status_seril
            ORDER BY Status
        """
        return self.db.fetch_all(query)

    def getAllInches(self) -> List[Dict]:
        """Obtiene todos los inches disponibles

        Returns:
            List[Dict]: Lista de diccionarios con los datos de los inches
        """
        query = """
            SELECT i.id_inch, i.Inch
            FROM inches i
            WHERE i.id_inch IN (
                SELECT DISTINCT d.id_inch
                FROM die_description d
                WHERE d.Obsolet = 0
            )
            ORDER BY i.Inch
        """
        return self.db.fetch_all(query)

    def getPartsByInch(self, inch_id: int) -> List[Dict]:
        """Obtiene las parts disponibles para un inch específico

        Args:
            inch_id (int): ID del inch seleccionado

        Returns:
            List[Dict]: Lista de diccionarios con los datos de las parts
        """
        query = """
            SELECT DISTINCT p.id_part, p.Part
            FROM parts p
            INNER JOIN die_description d ON d.id_part = p.id_part
            WHERE d.id_inch = %s AND d.Obsolet = 0
            ORDER BY p.Part
        """
        return self.db.fetch_all(query, (inch_id,))

    def getDescriptionsByInchAndPart(self, inch_id: int, part_id: int) -> List[Dict]:
        """Obtiene las descripciones disponibles para un inch y part específicos

        Args:
            inch_id (int): ID del inch seleccionado
            part_id (int): ID del part seleccionado

        Returns:
            List[Dict]: Lista de diccionarios con los datos de las descripciones
        """
        query = """
            SELECT d.id_die_description, d.Die_Description
            FROM die_description d
            WHERE d.id_inch = %s 
            AND d.id_part = %s 
            AND d.Obsolet = 0
            ORDER BY d.Die_Description
        """
        return self.db.fetch_all(query, (inch_id, part_id))

    def getDieDescriptionById(self, die_id: int) -> Optional[Dict]:
        """Obtiene los datos completos de un die description por su ID

        Args:
            die_id (int): ID del die description

        Returns:
            Optional[Dict]: Diccionario con los datos del die description o None si no existe
        """
        query = """
            SELECT d.id_die_description, d.Die_Description, d.id_inch, d.id_part
            FROM die_description d
            WHERE d.id_die_description = %s
        """
        return self.db.fetch_one(query, (die_id,)) 