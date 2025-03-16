from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from models.part_model import PartModel
from views.part_dialog import PartDialog

class PartsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parts Management")
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.part_model = PartModel()
        self.setupUI()
        self.load_parts()
        
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
        titleLabel = QLabel("Parts Management")
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
        self.addButton = QPushButton("Add Part")
        self.editButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.setObjectName("deleteButton")
        
        toolbar.addWidget(self.addButton)
        toolbar.addWidget(self.editButton)
        toolbar.addWidget(self.deleteButton)
        
        contentLayout.addLayout(toolbar)
        
        # Tabla de parts
        self.partsTable = QTableWidget()
        self.partsTable.setColumnCount(2)
        self.partsTable.setHorizontalHeaderLabels(['ID', 'Part'])
        
        # Configurar la tabla
        header = self.partsTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.partsTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.partsTable.setSelectionMode(QTableWidget.SingleSelection)
        self.partsTable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        contentLayout.addWidget(self.partsTable)
        mainLayout.addWidget(contentFrame)
        
        # Conectar señales
        self.addButton.clicked.connect(self.show_add_dialog)
        self.editButton.clicked.connect(self.edit_selected)
        self.deleteButton.clicked.connect(self.delete_selected)
        
        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(800, 600)

    def load_parts(self):
        """Carga las parts en la tabla"""
        self.partsTable.setRowCount(0)
        parts = self.part_model.get_all_parts()
        
        # Crear un diccionario para almacenar la relación entre part y su ID
        self.part_ids = {}
        
        for row, part in enumerate(parts):
            self.partsTable.insertRow(row)
            
            # ID
            id_item = QTableWidgetItem(str(part['id_part']))
            self.partsTable.setItem(row, 0, id_item)
            
            # Part
            part_item = QTableWidgetItem(part['Part'])
            self.partsTable.setItem(row, 1, part_item)
            
            # Guardar el ID asociado a esta part
            self.part_ids[row] = part['id_part']

    def get_selected_part_id(self):
        """Obtiene el ID de la part seleccionada"""
        selectedItems = self.partsTable.selectedItems()
        if not selectedItems:
            return None
        selectedRow = selectedItems[0].row()
        return self.part_ids[selectedRow]

    def show_add_dialog(self):
        """Muestra el diálogo para agregar una nueva part"""
        dialog = PartDialog(self)
        if dialog.exec_() == PartDialog.Accepted:
            self.load_parts()

    def edit_selected(self):
        """Edita la part seleccionada"""
        part_id = self.get_selected_part_id()
        if not part_id:
            QMessageBox.warning(self, "Selection Required", "Please select a part to edit")
            return
            
        # Obtener los datos de la part
        parts = self.part_model.get_all_parts()
        part_data = next((part for part in parts if part['id_part'] == part_id), None)
        
        if part_data:
            dialog = PartDialog(self, part_data)
            if dialog.exec_() == PartDialog.Accepted:
                self.load_parts()

    def delete_selected(self):
        """Elimina la part seleccionada"""
        part_id = self.get_selected_part_id()
        if not part_id:
            QMessageBox.warning(self, "Selection Required", "Please select a part to delete")
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this part?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.part_model.delete_part(part_id):
                self.load_parts()
                QMessageBox.information(self, "Success", "Part deleted successfully!")
            else:
                QMessageBox.critical(self, "Error", "Could not delete the part.") 