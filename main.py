from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- FLIP BURGERS MENU DATABASE ---
MENU = [
    {"id": 1, "name": "The OG Flip Burger", "price": 650, "category": "Beef"},
    {"id": 2, "name": "Double Smashed Flip", "price": 890, "category": "Beef"},
    {"id": 3, "name": "Fiery Zinger Burger", "price": 550, "category": "Chicken"},
    {"id": 4, "name": "Flip Loaded Fries", "price": 450, "category": "Sides"},
    {"id": 5, "name": "Soft Drink", "price": 120, "category": "Drinks"}
]

@app.get("/")
def home():
    return {"message": "Flip Burgers Backend is running successfully!"}

# New route for customers to fetch the menu items
@app.get("/menu")
def get_menu():
    return MENU