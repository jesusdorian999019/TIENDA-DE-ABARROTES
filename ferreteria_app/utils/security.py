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
        """
        try:
            # Usar bcrypt si está disponible
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception:
            # Fallback a hashlib si bcrypt falla
            return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verifica una contraseña contra su hash.
        
        Args:
            password: Contraseña en texto plano
            hashed_password: Contraseña hasheada
            
        Returns:
            True si la contraseña es correcta, False en caso contrario
        """
        try:
            # Intentar con bcrypt primero
            if hashed_password.startswith('$2'):
                return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
            else:
                # Fallback a hashlib
                return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed_password
        except Exception:
            return False
