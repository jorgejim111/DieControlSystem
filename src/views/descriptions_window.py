from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from models.description_model import DescriptionModel
from views.description_dialog import DescriptionDialog

class DescriptionsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Descriptions Management")
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.description_model = DescriptionModel()
        self.setupUI()
        self.load_descriptions()
        
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
        titleLabel = QLabel("Descriptions Management")
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
        
        # Tabla de descriptions
        self.descriptionsTable = QTableWidget()
        self.descriptionsTable.setColumnCount(2)
        self.descriptionsTable.setHorizontalHeaderLabels(['ID', 'Description'])
        
        # Configurar la tabla
        header = self.descriptionsTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.descriptionsTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.descriptionsTable.setSelectionMode(QTableWidget.SingleSelection)
        self.descriptionsTable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        contentLayout.addWidget(self.descriptionsTable)
        mainLayout.addWidget(contentFrame)
        
        # Conectar señales
        self.addButton.clicked.connect(self.show_add_dialog)
        self.editButton.clicked.connect(self.edit_selected)
        self.deleteButton.clicked.connect(self.delete_selected)
        
        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(800, 600)

    def load_descriptions(self):
        """Carga las descriptions en la tabla"""
        self.descriptionsTable.setRowCount(0)
        descriptions = self.description_model.get_all_descriptions()
        
        # Crear un diccionario para almacenar la relación entre description y su ID
        self.description_ids = {}
        
        for row, description in enumerate(descriptions):
            self.descriptionsTable.insertRow(row)
            
            # ID
            id_item = QTableWidgetItem(str(description['id_description']))
            self.descriptionsTable.setItem(row, 0, id_item)
            
            # Description
            description_item = QTableWidgetItem(description['Description'])
            self.descriptionsTable.setItem(row, 1, description_item)
            
            # Guardar el ID asociado a esta description
            self.description_ids[row] = description['id_description']

    def get_selected_description_id(self):
        """Obtiene el ID de la description seleccionada"""
        selectedItems = self.descriptionsTable.selectedItems()
        if not selectedItems:
            return None
        selectedRow = selectedItems[0].row()
        return self.description_ids[selectedRow]

    def show_add_dialog(self):
        """Muestra el diálogo para agregar una nueva description"""
        dialog = DescriptionDialog(self)
        if dialog.exec_() == DescriptionDialog.Accepted:
            self.load_descriptions()

    def edit_selected(self):
        """Edita la description seleccionada"""
        description_id = self.get_selected_description_id()
        if not description_id:
            QMessageBox.warning(self, "Selection Required", "Please select a description to edit")
            return
            
        # Obtener los datos de la description
        descriptions = self.description_model.get_all_descriptions()
        description_data = next((desc for desc in descriptions if desc['id_description'] == description_id), None)
        
        if description_data:
            dialog = DescriptionDialog(self, description_data)
            if dialog.exec_() == DescriptionDialog.Accepted:
                self.load_descriptions()

    def delete_selected(self):
        """Elimina la description seleccionada"""
        description_id = self.get_selected_description_id()
        if not description_id:
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
            if self.description_model.delete_description(description_id):
                self.load_descriptions()
                QMessageBox.information(self, "Success", "Description deleted successfully!")
            else:
                QMessageBox.critical(self, "Error", "Could not delete the description.") 