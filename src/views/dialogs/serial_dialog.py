from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox, QPushButton, QMessageBox,
                             QDoubleSpinBox, QFrame)
from PyQt5.QtCore import Qt
from models.serial_model import SerialModel

class SerialDialog(QDialog):
    def __init__(self, parent=None, serial_id=None):
        """Inicializa el diálogo de serials

        Args:
            parent: Widget padre
            serial_id (int, optional): ID del serial a editar. Defaults to None.
        """
        super().__init__(parent)
        self.serial_id = serial_id
        self.model = SerialModel()
        self.setupUi()
        
        if serial_id:
            self.setWindowTitle("Edit Serial")
            self.loadSerialData()
        else:
            self.setWindowTitle("New Serial")

    def setupUi(self):
        """Configura la interfaz de usuario"""
        self.setModal(True)
        self.resize(400, 400)  # Aumentamos el alto para los nuevos campos
        
        # Layout principal
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)
        
        # Establecer el estilo para todo el diálogo
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit, QComboBox, QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
                min-width: 200px;
            }
            QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus {
                border: 1px solid #0056b3;
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
            QPushButton[text="Cancel"] {
                background-color: #6c757d;
            }
            QPushButton[text="Cancel"]:hover {
                background-color: #545b62;
            }
        """)
        
        # Frame para el contenido
        contentFrame = QFrame()
        contentFrame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
        """)
        
        contentLayout = QVBoxLayout(contentFrame)
        contentLayout.setSpacing(15)
        contentLayout.setContentsMargins(20, 20, 20, 20)
        
        # Serial
        serialLayout = QHBoxLayout()
        serialLabel = QLabel("Serial:")
        serialLabel.setMinimumWidth(100)
        self.serialInput = QLineEdit()
        self.serialInput.setMaxLength(15)
        self.serialInput.setPlaceholderText("Enter serial number")
        self.serialInput.textChanged.connect(self._convert_to_upper)  # Convertir a mayúsculas mientras se escribe
        serialLayout.addWidget(serialLabel)
        serialLayout.addWidget(self.serialInput)
        contentLayout.addLayout(serialLayout)
        
        # Inch
        inchLayout = QHBoxLayout()
        inchLabel = QLabel("Inch:")
        inchLabel.setMinimumWidth(100)
        self.inchCombo = QComboBox()
        inchLayout.addWidget(inchLabel)
        inchLayout.addWidget(self.inchCombo)
        contentLayout.addLayout(inchLayout)
        
        # Part
        partLayout = QHBoxLayout()
        partLabel = QLabel("Part:")
        partLabel.setMinimumWidth(100)
        self.partCombo = QComboBox()
        self.partCombo.setEnabled(False)  # Deshabilitado hasta que se seleccione un inch
        partLayout.addWidget(partLabel)
        partLayout.addWidget(self.partCombo)
        contentLayout.addLayout(partLayout)
        
        # Die Description
        dieLayout = QHBoxLayout()
        dieLabel = QLabel("Die Description:")
        dieLabel.setMinimumWidth(100)
        self.dieCombo = QComboBox()
        self.dieCombo.setEnabled(False)  # Deshabilitado hasta que se seleccione un part
        dieLayout.addWidget(dieLabel)
        dieLayout.addWidget(self.dieCombo)
        contentLayout.addLayout(dieLayout)
        
        # Conectar señales después de crear todos los combos
        self.inchCombo.currentIndexChanged.connect(self.onInchChanged)
        self.partCombo.currentIndexChanged.connect(self.onPartChanged)
        
        # Cargar datos iniciales
        self.loadInches()
        
        # Inner
        innerLayout = QHBoxLayout()
        innerLabel = QLabel("Inner:")
        innerLabel.setMinimumWidth(100)
        self.innerSpin = QDoubleSpinBox()
        self.innerSpin.setDecimals(3)
        self.innerSpin.setRange(0, 999.999)
        innerLayout.addWidget(innerLabel)
        innerLayout.addWidget(self.innerSpin)
        contentLayout.addLayout(innerLayout)
        
        # Outer
        outerLayout = QHBoxLayout()
        outerLabel = QLabel("Outer:")
        outerLabel.setMinimumWidth(100)
        self.outerSpin = QDoubleSpinBox()
        self.outerSpin.setDecimals(3)
        self.outerSpin.setRange(0, 999.999)
        outerLayout.addWidget(outerLabel)
        outerLayout.addWidget(self.outerSpin)
        contentLayout.addLayout(outerLayout)
        
        # Status
        statusLayout = QHBoxLayout()
        statusLabel = QLabel("Status:")
        statusLabel.setMinimumWidth(100)
        self.statusCombo = QComboBox()
        self.loadStatus()
        statusLayout.addWidget(statusLabel)
        statusLayout.addWidget(self.statusCombo)
        contentLayout.addLayout(statusLayout)
        
        mainLayout.addWidget(contentFrame)
        
        # Botones
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        
        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")
        
        self.saveButton.clicked.connect(self.saveSerial)  # Cambiado de accept a saveSerial
        self.cancelButton.clicked.connect(self.reject)
        
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.cancelButton)
        mainLayout.addLayout(buttonLayout)

    def loadInches(self):
        """Carga los inches en el combo"""
        inches = self.model.getAllInches()
        self.inchCombo.clear()
        self.inchCombo.addItem("Select Inch", None)
        for inch in inches:
            self.inchCombo.addItem(str(inch['Inch']), inch['id_inch'])

    def loadParts(self, inch_id: int):
        """Carga las parts en el combo basado en el inch seleccionado"""
        parts = self.model.getPartsByInch(inch_id) if inch_id else []
        self.partCombo.clear()
        self.partCombo.addItem("Select Part", None)
        for part in parts:
            self.partCombo.addItem(part['Part'], part['id_part'])

    def loadDescriptions(self, inch_id: int, part_id: int):
        """Carga las descripciones en el combo basado en el inch y part seleccionados"""
        descriptions = self.model.getDescriptionsByInchAndPart(inch_id, part_id) if inch_id and part_id else []
        self.dieCombo.clear()
        self.dieCombo.addItem("Select Description", None)
        for desc in descriptions:
            self.dieCombo.addItem(desc['Die_Description'], desc['id_die_description'])

    def onInchChanged(self, index: int):
        """Maneja el cambio de selección en el combo de inches"""
        inch_id = self.inchCombo.currentData()
        self.partCombo.setEnabled(bool(inch_id))
        self.dieCombo.setEnabled(False)
        self.loadParts(inch_id)
        self.dieCombo.clear()
        self.dieCombo.addItem("Select Description", None)

    def onPartChanged(self, index: int):
        """Maneja el cambio de selección en el combo de parts"""
        inch_id = self.inchCombo.currentData()
        part_id = self.partCombo.currentData()
        self.dieCombo.setEnabled(bool(inch_id and part_id))
        self.loadDescriptions(inch_id, part_id)

    def loadStatus(self):
        """Carga los status en el combo"""
        status_list = self.model.getAllStatus()
        self.statusCombo.clear()
        self.statusCombo.addItem("Select Status", None)
        for status in status_list:
            self.statusCombo.addItem(status['Status'], status['id_status'])

    def loadSerialData(self):
        """Carga los datos del serial a editar"""
        serial_data = self.model.getSerialById(self.serial_id)
        if serial_data:
            self.serialInput.setText(serial_data['Serial'])
            
            # Obtener los datos del die description para seleccionar inch y part
            die_id = serial_data['id_die_description']
            die_data = self.model.getDieDescriptionById(die_id)
            if die_data:
                # Seleccionar Inch
                inch_index = self.inchCombo.findData(die_data['id_inch'])
                if inch_index >= 0:
                    self.inchCombo.setCurrentIndex(inch_index)
                    # Cargar y seleccionar Part
                    self.loadParts(die_data['id_inch'])
                    part_index = self.partCombo.findData(die_data['id_part'])
                    if part_index >= 0:
                        self.partCombo.setCurrentIndex(part_index)
                        # Cargar y seleccionar Description
                        self.loadDescriptions(die_data['id_inch'], die_data['id_part'])
                        die_index = self.dieCombo.findData(die_id)
                        if die_index >= 0:
                            self.dieCombo.setCurrentIndex(die_index)
                
            self.innerSpin.setValue(float(serial_data['inner']))
            self.outerSpin.setValue(float(serial_data['outer']))
            
            # Seleccionar Status
            index = self.statusCombo.findData(serial_data['id_status'])
            if index >= 0:
                self.statusCombo.setCurrentIndex(index)

    def _convert_to_upper(self, text):
        """Convierte el texto a mayúsculas y actualiza el campo"""
        cursor_pos = self.serialInput.cursorPosition()
        self.serialInput.setText(text.upper())
        self.serialInput.setCursorPosition(cursor_pos)

    def saveSerial(self):
        """Valida y guarda los datos del serial"""
        serial = self.serialInput.text().strip().upper()  # Asegurar que esté en mayúsculas
        die_id = self.dieCombo.currentData()
        inner = self.innerSpin.value()
        outer = self.outerSpin.value()
        status_id = self.statusCombo.currentData()
        
        # Validaciones
        if not serial:
            QMessageBox.warning(self, "Validation Error", "Serial number is required")
            self.serialInput.setFocus()
            return
            
        if not die_id:
            QMessageBox.warning(self, "Validation Error", "Please select a Die Description")
            self.dieCombo.setFocus()
            return
            
        if not status_id:
            QMessageBox.warning(self, "Validation Error", "Please select a Status")
            self.statusCombo.setFocus()
            return
            
        success = False
        if self.serial_id:  # Editar
            success = self.model.updateSerial(self.serial_id, serial, die_id, 
                                            inner, outer, status_id)
        else:  # Nuevo
            success = self.model.createSerial(serial, die_id, inner, outer, status_id)
            
        if success:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", 
                              "Could not save serial. Please verify that the serial number is not already in use.") 