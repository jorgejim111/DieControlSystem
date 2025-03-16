from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from models.inch_model import InchModel
from views.inch_dialog import InchDialog

class InchesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inches Management")
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.inch_model = InchModel()
        self.setupUI()
        self.load_inches()
        
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
        titleLabel = QLabel("Inches Management")
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
        self.addButton = QPushButton("Add Inch")
        self.editButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.setObjectName("deleteButton")
        
        toolbar.addWidget(self.addButton)
        toolbar.addWidget(self.editButton)
        toolbar.addWidget(self.deleteButton)
        
        contentLayout.addLayout(toolbar)
        
        # Tabla de pulgadas
        self.inchesTable = QTableWidget()
        self.inchesTable.setColumnCount(2)
        self.inchesTable.setHorizontalHeaderLabels(['ID', 'Inch'])
        
        # Configurar la tabla
        header = self.inchesTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.inchesTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.inchesTable.setSelectionMode(QTableWidget.SingleSelection)
        self.inchesTable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        contentLayout.addWidget(self.inchesTable)
        mainLayout.addWidget(contentFrame)
        
        # Conectar señales
        self.addButton.clicked.connect(self.show_add_dialog)
        self.editButton.clicked.connect(self.edit_selected)
        self.deleteButton.clicked.connect(self.delete_selected)
        
        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(800, 600)

    def load_inches(self):
        """Carga las pulgadas en la tabla"""
        self.inchesTable.setRowCount(0)
        inches = self.inch_model.get_all_inches()
        
        # Crear un diccionario para almacenar la relación entre pulgada y su ID
        self.inch_ids = {}
        
        for row, inch in enumerate(inches):
            self.inchesTable.insertRow(row)
            
            # ID
            id_item = QTableWidgetItem(str(inch['id_inch']))
            self.inchesTable.setItem(row, 0, id_item)
            
            # Pulgada
            inch_item = QTableWidgetItem(inch['Inch'])
            self.inchesTable.setItem(row, 1, inch_item)
            
            # Guardar el ID asociado a esta pulgada
            self.inch_ids[row] = inch['id_inch']

    def get_selected_inch_id(self):
        """Obtiene el ID de la pulgada seleccionada"""
        selectedItems = self.inchesTable.selectedItems()
        if not selectedItems:
            return None
        selectedRow = selectedItems[0].row()
        return self.inch_ids[selectedRow]

    def show_add_dialog(self):
        """Muestra el diálogo para agregar una nueva pulgada"""
        dialog = InchDialog(self)
        if dialog.exec_() == InchDialog.Accepted:
            self.load_inches()

    def edit_selected(self):
        """Edita la pulgada seleccionada"""
        inch_id = self.get_selected_inch_id()
        if not inch_id:
            QMessageBox.warning(self, "Selection Required", "Please select an inch to edit")
            return
            
        # Obtener los datos de la pulgada
        inches = self.inch_model.get_all_inches()
        inch_data = next((inch for inch in inches if inch['id_inch'] == inch_id), None)
        
        if inch_data:
            dialog = InchDialog(self, inch_data)
            if dialog.exec_() == InchDialog.Accepted:
                self.load_inches()

    def delete_selected(self):
        """Elimina la pulgada seleccionada"""
        inch_id = self.get_selected_inch_id()
        if not inch_id:
            QMessageBox.warning(self, "Selection Required", "Please select an inch to delete")
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this inch?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.inch_model.delete_inch(inch_id):
                self.load_inches()
                QMessageBox.information(self, "Success", "Inch deleted successfully!")
            else:
                QMessageBox.critical(self, "Error", "Could not delete the inch.") 