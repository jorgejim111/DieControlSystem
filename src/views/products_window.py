from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from models.product_model import ProductModel
from views.product_dialog import ProductDialog

class ProductsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Products Management")
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.productModel = ProductModel()
        self.setupUI()
        self.loadProducts()
        
    def setupUI(self):
        # Layout principal
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)
        self.setLayout(mainLayout)
        
        # Frame superior para el logo
        topFrame = QFrame()
        topFrame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        topFrame.setFrameShape(QFrame.StyledPanel)
        topLayout = QHBoxLayout(topFrame)
        topLayout.setContentsMargins(5, 5, 5, 5)
        
        # Título de la sección
        titleLabel = QLabel("Products Management")
        titleLabel.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        topLayout.addWidget(titleLabel)
        
        # Agregar espaciador entre el título y el logo
        topLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Agregar logo
        logoLabel = QLabel()
        logoPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'logo_masternet.png')
        if os.path.exists(logoPath):
            pixmap = QPixmap(logoPath)
            scaledPixmap = pixmap.scaled(108, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logoLabel.setPixmap(scaledPixmap)
            logoLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        topLayout.addWidget(logoLabel)
        mainLayout.addWidget(topFrame)
        
        # Frame principal para el contenido
        contentFrame = QFrame()
        contentFrame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #0056b3;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #003d80;
            }
            QPushButton#deleteButton {
                background-color: #dc3545;
            }
            QPushButton#deleteButton:hover {
                background-color: #c82333;
            }
            QTableWidget {
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 5px;
                border: 1px solid #cccccc;
                font-weight: bold;
            }
        """)
        contentLayout = QVBoxLayout(contentFrame)
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        
        # Espaciador
        toolbar.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Botones
        self.addButton = QPushButton("Add Product")
        self.editButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.setObjectName("deleteButton")
        
        toolbar.addWidget(self.addButton)
        toolbar.addWidget(self.editButton)
        toolbar.addWidget(self.deleteButton)
        
        contentLayout.addLayout(toolbar)
        
        # Tabla de productos
        self.productsTable = QTableWidget()
        self.productsTable.setColumnCount(2)  # Product y Die Description
        self.productsTable.setHorizontalHeaderLabels(['Product', 'Die Description'])
        
        # Configurar la tabla
        header = self.productsTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Product
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Die Description
        
        self.productsTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.productsTable.setSelectionMode(QTableWidget.SingleSelection)
        self.productsTable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        contentLayout.addWidget(self.productsTable)
        mainLayout.addWidget(contentFrame)
        
        # Conectar señales
        self.addButton.clicked.connect(self.addProduct)
        self.editButton.clicked.connect(self.editProduct)
        self.deleteButton.clicked.connect(self.deleteProduct)
        
        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(800, 600)

    def loadProducts(self):
        """Carga los productos en la tabla"""
        self.productsTable.setRowCount(0)
        products_list = self.productModel.getAllProducts()
        
        for row, product in enumerate(products_list):
            self.productsTable.insertRow(row)
            # Almacenar el ID como datos del item pero mostrar solo el Product
            item_product = QTableWidgetItem(product['Product'])
            item_product.setData(Qt.UserRole, product['id_product'])
            self.productsTable.setItem(row, 0, item_product)
            
            # Mostrar la descripción del die
            item_die = QTableWidgetItem(product['DieDescription'])
            self.productsTable.setItem(row, 1, item_die)

    def getSelectedProductId(self):
        """Obtiene el ID del producto seleccionado"""
        selectedItems = self.productsTable.selectedItems()
        if not selectedItems:
            return None
        return self.productsTable.item(selectedItems[0].row(), 0).data(Qt.UserRole)

    def addProduct(self):
        """Abre el diálogo para agregar un nuevo producto"""
        dialog = ProductDialog(self)
        if dialog.exec_() == ProductDialog.Accepted:
            self.loadProducts()

    def editProduct(self):
        """Abre el diálogo para editar un producto existente"""
        product_id = self.getSelectedProductId()
        if not product_id:
            QMessageBox.warning(self, "Selection Required", "Please select a product to edit")
            return
            
        dialog = ProductDialog(self, product_id)
        if dialog.exec_() == ProductDialog.Accepted:
            self.loadProducts()

    def deleteProduct(self):
        """Elimina el producto seleccionado"""
        product_id = self.getSelectedProductId()
        if not product_id:
            QMessageBox.warning(self, "Selection Required", "Please select a product to delete")
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this product?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.productModel.deleteProduct(product_id):
                self.loadProducts()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete product") 