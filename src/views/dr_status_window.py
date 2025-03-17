from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from models.dr_status_model import DRStatusModel
from database.database_schema import Columns

class DRStatusWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DR Status Management")
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.statusModel = DRStatusModel()
        self.setupUI()
        self.loadStatus()
        
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
        titleLabel = QLabel("DR Status Management")
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
        self.addButton = QPushButton("Add Status")
        self.editButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.setObjectName("deleteButton")
        
        toolbar.addWidget(self.addButton)
        toolbar.addWidget(self.editButton)
        toolbar.addWidget(self.deleteButton)
        
        contentLayout.addLayout(toolbar)
        
        # Tabla de estados
        self.statusTable = QTableWidget()
        self.statusTable.setColumnCount(1)  # Solo una columna para Status
        self.statusTable.setHorizontalHeaderLabels(['Status'])
        
        # Configurar la tabla
        header = self.statusTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Status
        self.statusTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.statusTable.setSelectionMode(QTableWidget.SingleSelection)
        self.statusTable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        contentLayout.addWidget(self.statusTable)
        mainLayout.addWidget(contentFrame)
        
        # Conectar señales
        self.addButton.clicked.connect(self.addStatus)
        self.editButton.clicked.connect(self.editStatus)
        self.deleteButton.clicked.connect(self.deleteStatus)
        
        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(800, 600)
    
    def loadStatus(self):
        """Carga los estados en la tabla"""
        self.statusTable.setRowCount(0)
        status_list = self.statusModel.getAllStatus()
        
        # Crear un diccionario para almacenar la relación entre estado y su ID
        self.statusIds = {}
        
        for row, status in enumerate(status_list):
            self.statusTable.insertRow(row)
            statusText = status[Columns.DRStatus.STATUS]
            self.statusTable.setItem(row, 0, QTableWidgetItem(statusText))
            # Guardar el ID asociado a este estado
            self.statusIds[row] = status[Columns.DRStatus.ID]
    
    def getSelectedStatusId(self):
        """Obtiene el ID del estado seleccionado"""
        selectedItems = self.statusTable.selectedItems()
        if not selectedItems:
            return None
        selectedRow = selectedItems[0].row()
        return self.statusIds[selectedRow]
        
    def addStatus(self):
        """Abre el diálogo para agregar un nuevo estado"""
        from .dr_status_dialog import DRStatusDialog
        dialog = DRStatusDialog(self)
        if dialog.exec_() == DRStatusDialog.Accepted:
            self.loadStatus()
        
    def editStatus(self):
        """Abre el diálogo para editar un estado existente"""
        statusId = self.getSelectedStatusId()
        if not statusId:
            QMessageBox.warning(self, "Selection Required", "Please select a status to edit")
            return
            
        from .dr_status_dialog import DRStatusDialog
        dialog = DRStatusDialog(self, statusId)
        if dialog.exec_() == DRStatusDialog.Accepted:
            self.loadStatus()
        
    def deleteStatus(self):
        """Elimina el estado seleccionado"""
        statusId = self.getSelectedStatusId()
        if not statusId:
            QMessageBox.warning(self, "Selection Required", "Please select a status to delete")
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this status?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.statusModel.deleteStatus(statusId):
                self.loadStatus()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete status") 