from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class BaseConnection(ABC):
    """Clase base abstracta para conexiones a bases de datos"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._connection = None
        self._cursor = None

    @abstractmethod
    def connect(self) -> Any:
        """Establece la conexión con la base de datos"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Cierra la conexión con la base de datos"""
        pass

    @abstractmethod
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Any:
        """Ejecuta una consulta SQL"""
        pass

    @abstractmethod
    def fetch_all(self, query: str, params: Optional[tuple] = None) -> List[Dict]:
        """Ejecuta una consulta y devuelve todos los resultados"""
        pass

    @abstractmethod
    def fetch_one(self, query: str, params: Optional[tuple] = None) -> Optional[Dict]:
        """Ejecuta una consulta y devuelve un solo resultado"""
        pass

    @abstractmethod
    def begin_transaction(self) -> None:
        """Inicia una transacción"""
        pass

    @abstractmethod
    def commit(self) -> None:
        """Confirma una transacción"""
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Revierte una transacción"""
        pass

    @property
    def is_connected(self) -> bool:
        """Verifica si la conexión está activa"""
        return self._connection is not None 