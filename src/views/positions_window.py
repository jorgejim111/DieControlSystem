from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from models.position_model import PositionModel
from database.database_schema import Columns

class PositionsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Positions Management")
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.positionModel = PositionModel()
        self.setupUI()
        self.loadPositions()
        
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
        titleLabel = QLabel("Positions Management")
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
        self.addButton = QPushButton("Add Position")
        self.editButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.setObjectName("deleteButton")
        
        toolbar.addWidget(self.addButton)
        toolbar.addWidget(self.editButton)
        toolbar.addWidget(self.deleteButton)
        
        contentLayout.addLayout(toolbar)
        
        # Tabla de posiciones
        self.positionsTable = QTableWidget()
        self.positionsTable.setColumnCount(1)  # Solo una columna para Position
        self.positionsTable.setHorizontalHeaderLabels(['Position'])
        
        # Configurar la tabla
        header = self.positionsTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Position
        self.positionsTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.positionsTable.setSelectionMode(QTableWidget.SingleSelection)
        self.positionsTable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        contentLayout.addWidget(self.positionsTable)
        mainLayout.addWidget(contentFrame)
        
        # Conectar señales
        self.addButton.clicked.connect(self.addPosition)
        self.editButton.clicked.connect(self.editPosition)
        self.deleteButton.clicked.connect(self.deletePosition)
        
        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(800, 600)
    
    def loadPositions(self):
        """Carga las posiciones en la tabla"""
        self.positionsTable.setRowCount(0)
        positions = self.positionModel.getAllPositions()  # Ya viene ordenado por position
        
        # Crear un diccionario para almacenar la relación entre posición y su ID
        self.positionIds = {}
        
        for row, position in enumerate(positions):
            self.positionsTable.insertRow(row)
            positionName = position[Columns.Positions.POSITION]
            self.positionsTable.setItem(row, 0, QTableWidgetItem(positionName))
            # Guardar el ID asociado a esta posición
            self.positionIds[row] = position[Columns.Positions.ID]
    
    def getSelectedPositionId(self):
        """Obtiene el ID de la posición seleccionada"""
        selectedItems = self.positionsTable.selectedItems()
        if not selectedItems:
            return None
        selectedRow = selectedItems[0].row()
        return self.positionIds[selectedRow]
        
    def addPosition(self):
        """Abre el diálogo para agregar una nueva posición"""
        from .position_dialog import PositionDialog
        dialog = PositionDialog(self)
        if dialog.exec_() == PositionDialog.Accepted:
            self.loadPositions()
        
    def editPosition(self):
        """Abre el diálogo para editar una posición existente"""
        positionId = self.getSelectedPositionId()
        if not positionId:
            QMessageBox.warning(self, "Selection Required", "Please select a position to edit")
            return
            
        from .position_dialog import PositionDialog
        dialog = PositionDialog(self, positionId)
        if dialog.exec_() == PositionDialog.Accepted:
            self.loadPositions()
        
    def deletePosition(self):
        """Elimina la posición seleccionada"""
        positionId = self.getSelectedPositionId()
        if not positionId:
            QMessageBox.warning(self, "Selection Required", "Please select a position to delete")
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this position?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.positionModel.deletePosition(positionId):
                self.loadPositions()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete position") 