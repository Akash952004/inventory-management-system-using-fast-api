from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from modell import Product, ProductUpdate
from database import SessionLocal, engine
import database_model
from sqlalchemy.orm import Session

# Create the FastAPI application that serves the API routes below.
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"], 
)

# Create any database tables that do not already exist.
database_model.Base.metadata.create_all(bind=engine)

# Example products used by the API's current in-memory operations. The
# endpoints below do not read or write product changes to the database.
products = [
    Product(
        id=1,
        name="Notebook",
        description="A ruled paper notebook",
        price=4.99,
        quantity=25,
    ),
    Product(
        id=2,
        name="Pen",
        description="A blue ballpoint pen",
        price=1.5,
        quantity=100,
    ),
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# A simple health/welcome endpoint at the root URL.


# Add the sample products to the database the first time the app starts.
def init_db():
    db = SessionLocal()
    # Avoid inserting the examples again if products are already stored.
    count = db.query(database_model.Product).count()

    if count == 0:
        for product in products:
            db.add(database_model.Product(**product.model_dump()))
        db.commit()


# Seed the database before the application starts handling requests.
init_db()


# Return the current in-memory product list as JSON.
@app.get("/products", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    db_products = db.query(database_model.Product).all()

    return db.query(database_model.Product).all()




@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == product_id).first()
    if  db_product:
        return db_product
    return  "product not found"  # Return a 404 error if the product ID does not match any existing product.

# Add a product to the in-memory list and return it with HTTP status 201.
@app.post("/products", response_model=Product, status_code=201)
def create_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_model.Product(**product.model_dump()))
    db.commit() #it is important to commit the changes to the database after adding a new product.
    return product  # Return the newly created product with HTTP status 201.



# Replace the matching product's details using the supplied product ID.
@app.put("/products/{product_id}")
def update_product(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
):
    db_product = (
        db.query(database_model.Product)
        .filter(database_model.Product.id == product_id)
        .first()
    )
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()
    db.refresh(db_product)
    return db_product

# Remove a product by ID, or return HTTP 404 if it does not exist.
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)): #this endpoint deletes a product from the database based on the provided product ID.
    db_product = db.query(database_model.Product).filter(database_model.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()  # Commit the changes to the database after deleting the product.
        return "Product deleted successfully"
    else:
        return "product not found"  # Return a 404 error if the product ID does not match any existing product.