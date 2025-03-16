from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QMessageBox,
                            QComboBox)
from PyQt5.QtCore import Qt
from models.product_model import ProductModel

class ProductDialog(QDialog):
    def __init__(self, parent=None, product_id=None):
        """Inicializa el diálogo para agregar/editar productos

        Args:
            parent: Widget padre
            product_id (int, optional): ID del producto a editar
        """
        super().__init__(parent)
        self.product_id = product_id
        self.model = ProductModel()
        self.setupUI()
        
        if product_id:
            self.setWindowTitle("Edit Product")
            self.loadProductData()
        else:
            self.setWindowTitle("Add Product")

    def setupUI(self):
        """Configura la interfaz de usuario del diálogo"""
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
                color: #333333;
            }
            QPushButton {
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                color: white;
                min-width: 80px;
            }
            QPushButton#saveButton {
                background-color: #0056b3;
            }
            QPushButton#saveButton:hover {
                background-color: #003d80;
            }
            QPushButton#cancelButton {
                background-color: #6c757d;
            }
            QPushButton#cancelButton:hover {
                background-color: #5a6268;
            }
        """)

        # Layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Campo de entrada para Product
        inputLayout = QHBoxLayout()
        productLabel = QLabel("Product:")
        productLabel.setFixedWidth(120)
        self.productInput = QLineEdit()
        self.productInput.setMaxLength(100)  # Limitar a 100 caracteres
        inputLayout.addWidget(productLabel)
        inputLayout.addWidget(self.productInput)
        layout.addLayout(inputLayout)

        # ComboBox para Die Description
        dieLayout = QHBoxLayout()
        dieLabel = QLabel("Die Description:")
        dieLabel.setFixedWidth(120)
        self.dieCombo = QComboBox()
        self.loadDieDescriptions()
        dieLayout.addWidget(dieLabel)
        dieLayout.addWidget(self.dieCombo)
        layout.addLayout(dieLayout)

        # Botones
        buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.saveButton.setObjectName("saveButton")
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setObjectName("cancelButton")
        
        self.saveButton.clicked.connect(self.saveProduct)
        self.cancelButton.clicked.connect(self.reject)
        
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonLayout)

        # Configurar el tamaño del diálogo
        self.setMinimumWidth(400)
        self.setMaximumHeight(200)

    def loadDieDescriptions(self):
        """Carga las descripciones de dies en el ComboBox"""
        die_descriptions = self.model.getAllDieDescriptions()
        self.dieCombo.clear()
        
        for die in die_descriptions:
            self.dieCombo.addItem(die['Description'], die['id_die_description'])

    def loadProductData(self):
        """Carga los datos del producto si se está editando"""
        product_data = self.model.getProductById(self.product_id)
        if product_data:
            self.productInput.setText(product_data['Product'])
            
            # Seleccionar el die description correcto en el combo
            index = self.dieCombo.findData(product_data['id_die_description'])
            if index >= 0:
                self.dieCombo.setCurrentIndex(index)

    def saveProduct(self):
        """Guarda o actualiza el producto en la base de datos"""
        product_name = self.productInput.text().strip()
        die_description_id = self.dieCombo.currentData()
        
        if not product_name:
            QMessageBox.warning(self, "Validation Error", "Product name cannot be empty")
            return
            
        if die_description_id is None:
            QMessageBox.warning(self, "Validation Error", "Please select a die description")
            return
            
        success = False
        if self.product_id:
            # Actualizar producto existente
            success = self.model.updateProduct(self.product_id, product_name, die_description_id)
        else:
            # Crear nuevo producto
            success = self.model.createProduct(product_name, die_description_id)
            
        if success:
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Could not save product. Please check if a similar one already exists."
            ) 