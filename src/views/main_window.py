from PyQt5.QtWidgets import (QMainWindow, QMdiArea, QMenuBar, QMenu, 
                            QAction, QApplication, QLabel, QWidget, QVBoxLayout, QMdiSubWindow, QHBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import os
from .users_window import UsersWindow

class MainWindow(QMainWindow):
    def __init__(self, user_info=None):
        super().__init__()
        self.user_info = user_info
        self.setWindowTitle("Die Control System - MasterNet")
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QMenuBar {
                font-size: 12px;
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
            }
            QMenuBar::item {
                padding: 8px 12px;
                margin: 0px;
            }
            QMenuBar::item:selected {
                background-color: #e9ecef;
            }
            QMenu {
                font-size: 12px;
                background-color: white;
                border: 1px solid #dee2e6;
                padding: 5px;
            }
            QMenu::item {
                padding: 6px 25px 6px 20px;
                border-radius: 3px;
                margin: 2px;
            }
            QMenu::item:selected {
                background-color: #e9ecef;
                font-weight: bold;
            }
            QMenu::separator {
                height: 1px;
                background-color: #dee2e6;
                margin: 5px 0px;
            }
            QLabel#workerName {
                font-size: 16px;
                font-weight: bold;
                color: #0056b3;
                padding: 5px 15px;
                letter-spacing: 0.5px;
            }
        """)
        
        # Establecer el ícono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Widget central para contener el logo y el área MDI
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout vertical para el widget central
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear widget para el encabezado (logo y nombre del trabajador)
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 5, 10, 5)
        
        # Agregar el nombre del trabajador si está disponible
        if self.user_info and 'worker_name' in self.user_info:
            worker_label = QLabel(f"User:  {self.user_info['worker_name']}")
            worker_label.setObjectName("workerName")
            header_layout.addWidget(worker_label)
        
        # Agregar espacio flexible
        header_layout.addStretch()
        
        # Configurar el logo
        self.logo_label = QLabel()
        self.setup_logo()
        header_layout.addWidget(self.logo_label)
        
        # Agregar el encabezado al layout principal
        layout.addWidget(header_widget)
        
        # Configurar el área MDI
        self.mdi_area = QMdiArea()
        self.mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setBackground(Qt.white)  # Fondo blanco para el área MDI
        layout.addWidget(self.mdi_area)
        
        # Crear menú
        self.create_menu()
        
        # Configurar ventana
        self.setMinimumSize(800, 600)
        self.showMaximized()

    def create_menu(self):
        menubar = self.menuBar()
        
        # Crear menú Database
        database_menu = menubar.addMenu("Database")
        database_menu.setStyleSheet("QMenu { font-size: 12px; }")
        
        # Crear submenú Users
        users_menu = QMenu("Users", self)
        users_menu.setStyleSheet("QMenu { font-size: 12px; }")
        database_menu.addMenu(users_menu)
        
        # Crear acciones para el menú Users
        manage_users_action = QAction("Manage Users", self)
        manage_users_action.triggered.connect(self.show_users_window)
        
        positions_action = QAction("Positions", self)
        positions_action.triggered.connect(self.show_positions_window)
        
        workers_action = QAction("Workers", self)
        workers_action.triggered.connect(self.show_workers_window)
        
        roles_action = QAction("Roles", self)
        roles_action.triggered.connect(self.show_roles_window)
        
        # Agregar acciones al menú Users
        users_menu.addAction(manage_users_action)
        users_menu.addAction(positions_action)
        users_menu.addAction(workers_action)
        users_menu.addAction(roles_action)
        
        users_menu.addSeparator()  # Agregar separador
        
        # Crear submenú Dies
        dies_menu = database_menu.addMenu("Dies")
        
        # Acción Manage Dies
        manage_dies_action = QAction("Manage Dies", self)
        manage_dies_action.triggered.connect(self.show_dies_window)
        dies_menu.addAction(manage_dies_action)

    def setup_logo(self):
        # Configurar el logo
        logo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'logo_masternet.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            # Escalar el logo a un tamaño apropiado
            scaled_pixmap = pixmap.scaled(360, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(scaled_pixmap)
            self.logo_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.logo_label.setStyleSheet("background-color: transparent; padding: 5px;")
            self.logo_label.setFixedSize(scaled_pixmap.size())

    def show_users_window(self):
        # Crear y mostrar la ventana de usuarios
        users_window = UsersWindow()
        sub_window = self.mdi_area.addSubWindow(users_window)
        sub_window.show()

    def show_positions_window(self):
        # Crear y mostrar la ventana de posiciones
        from .positions_window import PositionsWindow
        positions_window = PositionsWindow()
        sub_window = self.mdi_area.addSubWindow(positions_window)
        sub_window.show()

    def show_workers_window(self):
        """Muestra la ventana de gestión de trabajadores"""
        from views.workers_window import WorkersWindow
        workers_window = WorkersWindow()
        self.mdi_area.addSubWindow(workers_window)
        workers_window.show()

    def show_dies_window(self):
        # Implementar la lógica para mostrar la ventana de gestión de díes
        pass

    def show_roles_window(self):
        """Muestra la ventana de roles en el área MDI"""
        from views.roles_window import RolesWindow
        roles_window = RolesWindow()
        sub_window = QMdiSubWindow()
        sub_window.setWidget(roles_window)
        sub_window.setAttribute(Qt.WA_DeleteOnClose)
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show() 