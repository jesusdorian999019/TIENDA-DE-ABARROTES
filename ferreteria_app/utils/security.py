import bcrypt
import hashlib


class SecurityManager:
    """Gestor de seguridad para contraseñas y autenticación."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashea una contraseña usando bcrypt.
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Contraseña hasheada
            
        Raises:
            Exception: Si bcrypt no está disponible o falla
        """
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verifica una contraseña contra su hash usando bcrypt.
        
        Args:
            password: Contraseña en texto plano
            hashed_password: Contraseña hasheada con bcrypt
            
        Returns:
            True si la contraseña es correcta, False en caso contrario
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False
