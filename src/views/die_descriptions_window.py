from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from models.die_description_model import DieDescriptionModel
from views.die_description_dialog import DieDescriptionDialog

class DieDescriptionsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Die Descriptions Management")
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.die_description_model = DieDescriptionModel()
        self.setupUI()
        self.load_die_descriptions()
        
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
        titleLabel = QLabel("Die Descriptions Management")
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
        self.addButton = QPushButton("Add Die Description")
        self.editButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.setObjectName("deleteButton")
        
        toolbar.addWidget(self.addButton)
        toolbar.addWidget(self.editButton)
        toolbar.addWidget(self.deleteButton)
        
        contentLayout.addLayout(toolbar)
        
        # Tabla de die descriptions
        self.dieDescriptionsTable = QTableWidget()
        self.dieDescriptionsTable.setColumnCount(8)
        self.dieDescriptionsTable.setHorizontalHeaderLabels([
            'Die Description', 'Inch', 'Part', 'Description',
            'Obsolet', 'Circulation', 'New', 'Last Update'
        ])
        
        # Configurar la tabla
        header = self.dieDescriptionsTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)          # Die Description
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Inch
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Part
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Description
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Obsolet
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Circulation
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # New
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Last Update
        
        self.dieDescriptionsTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.dieDescriptionsTable.setSelectionMode(QTableWidget.SingleSelection)
        self.dieDescriptionsTable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        contentLayout.addWidget(self.dieDescriptionsTable)
        mainLayout.addWidget(contentFrame)
        
        # Conectar señales
        self.addButton.clicked.connect(self.show_add_dialog)
        self.editButton.clicked.connect(self.edit_selected)
        self.deleteButton.clicked.connect(self.delete_selected)
        
        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(1000, 600)

    def load_die_descriptions(self):
        """Carga las die descriptions en la tabla"""
        self.dieDescriptionsTable.setRowCount(0)
        die_descriptions = self.die_description_model.get_all_die_descriptions()
        
        # Crear un diccionario para almacenar la relación entre die description y su ID
        self.die_description_ids = {}
        
        for row, die_description in enumerate(die_descriptions):
            self.dieDescriptionsTable.insertRow(row)
            
            # Die Description
            description_item = QTableWidgetItem(die_description['Die_Description'])
            self.dieDescriptionsTable.setItem(row, 0, description_item)
            
            # Inch
            inch_item = QTableWidgetItem(die_description['Inch'])
            self.dieDescriptionsTable.setItem(row, 1, inch_item)
            
            # Part
            part_item = QTableWidgetItem(die_description['Part'])
            self.dieDescriptionsTable.setItem(row, 2, part_item)
            
            # Description
            desc_item = QTableWidgetItem(die_description['Description'])
            self.dieDescriptionsTable.setItem(row, 3, desc_item)
            
            # Obsolet
            obsolet_item = QTableWidgetItem('Yes' if die_description['Obsolet'] else 'No')
            self.dieDescriptionsTable.setItem(row, 4, obsolet_item)
            
            # Circulation
            circulation_item = QTableWidgetItem(str(die_description['Circulation']))
            self.dieDescriptionsTable.setItem(row, 5, circulation_item)
            
            # New
            new_item = QTableWidgetItem(str(die_description['New']))
            self.dieDescriptionsTable.setItem(row, 6, new_item)
            
            # Last Update
            update_item = QTableWidgetItem(str(die_description['updat_time']))
            self.dieDescriptionsTable.setItem(row, 7, update_item)
            
            # Guardar el ID asociado a esta die description
            self.die_description_ids[row] = die_description['id_die_description']

    def get_selected_die_description_id(self):
        """Obtiene el ID de la die description seleccionada"""
        selectedItems = self.dieDescriptionsTable.selectedItems()
        if not selectedItems:
            return None
        selectedRow = selectedItems[0].row()
        return self.die_description_ids[selectedRow]

    def show_add_dialog(self):
        """Muestra el diálogo para agregar una nueva die description"""
        dialog = DieDescriptionDialog(self)
        if dialog.exec_() == DieDescriptionDialog.Accepted:
            self.load_die_descriptions()

    def edit_selected(self):
        """Edita la die description seleccionada"""
        die_description_id = self.get_selected_die_description_id()
        if not die_description_id:
            QMessageBox.warning(self, "Selection Required", "Please select a die description to edit")
            return
            
        # Obtener los datos de la die description
        die_description_data = self.die_description_model.get_die_description_by_id(die_description_id)
        
        if die_description_data:
            dialog = DieDescriptionDialog(self, die_description_data)
            if dialog.exec_() == DieDescriptionDialog.Accepted:
                self.load_die_descriptions()

    def delete_selected(self):
        """Elimina la die description seleccionada"""
        die_description_id = self.get_selected_die_description_id()
        if not die_description_id:
            QMessageBox.warning(self, "Selection Required", "Please select a die description to delete")
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this die description?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.die_description_model.delete_die_description(die_description_id):
                self.load_die_descriptions()
                QMessageBox.information(self, "Success", "Die description deleted successfully!")
            else:
                QMessageBox.critical(self, "Error", "Could not delete the die description.") 