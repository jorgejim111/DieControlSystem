from typing import List, Dict, Optional
from database.connection import MySQLConnection
from database.database_schema import Tables, Columns

class ProductModel:
    def __init__(self):
        """Inicializa el modelo de productos"""
        self.db = MySQLConnection()
        self.table = "products"

    def getAllProducts(self) -> List[Dict]:
        """Obtiene todos los productos ordenados primero por Die Description y luego por Product

        Returns:
            List[Dict]: Lista de diccionarios con los datos de los productos
        """
        query = f"""
            SELECT p.id_product, p.Product, p.id_die_description,
                   d.Die_Description as DieDescription
            FROM {self.table} p
            LEFT JOIN die_description d ON p.id_die_description = d.id_die_description
            ORDER BY d.Die_Description ASC, p.Product ASC
        """
        return self.db.fetch_all(query)

    def getProductById(self, product_id: int) -> Optional[Dict]:
        """Obtiene un producto por su ID

        Args:
            product_id (int): ID del producto a buscar

        Returns:
            Optional[Dict]: Diccionario con los datos del producto o None si no existe
        """
        query = f"""
            SELECT p.id_product, p.Product, p.id_die_description,
                   d.Die_Description as DieDescription
            FROM {self.table} p
            LEFT JOIN die_description d ON p.id_die_description = d.id_die_description
            WHERE p.id_product = %s
        """
        return self.db.fetch_one(query, (product_id,))

    def createProduct(self, product_name: str, die_description_id: int) -> bool:
        """Crea un nuevo producto

        Args:
            product_name (str): Nombre del producto
            die_description_id (int): ID de la descripción del die asociado

        Returns:
            bool: True si se creó correctamente, False en caso contrario
        """
        # Convertir a mayúsculas
        product_name = product_name.strip().upper()
        
        if len(product_name) > 100:  # Validar longitud máxima
            return False
            
        # Verificar si ya existe un producto con el mismo nombre
        check_query = f"SELECT id_product FROM {self.table} WHERE Product = %s"
        if self.db.fetch_one(check_query, (product_name,)):
            return False
            
        query = f"""
            INSERT INTO {self.table} (Product, id_die_description)
            VALUES (%s, %s)
        """
        return bool(self.db.execute_query(query, (product_name, die_description_id)))

    def updateProduct(self, product_id: int, product_name: str, die_description_id: int) -> bool:
        """Actualiza un producto existente

        Args:
            product_id (int): ID del producto a actualizar
            product_name (str): Nuevo nombre del producto
            die_description_id (int): Nuevo ID de la descripción del die

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        # Convertir a mayúsculas
        product_name = product_name.strip().upper()
        
        if len(product_name) > 100:  # Validar longitud máxima
            return False
            
        # Verificar si ya existe otro producto con el mismo nombre
        check_query = f"""
            SELECT id_product 
            FROM {self.table} 
            WHERE Product = %s AND id_product != %s
        """
        if self.db.fetch_one(check_query, (product_name, product_id)):
            return False
            
        query = f"""
            UPDATE {self.table}
            SET Product = %s, id_die_description = %s
            WHERE id_product = %s
        """
        return bool(self.db.execute_query(query, (product_name, die_description_id, product_id)))

    def deleteProduct(self, product_id: int) -> bool:
        """Elimina un producto

        Args:
            product_id (int): ID del producto a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        query = f"""
            DELETE FROM {self.table}
            WHERE id_product = %s
        """
        return bool(self.db.execute_query(query, (product_id,)))

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