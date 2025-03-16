from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from models.inch_model import InchModel

class InchDialog(QDialog):
    def __init__(self, parent=None, inch_data=None):
        """Inicializa el diálogo para agregar/editar pulgadas

        Args:
            parent: Widget padre
            inch_data (dict, optional): Datos de la pulgada a editar. Defaults to None.
        """
        super().__init__(parent)
        self.inch_model = InchModel()
        self.inch_data = inch_data
        self.setupUI()

    def setupUI(self):
        """Configura la interfaz de usuario"""
        # Configuración de la ventana
        self.setWindowTitle("Add Inch" if not self.inch_data else "Edit Inch")
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
        value_label = QLabel("Inch:")
        self.value_input = QLineEdit()
        if self.inch_data:
            self.value_input.setText(self.inch_data['Inch'])
        value_layout.addWidget(value_label)
        value_layout.addWidget(self.value_input)
        layout.addLayout(value_layout)

        # Botones
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_inch)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        # Tamaño mínimo
        self.setMinimumWidth(300)

    def save_inch(self):
        """Guarda la pulgada en la base de datos"""
        value = self.value_input.text().strip()
        
        # Validación
        if not value:
            QMessageBox.critical(self, "Error", "Please enter a value.")
            return
        
        if len(value) > 5:
            QMessageBox.critical(self, "Error", "The value must be 5 characters or less.")
            return
        
        success = False
        if self.inch_data:
            # Actualizar pulgada existente
            success = self.inch_model.update_inch(self.inch_data['id_inch'], value)
        else:
            # Crear nueva pulgada
            success = self.inch_model.create_inch(value)
        
        if success:
            self.accept()
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Could not save the inch. The value might be duplicated."
            ) 