import sys
from PyQt5.QtWidgets import QApplication
from views.login_window import LoginWindow
from views.main_window import MainWindow

def main():
    # Crear la aplicación Qt
    app = QApplication(sys.argv)
    
    # Crear y mostrar la ventana de login
    login_window = LoginWindow()
    login_window.show()
    
    # Ejecutar el bucle de eventos
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 