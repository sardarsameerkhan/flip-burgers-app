from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MENU = [
    {"id": 1, "name": "The OG Flip Burger", "price": 650, "category": "Beef"},
    {"id": 2, "name": "Double Smashed Flip", "price": 890, "category": "Beef"},
    {"id": 3, "name": "Fiery Zinger Burger", "price": 550, "category": "Chicken"},
    {"id": 4, "name": "Flip Loaded Fries", "price": 450, "category": "Sides"},
    {"id": 5, "name": "Soft Drink", "price": 120, "category": "Drinks"}
]

# --- LIVE ORDERS DATABASE SIMULATION ---
orders_db = []
order_id_counter = 1001 

# Rules for incoming data data
class OrderItem(BaseModel):
    menu_id: int
    quantity: int

class PlaceOrderInput(BaseModel):
    customer_name: str
    phone_number: str
    address_or_table: str  
    items: List[OrderItem]

class UpdateStatusInput(BaseModel):
    new_status: str  


# --- OPERATIONS ROUTES ---

@app.get("/menu")
def get_menu():
    return MENU

# Customer: Places order
@app.post("/orders")
def place_order(data: PlaceOrderInput):
    global order_id_counter
    total_bill = 0
    ordered_items_summary = []
    
    for item in data.items:
        menu_item = next((m for m in MENU if m["id"] == item.menu_id), None)
        if not menu_item:
            raise HTTPException(status_code=400, detail="Item not found")
        
        item_total = menu_item["price"] * item.quantity
        total_bill += item_total
        ordered_items_summary.append({
            "name": menu_item["name"],
            "quantity": item.quantity,
            "price": menu_item["price"]
        })
        
    new_order = {
        "order_id": order_id_counter,
        "customer_name": data.customer_name,
        "phone_number": data.phone_number,
        "address_or_table": data.address_or_table,
        "items": ordered_items_summary,
        "total_bill": total_bill,
        "status": "Pending"
    }
    
    orders_db.append(new_order)
    order_id_counter += 1
    return {"message": "Order received!", "order_id": new_order["order_id"]}

# Admin Dashboard: Get all current orders
@app.get("/admin/orders")
def get_all_orders():
    return orders_db

# Customer: Track their specific food status
@app.get("/track/{order_id}")
def track_order(order_id: int):
    order = next((o for o in orders_db if o["order_id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order tracking ID invalid")
    return order

# Admin Dashboard: Update order stage
@app.put("/admin/orders/{order_id}")
def update_order_status(order_id: int, data: UpdateStatusInput):
    order = next((o for o in orders_db if o["order_id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order["status"] = data.new_status
    return {"status": "Updated successfully", "order": order}