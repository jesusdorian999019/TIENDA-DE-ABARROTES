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
    stock: int
    min_stock: int
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
    quantity: int
    unit_price: float
    total: float
    date: str
    time: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return asdict(self)
    
    @staticmethod
    def from_dict(data: dict):
        return Sale(**data)
