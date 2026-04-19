from typing import Optional, Tuple
from data.models import User
from data.json_manager import JsonManager
from utils.security import SecurityManager
from utils.validators import Validators


class UserService:
    """Servicio de gestión de usuarios."""
    
    def __init__(self, data_manager=None):
        """Inicializa el servicio de usuarios."""
        self.data_manager = data_manager or JsonManager()
        self.security = SecurityManager()
        self.validators = Validators()
    
    def create_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Crea un nuevo usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            Tupla (éxito, mensaje)
        """
        # Validar entrada
        valid, msg = self.validators.validate_username(username)
        if not valid:
            return False, msg
        
        valid, msg = self.validators.validate_password(password)
        if not valid:
            return False, msg
        
        # Verificar que no exista
        if self.data_manager.user_exists(username):
            return False, "El usuario ya existe"
        
        # Crear usuario
        password_hash = self.security.hash_password(password)
        user = User(
            id="",  # Se generará en el data manager
            username=username,
            password_hash=password_hash
        )
        
        if self.data_manager.create_user(user):
            return True, "Usuario creado exitosamente"
        else:
            return False, "Error al crear usuario"
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Autentica un usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            Tupla (éxito, mensaje)
        """
        user = self.data_manager.get_user_by_username(username)
        
        if not user:
            return False, "Usuario o contraseña incorrectos"
        
        if self.security.verify_password(password, user.password_hash):
            return True, "Autenticación exitosa"
        else:
            return False, "Usuario o contraseña incorrectos"
    
    def get_user(self, username: str) -> Optional[User]:
        """Obtiene un usuario por nombre."""
        return self.data_manager.get_user_by_username(username)
    
    def initialize_default_user(self) -> bool:
        """Inicializa usuario administrador por defecto."""
        from config.settings import DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD
        
        if self.data_manager.user_exists(DEFAULT_ADMIN_USERNAME):
            return True  # Ya existe
        
        success, _ = self.create_user(DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD)
        return success
