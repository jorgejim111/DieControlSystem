# Die Control System - Historial de Desarrollo

## Versiones Estables (Git)

### Versión Actual (Serial Management)
- Implementación completa del módulo de Seriales
- Ventana principal de Seriales con tabla y acciones
- Diálogo para agregar/editar seriales con estilos consistentes
- Integración con Die Descriptions y selección en cascada
- Validación de datos y manejo de duplicados
- Conversión automática a mayúsculas
- Filtrado inteligente de inches activos

### Versión Anterior (aabf1de)
- Implementación completa del módulo Die Description
- Ventana principal de Die Descriptions con tabla y acciones
- Diálogo para agregar/editar die descriptions
- Integración en el menú principal bajo Database
- Submenús para Inches, Parts y Description
- Validación de datos y manejo de duplicados
- Interfaz consistente con el diseño general

### Historial Completo
```
[nuevo-hash] - Implementación completa del módulo de Seriales
aabf1de - Implementación completa del módulo Die Description
a9ef948 - Implementación inicial del módulo Die Description
b43a806 - Mejoras en la interfaz de usuario
e112cb2 - Merge de cambios remotos
8e7e12a - Commit inicial
```

## Cómo Restaurar Versiones

### Ver una versión anterior (sin perder cambios actuales)
```bash
git checkout [hash]
# Ejemplo: git checkout aabf1de
```

### Regresar completamente a una versión anterior (descarta cambios posteriores)
```bash
git reset --hard [hash]
# Ejemplo: git reset --hard aabf1de
```

### Notas importantes
1. Usar `git checkout` es seguro pues no elimina cambios
2. `git reset --hard` es permanente y elimina cambios posteriores
3. Si hay cambios sin commitear, usar `git stash` antes de hacer checkout

## Estructura del Proyecto

### Módulos Principales
1. **Login y Autenticación**
   - Ventana de login mejorada
   - Validación de credenciales
   - Manejo de sesiones

2. **Gestión de Usuarios**
   - Manage Users
   - Positions
   - Workers
   - Roles

3. **Die Description**
   - Manage Die Description
   - Inches
   - Parts
   - Description

### Tecnologías
- Python con PyQt5 para la interfaz gráfica
- MySQL para la base de datos
- Git para control de versiones

### Estándares de Diseño
- Tema oscuro consistente
- Botones y controles estandarizados
- Validación de datos en tiempo real
- Mensajes de error informativos
- Interfaz responsiva y adaptable

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
- Gestión de Seriales:
  * Ventana principal de Seriales con tabla y acciones
  * Diálogo para agregar/editar seriales
  * Integración con Die Descriptions
  * Selección en cascada (Inch -> Part -> Description)
  * Validación de datos y manejo de duplicados
  * Conversión automática a mayúsculas
  * Filtrado inteligente de inches activos
  * Interfaz consistente con el diseño general

## Próximos Pasos
1. Implementar sistema de tareas por rol
2. Desarrollar jerarquía de roles
3. Integrar permisos basados en roles
4. Expandir funcionalidades del módulo de Seriales

## Notas Importantes
- Mantener consistencia en nombrado (CamelCase para clases, snake_case para métodos)
- Documentar métodos y clases
- Manejar errores con mensajes claros al usuario
- Validar datos antes de operaciones DB
- Actualizar este prompt al final de cada sesión de desarrollo
- Usar backticks en columnas SQL que usan palabras reservadas
- Mantener consistencia en estilos de diálogos y botones