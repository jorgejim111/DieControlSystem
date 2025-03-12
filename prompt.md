# Die Control System

## Descripción General
Sistema de control y gestión para Masternet, diseñado para administrar trabajadores, posiciones, roles y troqueles.

## Características Principales

### Sistema de Autenticación
- Ventana de login con diseño moderno
- Validación de credenciales contra base de datos MySQL
- Usuario administrador por defecto:
  - Username: admin
  - Password: admin123

### Interfaz Principal
- Diseño moderno y consistente
- Nombre del trabajador actual en tamaño 36px
- Logo de Masternet en la esquina superior derecha
- Sistema MDI (Multiple Document Interface) para gestionar múltiples ventanas
- Menú organizado por categorías

### Módulos del Sistema

#### 1. Gestión de Usuarios
- Crear, editar y eliminar usuarios
- Asignar trabajadores a usuarios
- Gestión de contraseñas seguras (hash bcrypt)
- Asignación de roles

#### 2. Gestión de Trabajadores
- Registro completo de trabajadores
- Asignación de posiciones
- Historial de cambios

#### 3. Gestión de Posiciones
- Mantenimiento de catálogo de posiciones
- Relación con trabajadores

#### 4. Gestión de Roles
- Control de roles del sistema
- Asignación de roles a usuarios
- Permisos basados en roles

#### 5. Gestión de Troqueles (Dies)
- [Módulo en desarrollo]

## Estructura de la Base de Datos

### Tablas Principales
1. `user`
   - id_user (PK)
   - username
   - email
   - password (hashed)
   - id_worker (FK)
   - create_time

2. `workers`
   - id_worker (PK)
   - name
   - id_position (FK)

3. `positions`
   - id_positions (PK)
   - position

4. `roles`
   - id_rol (PK)
   - rol

5. `roles_user`
   - id_rol (FK)
   - id_user (FK)

## Tecnologías Utilizadas

### Frontend
- PyQt5 para la interfaz gráfica
- Diseño moderno con estilos CSS
- Sistema MDI para gestión de ventanas

### Backend
- Python 3.x
- MySQL para la base de datos
- bcrypt para hash de contraseñas

### Características de la Interfaz
- Diseño consistente en todas las ventanas
- Paleta de colores corporativa
- Validaciones en tiempo real
- Mensajes de error y éxito informativos
- Interfaz responsiva

## Guía de Inicio

1. Ejecutar el sistema:
   ```bash
   python src/main.py
   ```

2. Iniciar sesión:
   - Usar credenciales de administrador por defecto
   - El sistema creará automáticamente el usuario admin si no existe

3. Navegación:
   - Usar el menú Database para acceder a todas las funciones
   - Las ventanas se abren dentro del área MDI
   - Se pueden tener múltiples ventanas abiertas simultáneamente

## Estructura del Proyecto

```
src/
├── main.py
├── database/
│   ├── connection.py
│   └── database_schema.py
├── models/
│   ├── user_model.py
│   ├── worker_model.py
│   ├── position_model.py
│   └── role_model.py
└── views/
    ├── login_window.py
    ├── main_window.py
    ├── users_window.py
    ├── workers_window.py
    ├── positions_window.py
    └── roles_window.py
```

## Mantenimiento y Desarrollo

### Agregar Nuevos Módulos
1. Crear el modelo en `src/models/`
2. Crear la vista en `src/views/`
3. Agregar la entrada en el menú principal
4. Actualizar el esquema de base de datos si es necesario

### Estándares de Código
- Usar Type Hints en Python
- Documentar métodos y clases
- Seguir PEP 8 para estilo de código
- Mantener consistencia en el diseño de UI

## Próximas Características
- Implementación completa del módulo de Troqueles
- Sistema de reportes
- Dashboard con estadísticas
- Exportación de datos
- Historial de cambios 