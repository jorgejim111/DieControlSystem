// Gestión de ventanas MDI
class MDIWindow {
    constructor(id, title, content) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.isMaximized = false;
        this.isMinimized = false;
        this.createWindow();
    }

    createWindow() {
        const window = document.createElement('div');
        window.className = 'mdi-window';
        window.id = `window-${this.id}`;
        window.innerHTML = `
            <div class="mdi-window-header">
                <h5 class="mdi-window-title">${this.title}</h5>
                <div class="mdi-window-controls">
                    <button class="mdi-window-control minimize" title="Minimizar">
                        <i class="fas fa-window-minimize"></i>
                    </button>
                    <button class="mdi-window-control maximize" title="Maximizar">
                        <i class="fas fa-window-maximize"></i>
                    </button>
                    <button class="mdi-window-control close" title="Cerrar">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            <div class="mdi-window-body">
                ${this.content}
            </div>
        `;

        document.getElementById('mdi-container').appendChild(window);
        this.setupEventListeners(window);
        this.makeWindowDraggable(window);
    }

    setupEventListeners(window) {
        const controls = window.querySelector('.mdi-window-controls');
        
        controls.querySelector('.minimize').addEventListener('click', () => this.minimize(window));
        controls.querySelector('.maximize').addEventListener('click', () => this.maximize(window));
        controls.querySelector('.close').addEventListener('click', () => this.close(window));
    }

    makeWindowDraggable(window) {
        const header = window.querySelector('.mdi-window-header');
        let isDragging = false;
        let currentX;
        let currentY;
        let initialX;
        let initialY;
        let xOffset = 0;
        let yOffset = 0;

        header.addEventListener('mousedown', (e) => {
            if (!this.isMaximized) {
                isDragging = true;
                initialX = e.clientX - xOffset;
                initialY = e.clientY - yOffset;
            }
        });

        document.addEventListener('mousemove', (e) => {
            if (isDragging) {
                e.preventDefault();
                currentX = e.clientX - initialX;
                currentY = e.clientY - initialY;
                xOffset = currentX;
                yOffset = currentY;
                window.style.transform = `translate(${currentX}px, ${currentY}px)`;
            }
        });

        document.addEventListener('mouseup', () => {
            isDragging = false;
        });
    }

    minimize(window) {
        if (this.isMaximized) {
            this.maximize(window); // Restaurar primero si está maximizada
        }
        window.classList.toggle('minimized');
        this.isMinimized = !this.isMinimized;
        this.updateTaskbar();
    }

    maximize(window) {
        window.classList.toggle('maximized');
        this.isMaximized = !this.isMaximized;
        if (!this.isMaximized) {
            window.style.transform = 'none';
        }
    }

    close(window) {
        window.remove();
        this.removeFromTaskbar();
    }

    updateTaskbar() {
        // Implementar la actualización de la barra de tareas
    }

    removeFromTaskbar() {
        // Implementar la eliminación de la barra de tareas
    }
}

// Función para abrir un nuevo módulo
function openModule(moduleName) {
    // Cargar el contenido del módulo mediante AJAX
    fetch(`/module/${moduleName}`)
        .then(response => response.text())
        .then(content => {
            const title = getModuleTitle(moduleName);
            new MDIWindow(moduleName, title, content);
        })
        .catch(error => {
            console.error('Error al cargar el módulo:', error);
            alert('Error al cargar el módulo. Por favor, intente nuevamente.');
        });
}

// Función para obtener el título del módulo
function getModuleTitle(moduleName) {
    const titles = {
        'inches': 'Pulgadas',
        'parts': 'Partes',
        'descriptions': 'Descripciones',
        'products': 'Productos',
        'lines': 'Líneas',
        'die_descriptions': 'Descripciones de Troqueles',
        'serials': 'Seriales',
        'users': 'Usuarios',
        'roles': 'Roles',
        'permissions': 'Permisos',
        'positions': 'Puestos',
        'workers': 'Trabajadores',
        'profile': 'Mi Perfil'
    };
    return titles[moduleName] || 'Ventana';
}

// Inicialización cuando el documento está listo
document.addEventListener('DOMContentLoaded', () => {
    // Crear la barra de tareas
    const taskbar = document.createElement('div');
    taskbar.className = 'mdi-taskbar';
    document.body.appendChild(taskbar);
}); 