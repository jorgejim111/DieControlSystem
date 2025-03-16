from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QComboBox, QCheckBox, QSpinBox,
    QGridLayout
)
from PyQt5.QtCore import Qt
from models.die_description_model import DieDescriptionModel

class DieDescriptionDialog(QDialog):
    def __init__(self, parent=None, die_description_data=None):
        """Inicializa el diálogo para agregar/editar die descriptions

        Args:
            parent: Widget padre
            die_description_data (dict, optional): Datos de la die description a editar
        """
        super().__init__(parent)
        self.die_description_data = die_description_data
        self.model = DieDescriptionModel()
        self.related_data = self.model.get_related_data()
        self.setupUI()

    def setupUI(self):
        """Configura la interfaz de usuario del diálogo"""
        # Configurar ventana
        self.setWindowTitle("Add Die Description" if not self.die_description_data else "Edit Die Description")
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit, QComboBox, QSpinBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
                color: #333333;
                selection-background-color: #0056b3;
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
            QCheckBox {
                color: #333333;
            }
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
                border: 1px solid #cccccc;
            }
            QCheckBox::indicator:unchecked {
                background: white;
            }
            QCheckBox::indicator:checked {
                background: #0056b3;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QComboBox:on {
                border: 1px solid #0056b3;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #333333;
                selection-background-color: #0056b3;
                selection-color: white;
            }
        """)

        # Layout principal
        layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # Campos de entrada
        # Inch ComboBox
        inch_label = QLabel("Inch:")
        self.inch_combo = QComboBox()
        for inch in self.related_data['inches']:
            self.inch_combo.addItem(str(inch['Inch']), inch['id_inch'])
        grid_layout.addWidget(inch_label, 0, 0)
        grid_layout.addWidget(self.inch_combo, 0, 1)

        # Part ComboBox
        part_label = QLabel("Part:")
        self.part_combo = QComboBox()
        for part in self.related_data['parts']:
            self.part_combo.addItem(str(part['Part']), part['id_part'])
        grid_layout.addWidget(part_label, 1, 0)
        grid_layout.addWidget(self.part_combo, 1, 1)

        # Description ComboBox
        description_label = QLabel("Description:")
        self.description_combo = QComboBox()
        for desc in self.related_data['descriptions']:
            self.description_combo.addItem(str(desc['Description']), desc['id_description'])
        grid_layout.addWidget(description_label, 2, 0)
        grid_layout.addWidget(self.description_combo, 2, 1)

        # Die Description (read-only)
        die_description_label = QLabel("Die Description:")
        self.die_description_input = QLineEdit()
        self.die_description_input.setReadOnly(True)
        grid_layout.addWidget(die_description_label, 3, 0)
        grid_layout.addWidget(self.die_description_input, 3, 1)

        # Obsolet Checkbox
        self.obsolet_check = QCheckBox("Obsolet")
        grid_layout.addWidget(self.obsolet_check, 4, 0, 1, 2)

        # Circulation SpinBox
        circulation_label = QLabel("Circulation:")
        self.circulation_spin = QSpinBox()
        self.circulation_spin.setRange(0, 999999)
        grid_layout.addWidget(circulation_label, 5, 0)
        grid_layout.addWidget(self.circulation_spin, 5, 1)

        # New SpinBox
        new_label = QLabel("New:")
        self.new_spin = QSpinBox()
        self.new_spin.setRange(0, 999999)
        grid_layout.addWidget(new_label, 6, 0)
        grid_layout.addWidget(self.new_spin, 6, 1)

        # Conectar señales para actualizar Die Description
        self.inch_combo.currentIndexChanged.connect(self.update_die_description)
        self.part_combo.currentIndexChanged.connect(self.update_die_description)
        self.description_combo.currentIndexChanged.connect(self.update_die_description)

        # Botones
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        
        self.save_button.clicked.connect(self.save_die_description)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        # Agregar layouts al layout principal
        layout.addLayout(grid_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Si hay datos, cargarlos en los campos
        if self.die_description_data:
            self.load_die_description_data()

        # Actualizar Die Description inicial
        self.update_die_description()

    def load_die_description_data(self):
        """Carga los datos de la die description en los campos del formulario"""
        # Establecer valores en los combos
        inch_index = self.inch_combo.findData(self.die_description_data['id_inch'])
        part_index = self.part_combo.findData(self.die_description_data['id_part'])
        description_index = self.description_combo.findData(self.die_description_data['id_description'])
        
        self.inch_combo.setCurrentIndex(inch_index)
        self.part_combo.setCurrentIndex(part_index)
        self.description_combo.setCurrentIndex(description_index)
        
        # Establecer otros valores
        self.obsolet_check.setChecked(bool(self.die_description_data['Obsolet']))
        self.circulation_spin.setValue(int(self.die_description_data['Circulation']))
        self.new_spin.setValue(int(self.die_description_data['New']))

    def update_die_description(self):
        """Actualiza el campo Die Description basado en los valores seleccionados"""
        inch = self.inch_combo.currentText()
        part = self.part_combo.currentText()
        description = self.description_combo.currentText()
        
        die_description = f"{inch}-{part}-{description}"
        self.die_description_input.setText(die_description.upper())

    def save_die_description(self):
        """Guarda o actualiza la die description en la base de datos"""
        # Preparar datos
        data = {
            'Die_Description': self.die_description_input.text(),
            'id_inch': self.inch_combo.currentData(),
            'id_part': self.part_combo.currentData(),
            'id_description': self.description_combo.currentData(),
            'Obsolet': self.obsolet_check.isChecked(),
            'Circulation': self.circulation_spin.value(),
            'New': self.new_spin.value()
        }

        success = False
        if self.die_description_data:
            # Actualizar
            success = self.model.update_die_description(
                self.die_description_data['id_die_description'],
                data
            )
        else:
            # Crear nuevo
            success = self.model.create_die_description(data)

        if success:
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Could not save Die Description. Please check if a similar one already exists."
            ) 