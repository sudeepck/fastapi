from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Products
from database import session, engine
import database_models
from dummyProducts import dummy_products
from sqlalchemy.orm import Session 
#Password
#5432

app = FastAPI()
## Create the database tables
database_models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def greet():
    return "Hello from main.py!"

def init__db():
    db = session()
    count = db.query(database_models.Product).count
    if count == 0 :
        for product in dummy_products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    
init__db()
            
## the session in the parameter is from "sqlalchemy.orm" and it Depnds on the "get_db"
@app.get("/products")
def get_products(db : Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")  
async def  get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product =  db.query(database_models.Product).filter(database_models.Product.id == id).first()
    return f"No Product found with product id :{id}" if db_product is None else db_product

@app.post("/products")
def add_product(product: Products, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id: int, product: Products, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name or db_product.name
        db_product.description = product.description or db_product.description
        db_product.price = product.price or db_product.price
        db_product.quantity = product.quantity or db_product.quantity
        db.commit()
        return f"product with id : {id} updated successfully"
    else:   
        return {"error": "no such Product exists to update"}

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_produc = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_produc:
        db.delete(db_produc)
        db.commit()
        return f"Product with id : {id} deleted successfully"
    else:
        return {"error": "Product not found"}