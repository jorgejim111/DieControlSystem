from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from models.user_model import UserModel
import os
from PyQt5.QtGui import QIcon
import re
import bcrypt

class UserDialog(QDialog):
    def __init__(self, parent=None, user_id=None):
        super().__init__(parent)
        self.user_id = user_id
        self.user_model = UserModel()
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.setupUI()
        if user_id:
            self.loadUser()
    
    def setupUI(self):
        self.setWindowTitle("Add User" if not self.user_id else "Edit User")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # ID de Usuario
        idLayout = QHBoxLayout()
        idLabel = QLabel("ID:")
        self.idInput = QLineEdit()
        self.idInput.setPlaceholderText("Ingrese el ID del usuario")
        idLayout.addWidget(idLabel)
        idLayout.addWidget(self.idInput)
        layout.addLayout(idLayout)
        
        # Username
        usernameLayout = QHBoxLayout()
        usernameLabel = QLabel("Username:")
        self.usernameInput = QLineEdit()
        self.usernameInput.setMaxLength(16)  # Limitar a 16 caracteres
        usernameLayout.addWidget(usernameLabel)
        usernameLayout.addWidget(self.usernameInput)
        layout.addLayout(usernameLayout)
        
        # Email
        emailLayout = QHBoxLayout()
        emailLabel = QLabel("Email:")
        self.emailInput = QLineEdit()
        self.emailInput.setMaxLength(255)  # Limitar a 255 caracteres
        emailLayout.addWidget(emailLabel)
        emailLayout.addWidget(self.emailInput)
        layout.addLayout(emailLayout)
        
        # Password
        passwordLayout = QHBoxLayout()
        passwordLabel = QLabel("Password:")
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        passwordLayout.addWidget(passwordLabel)
        passwordLayout.addWidget(self.passwordInput)
        layout.addLayout(passwordLayout)
        
        # Worker
        workerLayout = QHBoxLayout()
        workerLabel = QLabel("Worker:")
        self.workerCombo = QComboBox()
        self.loadWorkers()  # Cargar los trabajadores disponibles
        workerLayout.addWidget(workerLabel)
        workerLayout.addWidget(self.workerCombo)
        layout.addLayout(workerLayout)
        
        # Botones
        buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")
        
        self.saveButton.clicked.connect(self.saveUser)
        self.cancelButton.clicked.connect(self.reject)
        
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonLayout)
        
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
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
        """)
    
    def loadWorkers(self):
        """Carga los trabajadores en el combo box"""
        self.workerCombo.clear()
        self.workerCombo.addItem("No Worker", None)
        workers = self.user_model.get_all_workers()
        for worker in workers:
            self.workerCombo.addItem(worker['Name'], worker['idWorkers'])
    
    def loadUser(self):
        """Carga los datos del usuario para edición"""
        user = self.user_model.get_user_by_id(self.user_id)
        if user:
            self.idInput.setText(str(user['id_user']))
            self.usernameInput.setText(user['username'])
            self.emailInput.setText(user['email'])
            
            # Seleccionar el trabajador si existe
            if user['id_worker']:
                index = self.workerCombo.findData(user['id_worker'])
                if index >= 0:
                    self.workerCombo.setCurrentIndex(index)
            
            # Deshabilitar el campo ID en modo edición
            self.idInput.setEnabled(False)
    
    def validateInputs(self):
        """Valida los campos de entrada"""
        if not self.idInput.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese el ID del usuario")
            return False
        
        if not self.usernameInput.text().strip():
            QMessageBox.warning(self, "Error", "Username is required")
            return False
        
        if not self.emailInput.text().strip():
            QMessageBox.warning(self, "Error", "Email is required")
            return False
        
        # Validar formato de email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.emailInput.text()):
            QMessageBox.warning(self, "Error", "Por favor ingrese un email válido")
            return False
        
        if not self.user_id and not self.passwordInput.text().strip():
            QMessageBox.warning(self, "Error", "Password is required for new users")
            return False
        
        return True
    
    def saveUser(self):
        """Guarda o actualiza el usuario"""
        if not self.validateInputs():
            return
        
        username = self.usernameInput.text().strip()
        email = self.emailInput.text().strip()
        password = self.passwordInput.text().strip()
        worker_id = self.workerCombo.currentData()
        user_id = int(self.idInput.text()) if self.idInput.text() else None
        
        try:
            if self.user_id:
                # Actualizar usuario existente
                success = self.user_model.update_user(self.user_id, username, email, worker_id)
                if password:
                    self.user_model.update_password(self.user_id, password)
            else:
                # Crear nuevo usuario
                success = self.user_model.create_user(user_id, username, email, password, worker_id)
            
            if success:
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to save user")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar el usuario: {str(e)}") 