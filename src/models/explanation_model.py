from database.database_schema import Tables, Columns
from database.connection import MySQLConnection

class ExplanationModel:
    def __init__(self):
        self.db = MySQLConnection()
        
    def getAllExplanations(self):
        """Obtiene todas las explicaciones ordenadas por explanation"""
        query = f"""
            SELECT * FROM {Tables.EXPLANATION}
            ORDER BY {Columns.Explanation.EXPLANATION}
        """
        return self.db.execute_query(query)
    
    def getExplanationById(self, explanationId):
        """Obtiene una explicación por su ID"""
        query = f"""
            SELECT * FROM {Tables.EXPLANATION}
            WHERE {Columns.Explanation.ID} = %s
        """
        result = self.db.execute_query(query, (explanationId,))
        return result[0] if result else None
    
    def createExplanation(self, explanation):
        """Crea una nueva explicación"""
        query = f"""
            INSERT INTO {Tables.EXPLANATION}
            ({Columns.Explanation.EXPLANATION})
            VALUES (%s)
        """
        return self.db.execute_query(query, (explanation,))
    
    def updateExplanation(self, explanationId, explanation):
        """Actualiza una explicación existente"""
        query = f"""
            UPDATE {Tables.EXPLANATION}
            SET {Columns.Explanation.EXPLANATION} = %s
            WHERE {Columns.Explanation.ID} = %s
        """
        return self.db.execute_query(query, (explanation, explanationId))
    
    def deleteExplanation(self, explanationId):
        """Elimina una explicación"""
        query = f"""
            DELETE FROM {Tables.EXPLANATION}
            WHERE {Columns.Explanation.ID} = %s
        """
        return self.db.execute_query(query, (explanationId,)) 