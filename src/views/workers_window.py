from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSpacerItem, QSizePolicy, QMessageBox, QMainWindow, QDialog)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from models.worker_model import WorkerModel
from views.worker_dialog import WorkerDialog

class WorkersWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.workerModel = WorkerModel()
        self.setupUI()
        self.loadWorkers()
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
    
    def setupUI(self):
        self.setWindowTitle("Workers Management")
        
        # Widget central
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)
        
        # Frame superior para el título y logo
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
        titleLabel = QLabel("Workers Management")
        titleLabel.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        topLayout.addWidget(titleLabel)
        
        # Agregar espaciador entre el título y el logo
        topLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Logo
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
            QTableWidget {
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 5px;
                border: 1px solid #dee2e6;
                font-weight: bold;
            }
            QPushButton {
                background-color: #0056b3;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 3px;
                min-width: 100px;
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
        """)
        contentLayout = QVBoxLayout(contentFrame)
        contentLayout.setContentsMargins(10, 10, 10, 10)
        
        # Barra de herramientas
        toolbarLayout = QHBoxLayout()
        
        # Botones de acción
        self.addButton = QPushButton("Add Worker")
        self.addButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'add_icon.png')))
        self.addButton.clicked.connect(self.showAddWorkerDialog)
        
        self.editButton = QPushButton("Edit")
        self.editButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'edit_icon.png')))
        self.editButton.clicked.connect(self.editSelectedWorker)
        
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'delete_icon.png')))
        self.deleteButton.clicked.connect(self.deleteSelectedWorker)
        
        # Agregar espaciador y botones
        toolbarLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        toolbarLayout.addWidget(self.addButton)
        toolbarLayout.addWidget(self.editButton)
        toolbarLayout.addWidget(self.deleteButton)
        
        contentLayout.addLayout(toolbarLayout)
        
        # Tabla de trabajadores
        self.workersTable = QTableWidget()
        self.workersTable.setColumnCount(3)  # Reducido a 3 columnas
        self.workersTable.setHorizontalHeaderLabels(["Name", "Position", "Created"])
        self.workersTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.workersTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.workersTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.workersTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.workersTable.setSelectionMode(QTableWidget.SingleSelection)
        self.workersTable.setEditTriggers(QTableWidget.NoEditTriggers)
        contentLayout.addWidget(self.workersTable)
        
        mainLayout.addWidget(contentFrame)
        
        self.setMinimumSize(1000, 600)
    
    def loadWorkers(self):
        """Carga los trabajadores en la tabla"""
        self.workersTable.setRowCount(0)
        workers = self.workerModel.getAllWorkers()
        
        # Diccionario para mantener la relación entre filas e IDs
        self.workerIds = {}
        
        for row, worker in enumerate(workers):
            self.workersTable.insertRow(row)
            
            # Nombre
            self.workersTable.setItem(row, 0, QTableWidgetItem(worker['Name']))
            
            # Posición
            position = worker['position_name'] if worker['position_name'] else 'No Position'
            self.workersTable.setItem(row, 1, QTableWidgetItem(position))
            
            # Fecha de creación
            create_time = worker['create_time'].strftime('%Y-%m-%d %H:%M:%S') if worker['create_time'] else ''
            self.workersTable.setItem(row, 2, QTableWidgetItem(create_time))
            
            # Guardar el ID del trabajador
            self.workerIds[row] = worker['idWorkers']
    
    def showAddWorkerDialog(self):
        """Muestra el diálogo para agregar un trabajador"""
        dialog = WorkerDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.loadWorkers()
    
    def showEditWorkerDialog(self, workerId):
        """Muestra el diálogo para editar un trabajador"""
        dialog = WorkerDialog(self, workerId)
        if dialog.exec_() == QDialog.Accepted:
            self.loadWorkers()
    
    def deleteWorker(self, workerId):
        """Elimina un trabajador"""
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this worker?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.workerModel.deleteWorker(workerId):
                self.loadWorkers()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete worker")

    def getSelectedWorkerId(self):
        """Obtiene el ID del trabajador seleccionado"""
        selectedItems = self.workersTable.selectedItems()
        if not selectedItems:
            return None
        row = selectedItems[0].row()
        return self.workerIds.get(row)

    def editSelectedWorker(self):
        """Edita el trabajador seleccionado"""
        workerId = self.getSelectedWorkerId()
        if not workerId:
            QMessageBox.warning(self, "Selection Required", "Please select a worker to edit")
            return
        self.showEditWorkerDialog(workerId)

    def deleteSelectedWorker(self):
        """Elimina el trabajador seleccionado"""
        workerId = self.getSelectedWorkerId()
        if not workerId:
            QMessageBox.warning(self, "Selection Required", "Please select a worker to delete")
            return
        self.deleteWorker(workerId) 