from pydantic import BaseModel


# Product data shape used to validate API input and format API responses.
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int


# Fields accepted when updating a product; its ID is supplied separately.
class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
