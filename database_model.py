from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

# Base class for SQLAlchemy models (Python classes mapped to database tables).
Base = declarative_base()


# Defines the columns and types for the product table in the database.
class Product(Base):
    __tablename__ = "product"

    # Primary key uniquely identifying each product.
    id = Column(Integer, primary_key=True, index=True)
    # Product details and inventory information.
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)