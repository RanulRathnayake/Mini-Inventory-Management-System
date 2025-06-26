from fastapi import FastAPI, HTTPException
from models import Product, PurchaseRequest
from storage import PRODUCTS_DB
from utils import validate_product, determine_status, auto_restock
from response import success_response, error_response

app = FastAPI()

@app.post("/products")
def add_product(product: Product):
    data = validate_product(product.dict())
    if data["product_id"] in PRODUCTS_DB:
        return error_response("Product ID already exists.", "ProductAlreadyExists", 400)
    PRODUCTS_DB[data["product_id"]] = data
    return success_response("Product added successfully", data)

@app.get("/inventory/{product_id}")
def inventory_status(product_id: str):
    product = PRODUCTS_DB.get(product_id)
    if not product:
        return error_response("Product not found.", "ProductNotFound", 404)
    auto_restock(product)
    response_data = {
        "product_id": product["product_id"],
        "stock_quantity": product["stock_quantity"],
        "status": determine_status(product),
        "priority": product["priority"]
    }
    return success_response("Inventory status retrieved", response_data)

@app.patch("/purchase/{product_id}")
def purchase_product(product_id: str, request: PurchaseRequest):
    product = PRODUCTS_DB.get(product_id)
    quantity = request.quantity

    if not product:
        return error_response("Product not found.", "ProductNotFound", 404)

    if quantity <= 0:
        return error_response("Quantity must be positive.", "InvalidQuantity", 400)

    if product["stock_quantity"] < quantity:
        return error_response("Not enough stock available.", "InsufficientStock", 400)

    product["stock_quantity"] -= quantity
    auto_restock(product)

    result = {
        "product_id": product["product_id"],
        "new_stock": product["stock_quantity"],
        "status": determine_status(product)
    }

    return success_response(f"Purchased {quantity} units of {product['name']}.", result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


