from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from models.worker_model import WorkerModel
from models.position_model import PositionModel
from database.database_schema import Columns
import os
from PyQt5.QtGui import QIcon

class WorkerDialog(QDialog):
    def __init__(self, parent=None, workerId=None):
        super().__init__(parent)
        self.workerId = workerId
        self.workerModel = WorkerModel()
        self.positionModel = PositionModel()
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
        
        self.setupUI()
        if workerId:
            self.loadWorker()
    
    def setupUI(self):
        self.setWindowTitle("Add Worker" if not self.workerId else "Edit Worker")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Campos de entrada
        formLayout = QVBoxLayout()
        
        # Nombre
        nameLayout = QHBoxLayout()
        nameLabel = QLabel("Name:")
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Enter worker name")
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameInput)
        formLayout.addLayout(nameLayout)
        
        # Posición
        positionLayout = QHBoxLayout()
        positionLabel = QLabel("Position:")
        self.positionCombo = QComboBox()
        self.loadPositions()
        positionLayout.addWidget(positionLabel)
        positionLayout.addWidget(self.positionCombo)
        formLayout.addLayout(positionLayout)
        
        layout.addLayout(formLayout)
        
        # Botones
        buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")
        
        self.saveButton.clicked.connect(self.saveWorker)
        self.cancelButton.clicked.connect(self.reject)
        
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonLayout)
        
        # Estilo
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                min-width: 200px;
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
            QPushButton[text="Cancel"] {
                background-color: #6c757d;
            }
            QPushButton[text="Cancel"]:hover {
                background-color: #545b62;
            }
            QLabel {
                min-width: 80px;
            }
        """)
        
        self.setMinimumWidth(400)
    
    def loadPositions(self):
        """Carga las posiciones en el combo"""
        positions = self.positionModel.getAllPositions()
        self.positionCombo.clear()
        self.positions = {}  # Para mantener la relación índice -> id
        
        for position in positions:
            self.positionCombo.addItem(position[Columns.Positions.POSITION])
            self.positions[self.positionCombo.count() - 1] = position[Columns.Positions.ID]
    
    def loadWorker(self):
        """Carga los datos del trabajador para edición"""
        worker = self.workerModel.getWorkerById(self.workerId)
        if worker:
            self.nameInput.setText(worker[Columns.Workers.NAME])
            # Seleccionar la posición correcta
            for index, positionId in self.positions.items():
                if positionId == worker[Columns.Workers.POSITION_ID]:
                    self.positionCombo.setCurrentIndex(index)
                    break
    
    def validateInputs(self):
        """Valida los campos del formulario"""
        if not self.nameInput.text().strip():
            QMessageBox.warning(self, "Validation Error", "Worker name is required")
            return False
        return True
    
    def saveWorker(self):
        """Guarda o actualiza el trabajador"""
        if not self.validateInputs():
            return
        
        name = self.nameInput.text().strip()
        positionId = self.positions[self.positionCombo.currentIndex()]
        
        success = False
        if self.workerId:
            # Actualizar trabajador existente
            success = self.workerModel.updateWorker(
                self.workerId,
                name,
                positionId
            )
        else:
            # Crear nuevo trabajador
            success = self.workerModel.createWorker(
                name,
                positionId
            )
        
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to save worker") 