from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from models.status_model import StatusModel

class StatusDialog(QDialog):
    def __init__(self, parent=None, status_id=None):
        """Inicializa el diálogo para agregar/editar status

        Args:
            parent: Widget padre
            status_id (int, optional): ID del status a editar
        """
        super().__init__(parent)
        self.status_id = status_id
        self.model = StatusModel()
        self.setupUI()
        
        if status_id:
            self.setWindowTitle("Edit Status")
            self.loadStatusData()
        else:
            self.setWindowTitle("Add Status")

    def setupUI(self):
        """Configura la interfaz de usuario del diálogo"""
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
                color: #333333;
            }
            QPushButton {
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                color: white;
                min-width: 80px;
            }
            QPushButton#saveButton {
                background-color: #0056b3;
            }
            QPushButton#saveButton:hover {
                background-color: #003d80;
            }
            QPushButton#cancelButton {
                background-color: #6c757d;
            }
            QPushButton#cancelButton:hover {
                background-color: #5a6268;
            }
        """)

        # Layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Campo de entrada para Status
        inputLayout = QHBoxLayout()
        statusLabel = QLabel("Status:")
        statusLabel.setFixedWidth(80)
        self.statusInput = QLineEdit()
        self.statusInput.setMaxLength(45)  # Limitar a 45 caracteres
        inputLayout.addWidget(statusLabel)
        inputLayout.addWidget(self.statusInput)
        layout.addLayout(inputLayout)

        # Botones
        buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.saveButton.setObjectName("saveButton")
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setObjectName("cancelButton")
        
        self.saveButton.clicked.connect(self.saveStatus)
        self.cancelButton.clicked.connect(self.reject)
        
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonLayout)

        # Configurar el tamaño del diálogo
        self.setMinimumWidth(300)
        self.setMaximumHeight(150)

    def loadStatusData(self):
        """Carga los datos del status si se está editando"""
        status_data = self.model.getStatusById(self.status_id)
        if status_data:
            self.statusInput.setText(status_data['Status'])

    def saveStatus(self):
        """Guarda o actualiza el status en la base de datos"""
        status_name = self.statusInput.text().strip()
        
        if not status_name:
            QMessageBox.warning(self, "Validation Error", "Status name cannot be empty")
            return
            
        success = False
        if self.status_id:
            # Actualizar status existente
            success = self.model.updateStatus(self.status_id, status_name)
        else:
            # Crear nuevo status
            success = self.model.createStatus(status_name)
            
        if success:
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Could not save status. Please check if a similar one already exists."
            ) 