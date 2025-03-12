class DatabaseError(Exception):
    """Clase base para excepciones de base de datos"""
    pass

class ConnectionError(DatabaseError):
    """Excepción lanzada por errores de conexión"""
    pass

class QueryError(DatabaseError):
    """Excepción lanzada por errores en consultas"""
    pass

class TransactionError(DatabaseError):
    """Excepción lanzada por errores en transacciones"""
    pass 