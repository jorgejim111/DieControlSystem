from PyQt5.QtWidgets import (QMainWindow, QMdiArea, QMenuBar, QMenu, 
                            QAction, QApplication, QLabel, QWidget, QVBoxLayout, QMdiSubWindow, QFrame, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import os
from .users_window import UsersWindow
from views.positions_window import PositionsWindow
from views.workers_window import WorkersWindow
from views.roles_window import RolesWindow

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user  # Guardar el usuario actual
        self.setWindowTitle("Die Control System")
        
        # Establecer el ícono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icono.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Frame superior para el título, nombre del trabajador y logo
        top_frame = QFrame()
        top_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: none;
                padding: 5px;
            }
            QLabel {
                background: transparent;
            }
        """)
        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(5, 5, 5, 5)
        
        # Nombre del trabajador
        worker_name = self.user.get('worker_name', 'No Worker Assigned')
        worker_label = QLabel(worker_name)
        worker_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #333; border: none; background: transparent;")
        top_layout.addWidget(worker_label)
        
        # Agregar espaciador entre el nombre y el logo
        top_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'logo_masternet.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(216, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Doble del tamaño original
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        top_layout.addWidget(logo_label)
        
        main_layout.addWidget(top_frame)
        
        # Frame principal para el contenido
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 20px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Configurar el área MDI
        self.mdi_area = QMdiArea()
        self.mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setBackground(Qt.white)
        content_layout.addWidget(self.mdi_area)
        
        main_layout.addWidget(content_frame)
        
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

    def show_users_window(self):
        # Crear y mostrar la ventana de usuarios
        users_window = UsersWindow()
        sub_window = self.mdi_area.addSubWindow(users_window)
        sub_window.show()

    def show_positions_window(self):
        # Crear y mostrar la ventana de posiciones
        positions_window = PositionsWindow()
        sub_window = self.mdi_area.addSubWindow(positions_window)
        sub_window.show()

    def show_workers_window(self):
        """Muestra la ventana de gestión de trabajadores"""
        workers_window = WorkersWindow()
        self.mdi_area.addSubWindow(workers_window)
        workers_window.show()

    def show_dies_window(self):
        # Implementar la lógica para mostrar la ventana de gestión de díes
        pass

    def show_roles_window(self):
        """Muestra la ventana de roles en el área MDI"""
        roles_window = RolesWindow()
        sub_window = QMdiSubWindow()
        sub_window.setWidget(roles_window)
        sub_window.setAttribute(Qt.WA_DeleteOnClose)
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show() 