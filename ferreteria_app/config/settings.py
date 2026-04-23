import os
import sys
from pathlib import Path

# Determinar la carpeta base
if getattr(sys, 'frozen', False):
    # Es ejecutable compilado - usar la carpeta del .exe real
    BASE_DIR = Path(sys.executable).parent
else:
    # Es código fuente - usar la carpeta del proyecto
    BASE_DIR = Path(__file__).parent.parent

# Crear data_storage en la misma carpeta
DATA_DIR = BASE_DIR / "data_storage"
DATA_DIR.mkdir(exist_ok=True)

# Rutas de archivos JSON
USERS_FILE = DATA_DIR / "users.json"
PRODUCTS_FILE = DATA_DIR / "products.json"
SALES_FILE = DATA_DIR / "sales.json"

# Configuración de la aplicación
APP_TITLE = "Gestión de Ferretería"
APP_VERSION = "1.0.0"

# GitHub update settings - CONFIGURAR ESTO PARA ACTUALIZACIONES
GITHUB_OWNER = "jesusdorian999019"  # Usuario de GitHub
GITHUB_REPO = "TIENDA-DE-ABARROTES"  # Nombre del repo
GITHUB_BRANCH = "main"

# Configuración de ventana
WINDOW_GEOMETRY = "1000x700+100+100"
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

# Colores
PRIMARY_COLOR = "#1e3a5f"
SECONDARY_COLOR = "#2c3e50"
LIGHT_BG = "#f5f5f5"
TEXT_COLOR = "#333333"
SUCCESS_COLOR = "#27ae60"
WARNING_COLOR = "#e74c3c"

# Configuración de seguridad
PASSWORD_ROUNDS = 12

# Usuario y contraseña por defecto
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"

# Categorías de productos
PRODUCT_CATEGORIES = [
    "Herramientas",
    "Pinturas",
    "Fijaciones",
    "Electricidad",
    "Fontanería",
    "Madera",
    "Metal",
    "Jardinería",
    "Automotriz",
    "Otros"
]