from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QMessageBox, QLabel, QScrollArea, 
                             QWidget, QCheckBox)
from PyQt5.QtCore import Qt
from models.user_model import UserModel
from models.role_model import RoleModel
from database.database_schema import Columns
import os
from PyQt5.QtGui import QIcon

class UserRolesDialog(QDialog):
    def __init__(self, parent=None, user_id=None, username=None):
        super().__init__(parent)
        self.user_id = user_id
        self.username = username
        self.user_model = UserModel()
        self.role_model = RoleModel()
        self.role_checkboxes = {}  # Dictionary to store checkbox references
        
        # Set window icon
        iconPath = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(iconPath):
            self.setWindowIcon(QIcon(iconPath))
        
        self.setupUI()
        self.loadRoles()
    
    def setupUI(self):
        self.setWindowTitle(f"User Roles: {self.username}")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Title
        titleLabel = QLabel(f"Assign roles to: {self.username}")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Scrollable area for checkboxes
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scrollContent = QWidget()
        self.rolesLayout = QVBoxLayout(scrollContent)
        scrollArea.setWidget(scrollContent)
        layout.addWidget(scrollArea)
        
        # Buttons
        buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")
        
        self.saveButton.clicked.connect(self.saveRoles)
        self.cancelButton.clicked.connect(self.reject)
        
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonLayout)
        
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QCheckBox {
                padding: 5px;
            }
            QCheckBox:hover {
                background-color: #f0f0f0;
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
            QScrollArea {
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
        """)
    
    def loadRoles(self):
        """Load all roles and mark those assigned to the user"""
        try:
            # Get all roles
            all_roles = self.role_model.getAllRoles()
            
            # Get roles assigned to user
            user_roles = self.user_model.get_user_roles(self.user_id)
            user_role_ids = [role[Columns.Roles.ID] for role in user_roles]
            
            # Create checkboxes
            for role in all_roles:
                checkbox = QCheckBox(role[Columns.Roles.ROLE])
                checkbox.setChecked(role[Columns.Roles.ID] in user_role_ids)
                self.role_checkboxes[role[Columns.Roles.ID]] = checkbox
                self.rolesLayout.addWidget(checkbox)
            
            # Add spacing at the end
            self.rolesLayout.addStretch()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading roles: {str(e)}")
    
    def saveRoles(self):
        """Save selected roles for the user"""
        try:
            # First remove all current roles
            self.user_model.remove_all_user_roles(self.user_id)
            
            # Assign selected roles
            for role_id, checkbox in self.role_checkboxes.items():
                if checkbox.isChecked():
                    self.user_model.assign_role_to_user(self.user_id, role_id)
            
            QMessageBox.information(self, "Success", "Roles updated successfully")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving roles: {str(e)}") 