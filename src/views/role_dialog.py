from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from models.role_model import RoleModel
from database.database_schema import Columns
import os
from PyQt5.QtGui import QIcon

class RoleDialog(QDialog):
    def __init__(self, parent=None, roleId=None):
        super().__init__(parent)
        self.roleId = roleId
        self.roleModel = RoleModel()
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.setupUI()
        if roleId:
            self.loadRole()
    
    def setupUI(self):
        self.setWindowTitle("Add Role" if not self.roleId else "Edit Role")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Campos de entrada
        formLayout = QVBoxLayout()
        
        # ID Role (solo visible al crear nuevo rol)
        if not self.roleId:
            idLayout = QHBoxLayout()
            idLabel = QLabel("ID:")
            self.idInput = QLineEdit()
            self.idInput.setPlaceholderText("Enter role ID")
            idLayout.addWidget(idLabel)
            idLayout.addWidget(self.idInput)
            formLayout.addLayout(idLayout)
        
        # Role Name
        nameLayout = QHBoxLayout()
        nameLabel = QLabel("Role:")
        self.nameInput = QLineEdit()
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameInput)
        formLayout.addLayout(nameLayout)
        
        layout.addLayout(formLayout)
        
        # Botones
        buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")
        
        self.saveButton.clicked.connect(self.saveRole)
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
            QLabel {
                min-width: 80px;
            }
        """)
        
        self.setMinimumWidth(400)
    
    def loadRole(self):
        """Carga los datos del rol para edición"""
        role = self.roleModel.getRoleById(self.roleId)
        if role:
            self.nameInput.setText(role[Columns.Roles.ROLE])
    
    def validateInputs(self):
        """Valida los campos del formulario"""
        if not self.roleId and not self.idInput.text().strip():
            QMessageBox.warning(self, "Validation Error", "Role ID is required")
            return False
            
        if not self.nameInput.text().strip():
            QMessageBox.warning(self, "Validation Error", "Role name is required")
            return False
            
        if not self.roleId:
            try:
                int(self.idInput.text().strip())
            except ValueError:
                QMessageBox.warning(self, "Validation Error", "Role ID must be a number")
                return False
        return True
    
    def saveRole(self):
        """Guarda o actualiza el rol"""
        if not self.validateInputs():
            return
        
        roleName = self.nameInput.text().strip()
        
        success = False
        if self.roleId:
            # Actualizar rol existente
            success = self.roleModel.updateRole(
                self.roleId,
                roleName
            )
        else:
            # Crear nuevo rol con ID manual
            roleId = int(self.idInput.text().strip())
            success = self.roleModel.createRole(roleId, roleName)
        
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to save role") 