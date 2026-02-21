from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Section A — User Models
class UserCreate(BaseModel):
    """
    Request schema for creating a user
    """
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$', description="User's phone number")
    address: Optional[str] = Field(None, max_length=200, description="User's address")

class UserResponse(BaseModel):
    """
    Response schema for user data
    """
    id: Optional[str] = Field(None, alias="_id", description="MongoDB document ID")
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True

# Section B — Product Models
class ProductCreate(BaseModel):
    """
    Request schema for creating a product
    """
    sku: str = Field(..., min_length=3, max_length=50, description="Stock Keeping Unit - unique identifier")
    name: str = Field(..., min_length=2, max_length=200, description="Product name")
    price: float = Field(..., gt=0, description="Product price (must be greater than 0)")
    stock: int = Field(..., ge=0, description="Available stock quantity (must be 0 or greater)")
    description: Optional[str] = Field(None, max_length=1000, description="Product description")

class ProductResponse(BaseModel):
    """
    Response schema for product data
    """
    id: Optional[str] = Field(None, alias="_id", description="MongoDB document ID")
    sku: str
    name: str
    price: float
    stock: int
    description: Optional[str] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True