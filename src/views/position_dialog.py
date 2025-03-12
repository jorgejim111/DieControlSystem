from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from models.position_model import PositionModel
from database.database_schema import Columns
import os
from PyQt5.QtGui import QIcon

class PositionDialog(QDialog):
    def __init__(self, parent=None, positionId=None):
        super().__init__(parent)
        self.positionId = positionId
        self.positionModel = PositionModel()
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.setupUI()
        if positionId:
            self.loadPosition()
    
    def setupUI(self):
        self.setWindowTitle("Add Position" if not self.positionId else "Edit Position")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Campos de entrada
        formLayout = QVBoxLayout()
        
        # Position Name
        nameLayout = QHBoxLayout()
        nameLabel = QLabel("Position:")
        self.nameInput = QLineEdit()
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameInput)
        formLayout.addLayout(nameLayout)
        
        layout.addLayout(formLayout)
        
        # Botones
        buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")
        
        self.saveButton.clicked.connect(self.savePosition)
        self.cancelButton.clicked.connect(self.reject)
        
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonLayout)
        
        # Estilo
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLineEdit {
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
        """)
        
        self.setMinimumWidth(400)
    
    def loadPosition(self):
        position = self.positionModel.getPositionById(self.positionId)
        if position:
            self.nameInput.setText(position[Columns.Positions.POSITION])
    
    def validateInputs(self):
        if not self.nameInput.text().strip():
            QMessageBox.warning(self, "Validation Error", "Position name is required")
            return False
        return True
    
    def savePosition(self):
        if not self.validateInputs():
            return
        
        positionName = self.nameInput.text().strip()
        
        success = False
        if self.positionId:
            # Actualizar posición existente
            success = self.positionModel.updatePosition(
                self.positionId,
                positionName
            )
        else:
            # Crear nueva posición
            success = self.positionModel.createPosition(positionName)
        
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to save position") 