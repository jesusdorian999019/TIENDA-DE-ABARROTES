from dataclasses import dataclass, asdict, field
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """Modelo de usuario."""
    id: str
    username: str
    password_hash: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return asdict(self)
    
    @staticmethod
    def from_dict(data: dict):
        return User(**data)


@dataclass
class Product:
    """Modelo de producto."""
    id: str
    name: str
    category: str
    code: str
    provider: str
    purchase_price: float
    sale_price: float
    stock: float  # Cambiado a float para permitir ventas por kilo
    min_stock: float  # Cambiado a float para permitir decimales
    # Nuevos campos para ferretería grande (v1.0.2)
    marca: str = ""  # Marca del producto
    unidad: str = "UNIDAD"  # UNIDAD, KILO, METRO, LITRO, etc.
    flexible_stock: bool = False  # True = permite decimales (por kilo)
    equivalente_sunat: str = ""  # Código SUNAT para Perú
    tipo_igv: str = ""  # Gravado, Exonerado, Inafecto
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return asdict(self)
    
    @staticmethod
    def from_dict(data: dict):
        return Product(**data)


@dataclass
class Sale:
    """Modelo de venta."""
    id: str
    product_id: str
    product_name: str
    quantity: float  # Cambiado a float para permitir ventas por kilo
    unit_price: float  # Precio de venta unitario
    total: float
    # Nuevos campos para control de ganancias (v1.0.2)
    purchase_price: float = 0.0  # Precio de compra al momento de la venta
    unidad: str = "UNIDAD"  # UNIDAD, KILO, etc.
    date: str = ""
    time: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return asdict(self)
    
    @staticmethod
    def from_dict(data: dict):
        return Sale(**data)
