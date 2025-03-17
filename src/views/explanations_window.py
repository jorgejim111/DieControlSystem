from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from models.explanation_model import ExplanationModel
from database.database_schema import Columns

class ExplanationsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Explanations Management")
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.explanationModel = ExplanationModel()
        self.setupUI()
        self.loadExplanations()
        
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
        titleLabel = QLabel("Explanations Management")
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
        self.addButton = QPushButton("Add Explanation")
        self.editButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.setObjectName("deleteButton")
        
        toolbar.addWidget(self.addButton)
        toolbar.addWidget(self.editButton)
        toolbar.addWidget(self.deleteButton)
        
        contentLayout.addLayout(toolbar)
        
        # Tabla de explicaciones
        self.explanationsTable = QTableWidget()
        self.explanationsTable.setColumnCount(1)  # Solo una columna para Explanation
        self.explanationsTable.setHorizontalHeaderLabels(['Explanation'])
        
        # Configurar la tabla
        header = self.explanationsTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Explanation
        self.explanationsTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.explanationsTable.setSelectionMode(QTableWidget.SingleSelection)
        self.explanationsTable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        contentLayout.addWidget(self.explanationsTable)
        mainLayout.addWidget(contentFrame)
        
        # Conectar señales
        self.addButton.clicked.connect(self.addExplanation)
        self.editButton.clicked.connect(self.editExplanation)
        self.deleteButton.clicked.connect(self.deleteExplanation)
        
        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(800, 600)
    
    def loadExplanations(self):
        """Carga las explicaciones en la tabla"""
        self.explanationsTable.setRowCount(0)
        explanations = self.explanationModel.getAllExplanations()
        
        # Crear un diccionario para almacenar la relación entre explicación y su ID
        self.explanationIds = {}
        
        for row, explanation in enumerate(explanations):
            self.explanationsTable.insertRow(row)
            explanationText = explanation[Columns.Explanation.EXPLANATION]
            self.explanationsTable.setItem(row, 0, QTableWidgetItem(explanationText))
            # Guardar el ID asociado a esta explicación
            self.explanationIds[row] = explanation[Columns.Explanation.ID]
    
    def getSelectedExplanationId(self):
        """Obtiene el ID de la explicación seleccionada"""
        selectedItems = self.explanationsTable.selectedItems()
        if not selectedItems:
            return None
        selectedRow = selectedItems[0].row()
        return self.explanationIds[selectedRow]
        
    def addExplanation(self):
        """Abre el diálogo para agregar una nueva explicación"""
        from .explanation_dialog import ExplanationDialog
        dialog = ExplanationDialog(self)
        if dialog.exec_() == ExplanationDialog.Accepted:
            self.loadExplanations()
        
    def editExplanation(self):
        """Abre el diálogo para editar una explicación existente"""
        explanationId = self.getSelectedExplanationId()
        if not explanationId:
            QMessageBox.warning(self, "Selection Required", "Please select an explanation to edit")
            return
            
        from .explanation_dialog import ExplanationDialog
        dialog = ExplanationDialog(self, explanationId)
        if dialog.exec_() == ExplanationDialog.Accepted:
            self.loadExplanations()
        
    def deleteExplanation(self):
        """Elimina la explicación seleccionada"""
        explanationId = self.getSelectedExplanationId()
        if not explanationId:
            QMessageBox.warning(self, "Selection Required", "Please select an explanation to delete")
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this explanation?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.explanationModel.deleteExplanation(explanationId):
                self.loadExplanations()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete explanation") 