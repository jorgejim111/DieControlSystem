from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from models.line_model import LineModel

class LineDialog(QDialog):
    def __init__(self, parent=None, line_id=None):
        """Inicializa el diálogo para agregar/editar líneas

        Args:
            parent: Widget padre
            line_id (int, optional): ID de la línea a editar
        """
        super().__init__(parent)
        self.line_id = line_id
        self.model = LineModel()
        self.setupUI()
        
        if line_id:
            self.setWindowTitle("Edit Line")
            self.loadLineData()
        else:
            self.setWindowTitle("Add Line")

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

        # Campo de entrada para Line
        inputLayout = QHBoxLayout()
        lineLabel = QLabel("Line:")
        lineLabel.setFixedWidth(80)
        self.lineInput = QLineEdit()
        self.lineInput.setMaxLength(10)  # Limitar a 10 caracteres
        inputLayout.addWidget(lineLabel)
        inputLayout.addWidget(self.lineInput)
        layout.addLayout(inputLayout)

        # Botones
        buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.saveButton.setObjectName("saveButton")
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setObjectName("cancelButton")
        
        self.saveButton.clicked.connect(self.saveLine)
        self.cancelButton.clicked.connect(self.reject)
        
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonLayout)

        # Configurar el tamaño del diálogo
        self.setMinimumWidth(300)
        self.setMaximumHeight(150)

    def loadLineData(self):
        """Carga los datos de la línea si se está editando"""
        line_data = self.model.getLineById(self.line_id)
        if line_data:
            self.lineInput.setText(line_data['Line'])

    def saveLine(self):
        """Guarda o actualiza la línea en la base de datos"""
        line_name = self.lineInput.text().strip()
        
        if not line_name:
            QMessageBox.warning(self, "Validation Error", "Line name cannot be empty")
            return
            
        success = False
        if self.line_id:
            # Actualizar línea existente
            success = self.model.updateLine(self.line_id, line_name)
        else:
            # Crear nueva línea
            success = self.model.createLine(line_name)
            
        if success:
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Could not save line. Please check if a similar one already exists."
            ) 