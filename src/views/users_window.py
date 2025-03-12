from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSpacerItem, QSizePolicy, QMessageBox, QWidget)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from models.user_model import UserModel
from views.user_dialog import UserDialog
from views.user_roles_dialog import UserRolesDialog

class UsersWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Users Management")
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.userModel = UserModel()
        self.setupUI()
        self.loadUsers()
        
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
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        topFrame.setFrameShape(QFrame.StyledPanel)
        topLayout = QHBoxLayout(topFrame)
        topLayout.setContentsMargins(5, 5, 5, 5)
        
        # Título de la sección
        titleLabel = QLabel("Users Management")
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
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
            QTableWidget {
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 5px;
                border: 1px solid #dee2e6;
                font-weight: bold;
            }
            QPushButton {
                background-color: #0056b3;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 3px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #003d80;
            }
            QPushButton#deleteButton {
                background-color: #dc3545;
            }
            QPushButton#deleteButton:hover {
                background-color: #c82333;
            }
        """)
        contentLayout = QVBoxLayout(contentFrame)
        contentLayout.setContentsMargins(10, 10, 10, 10)
        
        # Barra de herramientas
        toolbarLayout = QHBoxLayout()
        
        # Botones de acción
        self.addButton = QPushButton("Add User")
        self.addButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'add_icon.png')))
        self.addButton.clicked.connect(self.showAddUserDialog)
        
        self.editButton = QPushButton("Edit")
        self.editButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'edit_icon.png')))
        self.editButton.clicked.connect(self.editSelectedUser)
        
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'delete_icon.png')))
        self.deleteButton.clicked.connect(self.deleteSelectedUser)
        
        self.rolesButton = QPushButton("Manage Roles")
        self.rolesButton.clicked.connect(self.showUserRolesDialog)
        
        # Agregar espaciador y botones
        toolbarLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        toolbarLayout.addWidget(self.addButton)
        toolbarLayout.addWidget(self.editButton)
        toolbarLayout.addWidget(self.deleteButton)
        toolbarLayout.addWidget(self.rolesButton)
        
        contentLayout.addLayout(toolbarLayout)
        
        # Tabla de usuarios
        self.usersTable = QTableWidget()
        self.usersTable.setColumnCount(5)
        self.usersTable.setHorizontalHeaderLabels(["Username", "Email", "Worker", "Created", "ID"])
        
        # Configurar la tabla
        header = self.usersTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Username
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Email
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Worker
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # Created
        header.setSectionResizeMode(4, QHeaderView.Fixed)    # ID
        self.usersTable.setColumnWidth(4, 50)  # ID width
        
        self.usersTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.usersTable.setSelectionMode(QTableWidget.SingleSelection)
        self.usersTable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        contentLayout.addWidget(self.usersTable)
        mainLayout.addWidget(contentFrame)
        
        self.setMinimumSize(1000, 600)
    
    def loadUsers(self):
        """Carga los usuarios en la tabla"""
        self.usersTable.setRowCount(0)
        users = self.userModel.get_all_users()
        
        # Diccionario para mantener la relación entre filas e IDs
        self.userIds = {}
        
        for row, user in enumerate(users):
            self.usersTable.insertRow(row)
            
            # Username
            self.usersTable.setItem(row, 0, QTableWidgetItem(user['username']))
            
            # Email
            self.usersTable.setItem(row, 1, QTableWidgetItem(user['email']))
            
            # Worker
            worker_name = user['worker_name'] if user['worker_name'] else 'No Worker'
            self.usersTable.setItem(row, 2, QTableWidgetItem(worker_name))
            
            # Created
            create_time = user['create_time'].strftime('%Y-%m-%d %H:%M:%S') if user['create_time'] else ''
            self.usersTable.setItem(row, 3, QTableWidgetItem(create_time))
            
            # ID
            self.usersTable.setItem(row, 4, QTableWidgetItem(str(user['id_user'])))
            
            # Guardar el ID del usuario
            self.userIds[row] = user['id_user']
    
    def getSelectedUserId(self):
        """Obtiene el ID del usuario seleccionado"""
        selectedItems = self.usersTable.selectedItems()
        if not selectedItems:
            return None
        row = selectedItems[0].row()
        return self.userIds.get(row)
    
    def showAddUserDialog(self):
        """Muestra el diálogo para agregar un usuario"""
        dialog = UserDialog(self)
        if dialog.exec_() == UserDialog.Accepted:
            self.loadUsers()
    
    def editSelectedUser(self):
        """Edita el usuario seleccionado"""
        userId = self.getSelectedUserId()
        if not userId:
            QMessageBox.warning(self, "Selection Required", "Please select a user to edit")
            return
        dialog = UserDialog(self, userId)
        if dialog.exec_() == UserDialog.Accepted:
            self.loadUsers()
    
    def deleteSelectedUser(self):
        """Elimina el usuario seleccionado"""
        userId = self.getSelectedUserId()
        if not userId:
            QMessageBox.warning(self, "Selection Required", "Please select a user to delete")
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this user?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.userModel.delete_user(userId):
                self.loadUsers()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete user")
    
    def showUserRolesDialog(self):
        """Muestra el diálogo para gestionar roles del usuario"""
        selectedRows = self.usersTable.selectedItems()
        if not selectedRows:
            QMessageBox.warning(self, "Error", "Por favor seleccione un usuario")
            return
        
        row = selectedRows[0].row()
        user_id = int(self.usersTable.item(row, 4).text())
        username = self.usersTable.item(row, 0).text()
        
        dialog = UserRolesDialog(self, user_id, username)
        dialog.exec_() 