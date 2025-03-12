# DieControlSystem - Guía de Desarrollo

## Contexto del Proyecto
Sistema de control y gestión para Die Control System, desarrollado en Python con PyQt5 y MySQL.

## Estándares de Diseño

### 1. Interfaz de Usuario
#### Ventanas Principales
- Heredan de `QMainWindow`
- Tamaño mínimo: 1000x600
- Estructura:
  * Frame superior con título y logo de Masternet
  * Frame principal con contenido
  * Barra de herramientas con botones principales

#### Elementos Visuales
- **Frame Superior**:
  * Fondo blanco
  * Borde: #cccccc
  * Título: 16px, negrita, color #333
  * Logo Masternet: 108x30px

- **Frame Principal**:
  * Fondo blanco
  * Borde: #cccccc
  * Radio de borde: 5px
  * Padding: 10px

- **Tablas**:
  * Encabezados: #f8f9fa
  * Bordes: #dee2e6
  * Selección de fila completa
  * Columna de acciones (ancho fijo: 100px)
  * Botones de acción en fila:
    - Editar: ✏️ (amarillo #ffc107)
    - Eliminar: ❌ (rojo #dc3545)

- **Botones Principales**:
  * Color principal: #0056b3
  * Color hover: #003d80
  * Botón eliminar: #dc3545
  * Padding: 8px 15px
  * Radio de borde: 3px
  * Ancho mínimo: 100px

### 2. Diálogos
- Heredan de `QDialog`
- Modal: True
- Ancho mínimo: 400px
- Campos:
  * Labels: ancho mínimo 80px
  * Inputs: padding 5px, borde #cccccc
  * Validación antes de guardar
- Botones:
  * Save: azul (#0056b3)
  * Cancel: gris (#6c757d)

### 3. Arquitectura
#### Estructura de Carpetas
```
src/
├── models/         # Modelos de datos
├── views/          # Interfaces de usuario
├── database/       # Conexión y queries
└── assets/         # Recursos (iconos, imágenes)
```

#### Patrones
- MVC (Model-View-Controller)
- Singleton para conexión DB
- Validación en modelos y vistas

### 4. Base de Datos
#### Tablas Implementadas
- `users`: Gestión de usuarios
- `positions`: Cargos/posiciones
- `workers`: Trabajadores
- `rols`: Roles del sistema

## Estado Actual
### Módulos Completados
1. Gestión de Usuarios
2. Gestión de Posiciones
3. Gestión de Roles
4. Gestión de Trabajadores

### En Desarrollo
- Sistema de jerarquía de roles y tareas:
  * Tabla `role_hierarchy`
  * Tabla `tasks`
  * Tabla `role_tasks`

## Próximos Pasos
1. Implementar sistema de tareas por rol
2. Desarrollar jerarquía de roles
3. Integrar permisos basados en roles

## Notas Importantes
- Mantener consistencia en nombrado (CamelCase para clases, snake_case para métodos)
- Documentar métodos y clases
- Manejar errores con mensajes claros al usuario
- Validar datos antes de operaciones DB
- Actualizar este prompt al final de cada sesión de desarrollo 