import re
from decimal import Decimal
from typing import Tuple


class Validators:
    """Validadores para datos de la aplicación."""
    
    @staticmethod
    def validate_product_name(name: str) -> Tuple[bool, str]:
        """Valida nombre de producto."""
        if not name or len(name.strip()) == 0:
            return False, "El nombre del producto es requerido"
        if len(name) > 100:
            return False, "El nombre no puede exceder 100 caracteres"
        return True, ""
    
    @staticmethod
    def validate_code(code: str) -> Tuple[bool, str]:
        """Valida código de producto."""
        if not code or len(code.strip()) == 0:
            return False, "El código es requerido"
        if len(code) > 50:
            return False, "El código no puede exceder 50 caracteres"
        return True, ""
    
    @staticmethod
    def validate_price(price: str) -> Tuple[bool, str]:
        """Valida un precio."""
        try:
            p = Decimal(price)
            if p < 0:
                return False, "El precio no puede ser negativo"
            return True, ""
        except:
            return False, "El precio debe ser un número válido"
    
    @staticmethod
    def validate_quantity(quantity: str) -> Tuple[bool, str]:
        """Valida una cantidad - ahora permite decimales para ventas por kilo."""
        try:
            q = float(quantity)  # Cambiado a float para permitir decimales
            if q < 0:
                return False, "La cantidad no puede ser negativa"
            return True, ""
        except:
            return False, "La cantidad debe ser un número válido"

    @staticmethod
    def validate_min_stock(min_stock: str) -> Tuple[bool, str]:
        """Valida stock mínimo - ahora permite decimales."""
        try:
            q = float(min_stock)  # Cambiado a float para permitir decimales
            if q < 0:
                return False, "El stock mínimo no puede ser negativo"
            return True, ""
        except:
            return False, "El stock mínimo debe ser un número válido"
    
    @staticmethod
    def validate_category(category: str) -> Tuple[bool, str]:
        """Valida categoría."""
        if not category or len(category.strip()) == 0:
            return False, "La categoría es requerida"
        return True, ""
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """Valida nombre de usuario."""
        if not username or len(username.strip()) == 0:
            return False, "El nombre de usuario es requerido"
        if len(username) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres"
        if len(username) > 30:
            return False, "El nombre de usuario no puede exceder 30 caracteres"
        if not re.match("^[a-zA-Z0-9_-]+$", username):
            return False, "El nombre de usuario solo puede contener letras, números, guiones y guiones bajos"
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Valida contraseña."""
        if not password or len(password) == 0:
            return False, "La contraseña es requerida"
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        return True, ""
    
    @staticmethod
    def validate_provider(provider: str) -> Tuple[bool, str]:
        """Valida nombre de proveedor."""
        if not provider or len(provider.strip()) == 0:
            return False, "El proveedor es requerido"
        if len(provider) > 100:
            return False, "El proveedor no puede exceder 100 caracteres"
        return True, ""
