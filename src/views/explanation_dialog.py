from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from models.explanation_model import ExplanationModel
from database.database_schema import Columns
import os
from PyQt5.QtGui import QIcon

class ExplanationDialog(QDialog):
    def __init__(self, parent=None, explanationId=None):
        super().__init__(parent)
        self.explanationId = explanationId
        self.explanationModel = ExplanationModel()
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.setupUI()
        if explanationId:
            self.loadExplanation()
    
    def setupUI(self):
        self.setWindowTitle("Add Explanation" if not self.explanationId else "Edit Explanation")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Campos de entrada
        formLayout = QVBoxLayout()
        
        # Explanation Text
        nameLayout = QHBoxLayout()
        nameLabel = QLabel("Explanation:")
        self.nameInput = QLineEdit()
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameInput)
        formLayout.addLayout(nameLayout)
        
        layout.addLayout(formLayout)
        
        # Botones
        buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")
        
        self.saveButton.clicked.connect(self.saveExplanation)
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
    
    def loadExplanation(self):
        explanation = self.explanationModel.getExplanationById(self.explanationId)
        if explanation:
            self.nameInput.setText(explanation[Columns.Explanation.EXPLANATION])
    
    def validateInputs(self):
        if not self.nameInput.text().strip():
            QMessageBox.warning(self, "Validation Error", "Explanation text is required")
            return False
        return True
    
    def saveExplanation(self):
        if not self.validateInputs():
            return
        
        explanationText = self.nameInput.text().strip()
        
        success = False
        if self.explanationId:
            # Actualizar explicación existente
            success = self.explanationModel.updateExplanation(
                self.explanationId,
                explanationText
            )
        else:
            # Crear nueva explicación
            success = self.explanationModel.createExplanation(explanationText)
        
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to save explanation") 