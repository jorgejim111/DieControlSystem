from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from models.serial_model import SerialModel
from views.dialogs.serial_dialog import SerialDialog

class SerialWindow(QWidget):
    def __init__(self):
        """Inicializa la ventana de serials"""
        super().__init__()
        self.setWindowTitle("Serials Management")
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.model = SerialModel()
        self.setupUi()
        self.loadData()
        
    def setupUi(self):
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
        titleLabel = QLabel("Serials Management")
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
        self.addButton = QPushButton("Add Serial")
        self.editButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.setObjectName("deleteButton")
        
        toolbar.addWidget(self.addButton)
        toolbar.addWidget(self.editButton)
        toolbar.addWidget(self.deleteButton)
        
        contentLayout.addLayout(toolbar)
        
        # Tabla de serials
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Serial", "Die Description", "Inner", "Outer", "Status", "ID Die"
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Ajustar columnas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Serial
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Die Description
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Inner
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Outer
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # ID Die
        
        contentLayout.addWidget(self.table)
        mainLayout.addWidget(contentFrame)
        
        # Ocultar columnas de IDs
        self.table.setColumnHidden(0, True)  # ID Serial
        self.table.setColumnHidden(6, True)  # ID Die
        
        # Conectar señales
        self.addButton.clicked.connect(self.addSerial)
        self.editButton.clicked.connect(self.editSerial)
        self.deleteButton.clicked.connect(self.deleteSerial)
        
        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(800, 600)

    def loadData(self):
        """Carga los datos en la tabla"""
        self.table.setRowCount(0)
        serials = self.model.getAllSerials()
        
        for i, serial in enumerate(serials):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(serial['id_serial'])))
            self.table.setItem(i, 1, QTableWidgetItem(serial['Serial']))
            self.table.setItem(i, 2, QTableWidgetItem(serial['DieDescription']))
            self.table.setItem(i, 3, QTableWidgetItem(str(serial['inner'])))
            self.table.setItem(i, 4, QTableWidgetItem(str(serial['outer'])))
            self.table.setItem(i, 5, QTableWidgetItem(serial['StatusName']))
            self.table.setItem(i, 6, QTableWidgetItem(str(serial['id_die_description'])))

    def addSerial(self):
        """Abre el diálogo para agregar un nuevo serial"""
        dialog = SerialDialog(self)
        if dialog.exec_():
            self.loadData()

    def editSerial(self):
        """Abre el diálogo para editar el serial seleccionado"""
        selectedItems = self.table.selectedItems()
        if not selectedItems:
            QMessageBox.warning(self, "Selection Required", "Please select a serial to edit")
            return
            
        currentRow = self.table.currentRow()
        serialId = int(self.table.item(currentRow, 0).text())
        dialog = SerialDialog(self, serialId)
        if dialog.exec_():
            self.loadData()

    def deleteSerial(self):
        """Elimina el serial seleccionado"""
        selectedItems = self.table.selectedItems()
        if not selectedItems:
            QMessageBox.warning(self, "Selection Required", "Please select a serial to delete")
            return
            
        currentRow = self.table.currentRow()
        serialId = int(self.table.item(currentRow, 0).text())
        serialNumber = self.table.item(currentRow, 1).text()
        
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete serial {serialNumber}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.model.deleteSerial(serialId):
                self.loadData()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete serial") 