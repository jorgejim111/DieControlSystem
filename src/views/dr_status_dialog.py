from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from models.dr_status_model import DRStatusModel
from database.database_schema import Columns
import os
from PyQt5.QtGui import QIcon

class DRStatusDialog(QDialog):
    def __init__(self, parent=None, status_id=None):
        """Inicializa el diálogo para agregar/editar estado

        Args:
            parent: Widget padre
            status_id (int, optional): ID del estado a editar
        """
        super().__init__(parent)
        self.status_id = status_id
        self.statusModel = DRStatusModel()
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.setupUI()
        if status_id:
            self.loadStatus()
    
    def setupUI(self):
        """Configura la interfaz de usuario del diálogo"""
        self.setWindowTitle("Add Status" if not self.status_id else "Edit Status")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Campos de entrada
        formLayout = QVBoxLayout()
        
        # Status Text
        nameLayout = QHBoxLayout()
        nameLabel = QLabel("Status:")
        self.nameInput = QLineEdit()
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameInput)
        formLayout.addLayout(nameLayout)
        
        layout.addLayout(formLayout)
        
        # Botones
        buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")
        
        self.saveButton.clicked.connect(self.saveStatus)
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
    
    def loadStatus(self):
        """Carga los datos del estado si se está editando"""
        status = self.statusModel.getStatusById(self.status_id)
        if status:
            self.nameInput.setText(status[Columns.DRStatus.STATUS])
    
    def validateInputs(self):
        if not self.nameInput.text().strip():
            QMessageBox.warning(self, "Validation Error", "Status text is required")
            return False
        return True
    
    def saveStatus(self):
        """Guarda o actualiza el estado en la base de datos"""
        if not self.validateInputs():
            return
        
        statusText = self.nameInput.text().strip()
        
        success = False
        if self.status_id:
            # Actualizar estado existente
            success = self.statusModel.updateStatus(
                self.status_id,
                statusText
            )
        else:
            # Crear nuevo estado
            success = self.statusModel.createStatus(statusText)
        
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to save status") 