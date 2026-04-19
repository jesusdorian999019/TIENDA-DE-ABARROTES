import os
from pathlib import Path

# Rutas base - Compatible con .exe compilado y código fuente
if getattr(os, 'frozen', False):
    # Si es ejecutable compilado con PyInstaller
    BASE_DIR = Path(os.path.dirname(os.path.abspath(os.sys.executable))).parent
else:
    # Si es código fuente
    BASE_DIR = Path(__file__).parent.parent

# Crear data_storage en la ruta del ejecutable o código
DATA_DIR = BASE_DIR / "data_storage"

# Asegurar que exista el directorio de datos
DATA_DIR.mkdir(exist_ok=True)

# Rutas de archivos JSON
USERS_FILE = DATA_DIR / "users.json"
PRODUCTS_FILE = DATA_DIR / "products.json"
SALES_FILE = DATA_DIR / "sales.json"

# Configuración de la aplicación
APP_TITLE = "Gestión de Ferretería"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_GEOMETRY = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+100+100"

# Configuración de colores
PRIMARY_COLOR = "#2c3e50"
SECONDARY_COLOR = "#3498db"
SUCCESS_COLOR = "#27ae60"
WARNING_COLOR = "#e74c3c"
LIGHT_BG = "#ecf0f1"
TEXT_COLOR = "#2c3e50"

# Configuración de usuario de demostración
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"  # Se hasheará al crear

# Categorías predeterminadas
PRODUCT_CATEGORIES = [
    "Herramientas",
    "Electricidad",
    "Plomería",
    "Construcción",
    "Pintura",
    "Tornillos y Tuercas",
    "Otro"
]

# Configuración de exportación
EXCEL_DATE_FORMAT = "dd/mm/yyyy"
EXCEL_NUMBER_FORMAT = "0.00"
