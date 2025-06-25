def assign_category(restock_quantity: int) -> str:
    return "high_volume" if restock_quantity > 50 else "low_volume"

def validate_product(data):

    if data["priority"] == "high" and data["min_threshold"] < 10:
        data["min_threshold"] = 10
    data["category"] = assign_category(data["restock_quantity"])
    return data

def determine_status(product):
    if product["stock_quantity"] == 0:
        return "out_of_stock"
    elif product["stock_quantity"] < product["min_threshold"]:
        return "below_threshold"
    else:
        return "ok"

def auto_restock(product):
    if product["priority"] == "high" and product["stock_quantity"] < product["min_threshold"]:
        product["stock_quantity"] += product["restock_quantity"]
    elif product["priority"] != "low" and product["stock_quantity"] == 0:
        product["stock_quantity"] += product["restock_quantity"]
