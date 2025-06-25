from fastapi import FastAPI, HTTPException
from models import Product
from models import PurchaseRequest
from storage import PRODUCTS_DB
from utils import validate_product, determine_status, auto_restock

app = FastAPI()

@app.post("/products")
def add_product(product: Product):
    data = validate_product(product.dict())
    if data["product_id"] in PRODUCTS_DB:
        raise HTTPException(status_code=400, detail="Product ID already exists.")
    PRODUCTS_DB[data["product_id"]] = data
    return {"message": "Product added successfully", "product": data}

@app.get("/inventory/{product_id}")
def inventory_status(product_id: str):
    product = PRODUCTS_DB.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    auto_restock(product)
    return {
        "product_id": product["product_id"],
        "stock_quantity": product["stock_quantity"],
        "status": determine_status(product),
        "priority": product["priority"]
    }

@app.patch("/purchase/{product_id}")
def purchase_product(product_id: str, request: PurchaseRequest):
    quantity = request.quantity
    product = PRODUCTS_DB.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Purchase quantity must be positive.")

    if product["stock_quantity"] < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available.")

    product["stock_quantity"] = product["stock_quantity"] - quantity
    auto_restock(product)

    return {
        "message": f"Purchased {quantity} units of {product['name']}.",
        "new_stock": product["stock_quantity"],
        "status": determine_status(product)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


