from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QPushButton, QLineEdit, QSpacerItem, QSizePolicy, 
                             QMessageBox, QWidget)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from models.user_model import UserModel
from views.main_window import MainWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Die Control System")
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.userModel = UserModel()
        self.setupUI()
    
    def setupUI(self):
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
                border: none;
                border-radius: 5px;
                padding: 5px;
            }
            QLabel {
                border: none;
                background: transparent;
            }
        """)
        topLayout = QHBoxLayout(topFrame)
        topLayout.setContentsMargins(5, 5, 5, 5)
        
        # Título de la sección
        titleLabel = QLabel("Die Control System")
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
                border: none;
                border-radius: 5px;
                padding: 20px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
                min-width: 250px;
            }
            QPushButton {
                background-color: #0056b3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 3px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #003d80;
            }
            QLabel {
                color: #333;
                border: none;
                background: transparent;
            }
        """)
        contentLayout = QVBoxLayout(contentFrame)
        contentLayout.setContentsMargins(20, 20, 20, 20)
        contentLayout.setSpacing(15)
        
        # Título de login
        loginLabel = QLabel("Login")
        loginLabel.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px; border: none; background: transparent;")
        loginLabel.setAlignment(Qt.AlignCenter)
        contentLayout.addWidget(loginLabel)
        
        # Formulario
        formLayout = QVBoxLayout()
        formLayout.setSpacing(10)
        
        # Username
        usernameLayout = QHBoxLayout()
        usernameLabel = QLabel("Username:")
        usernameLabel.setMinimumWidth(80)
        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Enter your username")
        usernameLayout.addWidget(usernameLabel)
        usernameLayout.addWidget(self.usernameInput)
        formLayout.addLayout(usernameLayout)
        
        # Password
        passwordLayout = QHBoxLayout()
        passwordLabel = QLabel("Password:")
        passwordLabel.setMinimumWidth(80)
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setPlaceholderText("Enter your password")
        passwordLayout.addWidget(passwordLabel)
        passwordLayout.addWidget(self.passwordInput)
        formLayout.addLayout(passwordLayout)
        
        contentLayout.addLayout(formLayout)
        
        # Botón de login
        buttonLayout = QHBoxLayout()
        buttonLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.loginButton = QPushButton("Login")
        self.loginButton.clicked.connect(self.handleLogin)
        self.loginButton.setDefault(True)  # Enter key triggers this button
        buttonLayout.addWidget(self.loginButton)
        
        contentLayout.addLayout(buttonLayout)
        
        mainLayout.addWidget(contentFrame)
        
        # Ajustar el tamaño de la ventana
        self.setMinimumSize(500, 400)
        self.setMaximumSize(600, 500)
        
        # Centrar la ventana en la pantalla
        self.center()
        
        # Establecer el foco en el campo de usuario
        self.usernameInput.setFocus()
    
    def center(self):
        """Centra la ventana en la pantalla"""
        frameGm = self.frameGeometry()
        screen = self.screen()
        centerPoint = screen.availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
    
    def handleLogin(self):
        """Maneja el proceso de login"""
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text().strip()
        
        if not username:
            QMessageBox.warning(self, "Error", "Please enter your username")
            self.usernameInput.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, "Error", "Please enter your password")
            self.passwordInput.setFocus()
            return
        
        # Validar credenciales
        user = self.userModel.validate_login(username, password)
        
        if user:
            # Login exitoso
            QMessageBox.information(self, "Success", f"Welcome {user['username']}!")
            self.accept(user)
        else:
            # Login fallido
            QMessageBox.critical(self, "Error", "Invalid username or password")
            self.passwordInput.clear()
            self.passwordInput.setFocus()
    
    def accept(self, user):
        """Método llamado cuando el login es exitoso"""
        # Crear y mostrar la ventana principal
        self.main_window = MainWindow(user)
        self.main_window.show()
        # Cerrar la ventana de login
        self.close() 