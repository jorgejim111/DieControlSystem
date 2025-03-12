from database.connection import MySQLConnection
from database.database_schema import Tables, Columns
from typing import List, Dict, Optional

class PositionModel:
    def __init__(self):
        self.db = MySQLConnection()
    
    def getAllPositions(self) -> List[Dict]:
        """Obtiene todas las posiciones"""
        query = """
            SELECT {id}, {position}
            FROM {positions}
            ORDER BY {position}
        """.format(
            id=Columns.Positions.ID,
            position=Columns.Positions.POSITION,
            positions=Tables.POSITIONS
        )
        return self.db.fetch_all(query)
    
    def getPositionById(self, positionId: int) -> Optional[Dict]:
        """Obtiene una posición por su ID"""
        query = """
            SELECT {id}, {position}
            FROM {positions}
            WHERE {id} = %s
        """.format(
            id=Columns.Positions.ID,
            position=Columns.Positions.POSITION,
            positions=Tables.POSITIONS
        )
        return self.db.fetch_one(query, (positionId,))
    
    def createPosition(self, positionName: str) -> bool:
        """Crea una nueva posición"""
        query = """
            INSERT INTO {positions} ({position})
            VALUES (%s)
        """.format(
            positions=Tables.POSITIONS,
            position=Columns.Positions.POSITION
        )
        return bool(self.db.execute_query(query, (positionName,)))
    
    def updatePosition(self, positionId: int, positionName: str) -> bool:
        """Actualiza una posición existente"""
        query = """
            UPDATE {positions}
            SET {position} = %s
            WHERE {id} = %s
        """.format(
            positions=Tables.POSITIONS,
            position=Columns.Positions.POSITION,
            id=Columns.Positions.ID
        )
        return bool(self.db.execute_query(query, (positionName, positionId)))
    
    def deletePosition(self, positionId: int) -> bool:
        """Elimina una posición"""
        query = "DELETE FROM {positions} WHERE {id} = %s".format(
            positions=Tables.POSITIONS,
            id=Columns.Positions.ID
        )
        return bool(self.db.execute_query(query, (positionId,))) 