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
        
        # Campos de entrada
        formLayout = QVBoxLayout()
        
        # Username
        usernameLayout = QHBoxLayout()
        usernameLabel = QLabel("Username:")
        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Enter username")
        usernameLayout.addWidget(usernameLabel)
        usernameLayout.addWidget(self.usernameInput)
        formLayout.addLayout(usernameLayout)
        
        # Email
        emailLayout = QHBoxLayout()
        emailLabel = QLabel("Email:")
        self.emailInput = QLineEdit()
        self.emailInput.setPlaceholderText("Enter email")
        emailLayout.addWidget(emailLabel)
        emailLayout.addWidget(self.emailInput)
        formLayout.addLayout(emailLayout)
        
        # Password (solo visible al crear nuevo usuario)
        if not self.user_id:
            passwordLayout = QHBoxLayout()
            passwordLabel = QLabel("Password:")
            self.passwordInput = QLineEdit()
            self.passwordInput.setEchoMode(QLineEdit.Password)
            self.passwordInput.setPlaceholderText("Enter password")
            passwordLayout.addWidget(passwordLabel)
            passwordLayout.addWidget(self.passwordInput)
            formLayout.addLayout(passwordLayout)
        
        # Worker
        workerLayout = QHBoxLayout()
        workerLabel = QLabel("Worker:")
        self.workerCombo = QComboBox()
        self.loadWorkers()  # Cargar la lista de trabajadores
        workerLayout.addWidget(workerLabel)
        workerLayout.addWidget(self.workerCombo)
        formLayout.addLayout(workerLayout)
        
        layout.addLayout(formLayout)
        
        # Botones
        buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")
        
        self.saveButton.clicked.connect(self.saveUser)
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
            self.usernameInput.setText(user['username'])
            self.emailInput.setText(user['email'])
            
            # Seleccionar el trabajador si existe
            if user['id_worker']:
                index = self.workerCombo.findData(user['id_worker'])
                if index >= 0:
                    self.workerCombo.setCurrentIndex(index)
            
            # Deshabilitar el campo ID en modo edición
            self.usernameInput.setEnabled(False)
            self.emailInput.setEnabled(False)
    
    def validateInputs(self):
        """Valida los campos del formulario"""
        if not self.usernameInput.text().strip():
            QMessageBox.warning(self, "Validation Error", "Username is required")
            return False
            
        if not self.emailInput.text().strip():
            QMessageBox.warning(self, "Validation Error", "Email is required")
            return False
            
        if not self.user_id and not self.passwordInput.text().strip():
            QMessageBox.warning(self, "Validation Error", "Password is required")
            return False
            
        if self.workerCombo.currentData() is None:
            QMessageBox.warning(self, "Validation Error", "Worker is required")
            return False
            
        return True
    
    def saveUser(self):
        """Guarda o actualiza el usuario"""
        if not self.validateInputs():
            return
        
        username = self.usernameInput.text().strip()
        email = self.emailInput.text().strip()
        workerId = self.workerCombo.currentData()
        
        success = False
        if self.user_id:
            # Actualizar usuario existente
            success = self.user_model.update_user(
                self.user_id,
                username,
                email,
                workerId
            )
        else:
            # Crear nuevo usuario
            password = self.passwordInput.text().strip()
            success = self.user_model.createUser(
                username,
                email,
                password,
                workerId
            )
        
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to save user") 