from app import app, db
from models.database import User, Role, Permission
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Crear las tablas
        db.create_all()

        # Crear rol de administrador si no existe
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(
                name='admin',
                description='Administrador del sistema'
            )
            db.session.add(admin_role)
            db.session.commit()

        # Crear usuario administrador si no existe
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                password=generate_password_hash('admin123'),
                role='admin',
                role_id=admin_role.id,
                is_active=True
            )
            db.session.add(admin_user)
            db.session.commit()

        print("Base de datos inicializada con éxito!")
        print("Usuario admin creado:")
        print("Username: admin")
        print("Password: admin123")

if __name__ == '__main__':
    init_db() 