import os
from typing import Any, List, Dict, Optional
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from threading import Lock
from .base_connection import BaseConnection
from .db_exceptions import ConnectionError, QueryError, TransactionError

# Cargar variables de entorno
load_dotenv()

class MySQLConnection(BaseConnection):
    """Implementación de conexión MySQL con patrón Singleton thread-safe"""
    
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self.host = os.getenv('DB_HOST')
            self.port = os.getenv('DB_PORT')
            self.database = os.getenv('DB_NAME')
            self.user = os.getenv('DB_USER')
            self.password = os.getenv('DB_PASSWORD')
            self._initialized = True

    def connect(self) -> Any:
        """Establece la conexión con MySQL"""
        try:
            if not self.is_connected:
                self._connection = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                self._cursor = self._connection.cursor(dictionary=True)
                self.logger.info("Conexión exitosa a la base de datos MySQL")
            return self._connection
        except Error as e:
            error_msg = f"Error al conectar a MySQL: {str(e)}"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)

    def disconnect(self) -> None:
        """Cierra la conexión con MySQL"""
        try:
            if self._cursor:
                self._cursor.close()
            if self.is_connected:
                self._connection.close()
                self._connection = None
                self.logger.info("Conexión cerrada")
        except Error as e:
            error_msg = f"Error al cerrar la conexión: {str(e)}"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)

    def execute_query(self, query: str, params: Optional[tuple] = None) -> Any:
        """Ejecuta una consulta SQL"""
        try:
            self.connect()
            self._cursor.execute(query, params or ())
            if not query.strip().upper().startswith('SELECT'):
                self._connection.commit()
            return self._cursor
        except Error as e:
            if self.is_connected:
                self._connection.rollback()
            error_msg = f"Error al ejecutar la consulta: {str(e)}"
            self.logger.error(error_msg)
            raise QueryError(error_msg)

    def fetch_all(self, query: str, params: Optional[tuple] = None) -> List[Dict]:
        """Ejecuta una consulta y devuelve todos los resultados"""
        cursor = self.execute_query(query, params)
        return cursor.fetchall()

    def fetch_one(self, query: str, params: Optional[tuple] = None) -> Optional[Dict]:
        """Ejecuta una consulta y devuelve un solo resultado"""
        cursor = self.execute_query(query, params)
        return cursor.fetchone()

    def begin_transaction(self) -> None:
        """Inicia una transacción"""
        try:
            self.connect()
            self._connection.start_transaction()
            self.logger.info("Transacción iniciada")
        except Error as e:
            error_msg = f"Error al iniciar la transacción: {str(e)}"
            self.logger.error(error_msg)
            raise TransactionError(error_msg)

    def commit(self) -> None:
        """Confirma una transacción"""
        try:
            self._connection.commit()
            self.logger.info("Transacción confirmada")
        except Error as e:
            error_msg = f"Error al confirmar la transacción: {str(e)}"
            self.logger.error(error_msg)
            raise TransactionError(error_msg)

    def rollback(self) -> None:
        """Revierte una transacción"""
        try:
            self._connection.rollback()
            self.logger.info("Transacción revertida")
        except Error as e:
            error_msg = f"Error al revertir la transacción: {str(e)}"
            self.logger.error(error_msg)
            raise TransactionError(error_msg)

    def get_table_schema(self, table_name: str) -> List[Dict]:
        """Obtiene la estructura de una tabla específica"""
        try:
            return self.fetch_all(f"""
                SELECT 
                    COLUMN_NAME as column_name,
                    COLUMN_TYPE as data_type,
                    IS_NULLABLE as is_nullable,
                    COLUMN_KEY as key_type,
                    COLUMN_DEFAULT as default_value,
                    EXTRA as extra
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION
            """, (self.database, table_name))
        except Error as e:
            error_msg = f"Error al obtener el esquema de la tabla {table_name}: {str(e)}"
            self.logger.error(error_msg)
            raise QueryError(error_msg)

    def get_table_relationships(self, table_name: str) -> List[Dict]:
        """Obtiene las relaciones de una tabla específica"""
        try:
            return self.fetch_all(f"""
                SELECT 
                    CONSTRAINT_NAME as constraint_name,
                    COLUMN_NAME as column_name,
                    REFERENCED_TABLE_NAME as referenced_table,
                    REFERENCED_COLUMN_NAME as referenced_column
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = %s 
                    AND TABLE_NAME = %s
                    AND REFERENCED_TABLE_NAME IS NOT NULL
            """, (self.database, table_name))
        except Error as e:
            error_msg = f"Error al obtener las relaciones de la tabla {table_name}: {str(e)}"
            self.logger.error(error_msg)
            raise QueryError(error_msg)

    def get_all_tables(self) -> List[str]:
        """Obtiene la lista de todas las tablas en la base de datos"""
        try:
            tables = self.fetch_all("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = %s
            """, (self.database,))
            return [table['TABLE_NAME'] for table in tables]
        except Error as e:
            error_msg = f"Error al obtener la lista de tablas: {str(e)}"
            self.logger.error(error_msg)
            raise QueryError(error_msg)

# Función de utilidad para probar la conexión
def test_connection():
    try:
        db = MySQLConnection()
        db.connect()
        version = db.fetch_one("SELECT VERSION() as version")
        print(f"Conectado a MySQL Server versión {version['version']}")
        db.disconnect()
        return True
    except Exception as e:
        print(f"Error de conexión: {str(e)}")
        return False 