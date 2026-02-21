from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.database import users_collection, products_collection
from app.schemas import UserCreate, UserResponse, ProductCreate, ProductResponse
from bson import ObjectId
from typing import Dict, Any

app = FastAPI(
    title="Atlas User & Product Management API",
    description="API for managing users and products with MongoDB Atlas",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to convert MongoDB document to response model
def mongo_to_response(data: Dict[str, Any], response_model):
    if data:
        data["id"] = str(data.pop("_id"))
        return response_model(**data)
    return None

# Section A — User Endpoints

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Create a new user
    
    - Validates email uniqueness
    - Returns 400 if email already exists
    - Returns created user data
    """
    # Check if email already exists
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user.email} already exists"
        )
    
    # Insert new user
    user_dict = user.dict()
    result = users_collection.insert_one(user_dict)
    
    # Retrieve and return created user
    created_user = users_collection.find_one({"_id": result.inserted_id})
    return mongo_to_response(created_user, UserResponse)

@app.get("/users/{email}", response_model=UserResponse)
async def get_user_by_email(email: str):
    """
    Get user by email address
    
    - Returns 404 if user not found
    - Returns user data if found
    """
    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found"
        )
    
    return mongo_to_response(user, UserResponse)

# Section B — Product Endpoints

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    """
    Create a new product
    
    - Validates SKU uniqueness
    - Returns 400 if SKU already exists
    - Returns created product data
    """
    # Check if SKU already exists
    existing_product = products_collection.find_one({"sku": product.sku})
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with SKU {product.sku} already exists"
        )
    
    # Insert new product
    product_dict = product.dict()
    result = products_collection.insert_one(product_dict)
    
    # Retrieve and return created product
    created_product = products_collection.find_one({"_id": result.inserted_id})
    return mongo_to_response(created_product, ProductResponse)

@app.get("/products/{sku}", response_model=ProductResponse)
async def get_product_by_sku(sku: str):
    """
    Get product by SKU
    
    - Returns 404 if product not found
    - Returns product data if found
    """
    product = products_collection.find_one({"sku": sku})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with SKU {sku} not found"
        )
    
    return mongo_to_response(product, ProductResponse)

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running
    """
    return {"status": "healthy", "message": "API is running successfully"}

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Welcome to Atlas User & Product Management API",
        "version": "1.0.0",
        "endpoints": {
            "users": {
                "create": "POST /users",
                "get_by_email": "GET /users/{email}"
            },
            "products": {
                "create": "POST /products",
                "get_by_sku": "GET /products/{sku}"
            },
            "health": "GET /health"
        }
    }