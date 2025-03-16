from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from models.user_model import UserModel
import os

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.user_model = UserModel()
        self.user_data = None  # Para almacenar los datos del usuario autenticado
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.setupUI()
    
    def setupUI(self):
        self.setWindowTitle("Login - Die Control System")
        self.setModal(True)
        
        # Layout principal
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(15)
        self.setLayout(mainLayout)
        
        # Frame superior para el logo
        topFrame = QFrame()
        topFrame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        topLayout = QHBoxLayout(topFrame)
        
        # Logo
        logoLabel = QLabel()
        logoPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'logo_masternet.png')
        if os.path.exists(logoPath):
            pixmap = QPixmap(logoPath)
            scaledPixmap = pixmap.scaled(216, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logoLabel.setPixmap(scaledPixmap)
            logoLabel.setAlignment(Qt.AlignCenter)
        topLayout.addWidget(logoLabel)
        mainLayout.addWidget(topFrame)
        
        # Frame principal para el formulario
        contentFrame = QFrame()
        contentFrame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 20px;
            }
            QLabel {
                border: none;
                font-size: 12px;
                color: #333333;
                min-width: 80px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                min-width: 200px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #0056b3;
            }
            QPushButton {
                background-color: #0056b3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 3px;
                min-width: 100px;
                font-size: 14px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #003d80;
            }
        """)
        formLayout = QVBoxLayout(contentFrame)
        formLayout.setSpacing(15)
        
        # Username
        usernameLayout = QHBoxLayout()
        usernameLayout.setSpacing(10)
        usernameLabel = QLabel("Username:")
        usernameLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Enter your username")
        usernameLayout.addWidget(usernameLabel)
        usernameLayout.addWidget(self.usernameInput)
        formLayout.addLayout(usernameLayout)
        
        # Password
        passwordLayout = QHBoxLayout()
        passwordLayout.setSpacing(10)
        passwordLabel = QLabel("Password:")
        passwordLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setPlaceholderText("Enter your password")
        passwordLayout.addWidget(passwordLabel)
        passwordLayout.addWidget(self.passwordInput)
        formLayout.addLayout(passwordLayout)
        
        # Botón de login
        self.loginButton = QPushButton("Login")
        self.loginButton.clicked.connect(self.login)
        formLayout.addWidget(self.loginButton, alignment=Qt.AlignCenter)
        
        mainLayout.addWidget(contentFrame)
        
        # Estilo general de la ventana
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
        """)
        
        # Configurar tamaño y posición
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        # Permitir presionar Enter para hacer login
        self.passwordInput.returnPressed.connect(self.login)
        self.usernameInput.returnPressed.connect(self.passwordInput.setFocus)
    
    def login(self):
        """Valida las credenciales e inicia sesión"""
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Validation Error", "Please enter username and password")
            return
        
        user = self.user_model.validate_login(username, password)
        if user:
            self.user_data = user
            self.accept()
        else:
            QMessageBox.critical(self, "Login Error", "Invalid username or password")
            self.passwordInput.clear()
            self.passwordInput.setFocus()
    
    def get_user_data(self):
        """Retorna los datos del usuario autenticado"""
        return self.user_data 