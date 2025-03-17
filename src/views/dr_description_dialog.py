from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from models.dr_description_model import DRDescriptionModel
from database.database_schema import Columns
import os
from PyQt5.QtGui import QIcon

class DRDescriptionDialog(QDialog):
    def __init__(self, parent=None, descriptionId=None):
        """Inicializa el diálogo para agregar/editar descripción

        Args:
            parent: Widget padre
            descriptionId (int, optional): ID de la descripción a editar
        """
        super().__init__(parent)
        self.descriptionId = descriptionId
        self.descriptionModel = DRDescriptionModel()
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.setupUI()
        if descriptionId:
            self.loadDescription()
    
    def setupUI(self):
        """Configura la interfaz de usuario del diálogo"""
        self.setWindowTitle("Add Description" if not self.descriptionId else "Edit Description")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Campos de entrada
        formLayout = QVBoxLayout()
        
        # Description Text
        nameLayout = QHBoxLayout()
        nameLabel = QLabel("Description:")
        self.nameInput = QLineEdit()
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameInput)
        formLayout.addLayout(nameLayout)
        
        layout.addLayout(formLayout)
        
        # Botones
        buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")
        
        self.saveButton.clicked.connect(self.saveDescription)
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
    
    def loadDescription(self):
        """Carga los datos de la descripción si se está editando"""
        description = self.descriptionModel.getDescriptionById(self.descriptionId)
        if description:
            self.nameInput.setText(description[Columns.DRDescription.DESCRIPTION])
    
    def validateInputs(self):
        if not self.nameInput.text().strip():
            QMessageBox.warning(self, "Validation Error", "Description text is required")
            return False
        return True
    
    def saveDescription(self):
        """Guarda o actualiza la descripción en la base de datos"""
        if not self.validateInputs():
            return
        
        descriptionText = self.nameInput.text().strip()
        
        success = False
        if self.descriptionId:
            # Actualizar descripción existente
            success = self.descriptionModel.updateDescription(
                self.descriptionId,
                descriptionText
            )
        else:
            # Crear nueva descripción
            success = self.descriptionModel.createDescription(descriptionText)
        
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to save description") 