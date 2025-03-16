from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from models.part_model import PartModel

class PartDialog(QDialog):
    def __init__(self, parent=None, part_data=None):
        super().__init__(parent)
        self.part_model = PartModel()
        self.part_data = part_data
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Add Part" if not self.part_data else "Edit Part")
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
        value_label = QLabel("Part:")
        self.value_input = QLineEdit()
        if self.part_data:
            self.value_input.setText(self.part_data['Part'])
        # Convertir automáticamente a mayúsculas mientras se escribe
        self.value_input.textChanged.connect(self._convert_to_upper)
        value_layout.addWidget(value_label)
        value_layout.addWidget(self.value_input)
        layout.addLayout(value_layout)

        # Botones
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_part)
        
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

    def save_part(self):
        """Guarda la part en la base de datos"""
        value = self.value_input.text().strip().upper()
        
        # Validación
        if not value:
            QMessageBox.critical(self, "Error", "Please enter a value.")
            return
        
        if len(value) > 20:
            QMessageBox.critical(self, "Error", "The value must be 20 characters or less.")
            return
        
        success = False
        if self.part_data:
            # Actualizar part existente
            success = self.part_model.update_part(self.part_data['id_part'], value)
        else:
            # Crear nueva part
            success = self.part_model.create_part(value)
        
        if success:
            self.accept()
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Could not save the part. The value might be duplicated."
            ) 