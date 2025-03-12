from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from models.role_model import RoleModel
from database.database_schema import Columns

class RolesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roles Management")
        
        # Establecer el ícono de la ventana
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
            
        self.roleModel = RoleModel()
        self.setupUI()
        self.loadRoles()
        
    def setupUI(self):
        # Layout principal
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)
        self.setLayout(mainLayout)
        
        # Frame superior para el logo
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
        titleLabel = QLabel("Roles Management")
        titleLabel.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        topLayout.addWidget(titleLabel)
        
        # Agregar espaciador entre el título y el logo
        topLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Agregar logo
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
            QPushButton#deleteButton {
                background-color: #dc3545;
            }
            QPushButton#deleteButton:hover {
                background-color: #c82333;
            }
            QTableWidget {
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 5px;
                border: 1px solid #cccccc;
                font-weight: bold;
            }
        """)
        contentLayout = QVBoxLayout(contentFrame)
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        
        # Espaciador
        toolbar.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Botones
        self.addButton = QPushButton("Add Role")
        self.editButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.setObjectName("deleteButton")
        
        toolbar.addWidget(self.addButton)
        toolbar.addWidget(self.editButton)
        toolbar.addWidget(self.deleteButton)
        
        contentLayout.addLayout(toolbar)
        
        # Tabla de roles
        self.rolesTable = QTableWidget()
        self.rolesTable.setColumnCount(1)
        self.rolesTable.setHorizontalHeaderLabels(['Role'])
        
        # Configurar la tabla
        header = self.rolesTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.rolesTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.rolesTable.setSelectionMode(QTableWidget.SingleSelection)
        self.rolesTable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        contentLayout.addWidget(self.rolesTable)
        mainLayout.addWidget(contentFrame)
        
        # Conectar señales
        self.addButton.clicked.connect(self.addRole)
        self.editButton.clicked.connect(self.editRole)
        self.deleteButton.clicked.connect(self.deleteRole)
        
        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(800, 600)
    
    def loadRoles(self):
        """Carga los roles en la tabla"""
        self.rolesTable.setRowCount(0)
        roles = self.roleModel.getAllRoles()  # Ya viene ordenado por rol
        
        # Crear un diccionario para almacenar la relación entre rol y su ID
        self.roleIds = {}
        
        for row, role in enumerate(roles):
            self.rolesTable.insertRow(row)
            roleName = role[Columns.Roles.ROLE]
            self.rolesTable.setItem(row, 0, QTableWidgetItem(roleName))
            # Guardar el ID asociado a este rol
            self.roleIds[row] = role[Columns.Roles.ID]
    
    def getSelectedRoleId(self):
        """Obtiene el ID del rol seleccionado"""
        selectedItems = self.rolesTable.selectedItems()
        if not selectedItems:
            return None
        selectedRow = selectedItems[0].row()
        return self.roleIds[selectedRow]
        
    def addRole(self):
        """Abre el diálogo para agregar un nuevo rol"""
        from .role_dialog import RoleDialog
        dialog = RoleDialog(self)
        if dialog.exec_() == RoleDialog.Accepted:
            self.loadRoles()
        
    def editRole(self):
        """Abre el diálogo para editar un rol existente"""
        roleId = self.getSelectedRoleId()
        if not roleId:
            QMessageBox.warning(self, "Selection Required", "Please select a role to edit")
            return
            
        from .role_dialog import RoleDialog
        dialog = RoleDialog(self, roleId)
        if dialog.exec_() == RoleDialog.Accepted:
            self.loadRoles()
        
    def deleteRole(self):
        """Elimina el rol seleccionado"""
        roleId = self.getSelectedRoleId()
        if not roleId:
            QMessageBox.warning(self, "Selection Required", "Please select a role to delete")
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this role?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.roleModel.deleteRole(roleId):
                self.loadRoles()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete role") 