from database.connection import MySQLConnection
from database.database_schema import Tables, Columns, CommonQueries
from typing import List, Dict, Optional
from datetime import datetime

class WorkerModel:
    def __init__(self):
        self.db = MySQLConnection()
    
    def getAllWorkers(self) -> List[Dict]:
        """Obtiene todos los trabajadores con sus posiciones"""
        return self.db.fetch_all(CommonQueries.GET_WORKER_WITH_POSITION)
    
    def getWorkerById(self, workerId: int) -> Optional[Dict]:
        """Obtiene un trabajador por su ID"""
        query = CommonQueries.GET_WORKER_WITH_POSITION + " WHERE w.{worker_id} = %s".format(
            worker_id=Columns.Workers.ID
        )
        return self.db.fetch_one(query, (workerId,))
    
    def createWorker(self, name: str, positionId: int) -> bool:
        """Crea un nuevo trabajador"""
        query = """
            INSERT INTO {workers} ({name}, {position_id})
            VALUES (%s, %s)
        """.format(
            workers=Tables.WORKERS,
            name=Columns.Workers.NAME,
            position_id=Columns.Workers.POSITION_ID
        )
        return bool(self.db.execute_query(query, (name, positionId)))
    
    def updateWorker(self, workerId: int, name: str, positionId: int) -> bool:
        """Actualiza un trabajador existente"""
        query = """
            UPDATE {workers}
            SET {name} = %s,
                {position_id} = %s
            WHERE {id} = %s
        """.format(
            workers=Tables.WORKERS,
            name=Columns.Workers.NAME,
            position_id=Columns.Workers.POSITION_ID,
            id=Columns.Workers.ID
        )
        return bool(self.db.execute_query(query, (name, positionId, workerId)))
    
    def deleteWorker(self, workerId: int) -> bool:
        """Elimina un trabajador"""
        query = "DELETE FROM {workers} WHERE {id} = %s".format(
            workers=Tables.WORKERS,
            id=Columns.Workers.ID
        )
        return bool(self.db.execute_query(query, (workerId,)))
            
    def getAllUsers(self) -> List[Dict]:
        """Obtiene todos los usuarios para el combo box"""
        query = """
            SELECT {id}, {username}
            FROM {users}
            ORDER BY {username}
        """.format(
            id=Columns.Users.ID,
            username=Columns.Users.USERNAME,
            users=Tables.USERS
        )
        return self.db.fetch_all(query)
    
    def getAllPositions(self) -> List[Dict]:
        """Obtiene todas las posiciones para el combo box"""
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