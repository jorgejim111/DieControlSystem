import sys
from PyQt5.QtWidgets import QApplication
from views.login_window import LoginWindow
from views.main_window import MainWindow
from models.user_model import UserModel

def main():
    app = QApplication(sys.argv)
    
    # Mostrar ventana de login
    login = LoginWindow()
    if login.exec_() == LoginWindow.Accepted:
        # Si el login es exitoso, obtener datos del usuario
        user_data = login.get_user_data()
        
        # Obtener información completa del usuario incluyendo el worker
        user_model = UserModel()
        user_info = user_model.get_user_by_id(user_data['id_user'])
        
        # Mostrar ventana principal
        window = MainWindow(user_info)
        window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main() 