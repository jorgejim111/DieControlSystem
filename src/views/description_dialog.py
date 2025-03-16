from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from models.description_model import DescriptionModel

class DescriptionDialog(QDialog):
    def __init__(self, parent=None, description_data=None):
        super().__init__(parent)
        self.description_model = DescriptionModel()
        self.description_data = description_data
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Add Description" if not self.description_data else "Edit Description")
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QLineEdit {
                background-color: white;
                color: #333333;
                border: 1px solid #cccccc;
                padding: 5px;
                border-radius: 3px;
            }
            QLineEdit:focus {
                border: 1px solid #66afe9;
                outline: 0;
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
            QPushButton#cancelButton {
                background-color: #6c757d;
            }
            QPushButton#cancelButton:hover {
                background-color: #5a6268;
            }
        """)

        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)

        # Campo de valor
        value_layout = QHBoxLayout()
        value_label = QLabel("Description:")
        self.value_input = QLineEdit()
        if self.description_data:
            self.value_input.setText(self.description_data['Description'])
        # Convertir automáticamente a mayúsculas mientras se escribe
        self.value_input.textChanged.connect(self._convert_to_upper)
        value_layout.addWidget(value_label)
        value_layout.addWidget(self.value_input)
        layout.addLayout(value_layout)

        # Botones
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_description)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        # Tamaño mínimo
        self.setMinimumWidth(300)

    def _convert_to_upper(self, text):
        """Convierte el texto a mayúsculas y actualiza el campo"""
        cursor_pos = self.value_input.cursorPosition()
        self.value_input.setText(text.upper())
        self.value_input.setCursorPosition(cursor_pos)

    def save_description(self):
        """Guarda la description en la base de datos"""
        value = self.value_input.text().strip().upper()
        
        # Validación
        if not value:
            QMessageBox.critical(self, "Error", "Please enter a value.")
            return
        
        if len(value) > 5:
            QMessageBox.critical(self, "Error", "The value must be 5 characters or less.")
            return
        
        success = False
        if self.description_data:
            # Actualizar description existente
            success = self.description_model.update_description(self.description_data['id_description'], value)
        else:
            # Crear nueva description
            success = self.description_model.create_description(value)
        
        if success:
            self.accept()
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Could not save the description. The value might be duplicated."
            ) 