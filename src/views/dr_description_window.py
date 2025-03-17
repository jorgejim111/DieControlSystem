from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from models.dr_description_model import DRDescriptionModel
from database.database_schema import Columns

class DRDescriptionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DR Description Management")
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.descriptionModel = DRDescriptionModel()
        self.setupUI()
        self.loadDescriptions()
        
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
        titleLabel = QLabel("DR Description Management")
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
        self.addButton = QPushButton("Add Description")
        self.editButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.setObjectName("deleteButton")
        
        toolbar.addWidget(self.addButton)
        toolbar.addWidget(self.editButton)
        toolbar.addWidget(self.deleteButton)
        
        contentLayout.addLayout(toolbar)
        
        # Tabla de descripciones
        self.descriptionTable = QTableWidget()
        self.descriptionTable.setColumnCount(1)  # Solo una columna para Description
        self.descriptionTable.setHorizontalHeaderLabels(['Description'])
        
        # Configurar la tabla
        header = self.descriptionTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Description
        self.descriptionTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.descriptionTable.setSelectionMode(QTableWidget.SingleSelection)
        self.descriptionTable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        contentLayout.addWidget(self.descriptionTable)
        mainLayout.addWidget(contentFrame)
        
        # Conectar señales
        self.addButton.clicked.connect(self.addDescription)
        self.editButton.clicked.connect(self.editDescription)
        self.deleteButton.clicked.connect(self.deleteDescription)
        
        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(800, 600)
    
    def loadDescriptions(self):
        """Carga las descripciones en la tabla"""
        self.descriptionTable.setRowCount(0)
        descriptions = self.descriptionModel.getAllDescriptions()
        
        # Crear un diccionario para almacenar la relación entre descripción y su ID
        self.descriptionIds = {}
        
        for row, description in enumerate(descriptions):
            self.descriptionTable.insertRow(row)
            descriptionText = description[Columns.DRDescription.DESCRIPTION]
            self.descriptionTable.setItem(row, 0, QTableWidgetItem(descriptionText))
            # Guardar el ID asociado a esta descripción
            self.descriptionIds[row] = description[Columns.DRDescription.ID]
    
    def getSelectedDescriptionId(self):
        """Obtiene el ID de la descripción seleccionada"""
        selectedItems = self.descriptionTable.selectedItems()
        if not selectedItems:
            return None
        selectedRow = selectedItems[0].row()
        return self.descriptionIds[selectedRow]
        
    def addDescription(self):
        """Abre el diálogo para agregar una nueva descripción"""
        from .dr_description_dialog import DRDescriptionDialog
        dialog = DRDescriptionDialog(self)
        if dialog.exec_() == DRDescriptionDialog.Accepted:
            self.loadDescriptions()
        
    def editDescription(self):
        """Abre el diálogo para editar una descripción existente"""
        descriptionId = self.getSelectedDescriptionId()
        if not descriptionId:
            QMessageBox.warning(self, "Selection Required", "Please select a description to edit")
            return
            
        from .dr_description_dialog import DRDescriptionDialog
        dialog = DRDescriptionDialog(self, descriptionId)
        if dialog.exec_() == DRDescriptionDialog.Accepted:
            self.loadDescriptions()
        
    def deleteDescription(self):
        """Elimina la descripción seleccionada"""
        descriptionId = self.getSelectedDescriptionId()
        if not descriptionId:
            QMessageBox.warning(self, "Selection Required", "Please select a description to delete")
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this description?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.descriptionModel.deleteDescription(descriptionId):
                self.loadDescriptions()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete description") 