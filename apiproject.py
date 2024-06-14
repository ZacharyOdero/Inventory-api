from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI() #creating an object of FastAPI class

class Item(BaseModel): #Base Model for items stored in inventory
    name: str
    price: int
    brand: str = None

class UpdateItem(BaseModel):
    name: str = None
    price: int = None
    brand: str = None

inventory = {}

#defining end points
@app.get("/get-item/{item_id}")
def get_item(item_id : int = Path(description="The ID of the item you would like to view", gt= 0)):
    return inventory[item_id]


@app.get("/get-by-name")
def get_item(name: str = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    return {"Data": "Not Found"}   
 

@app.post("/create-item/{item_id}")
def create_item(item: Item, item_id: int):
    if item_id in inventory:
        return{"Error": "Item ID already exists"}
    
    inventory[item_id] = item
    return inventory[item_id]

    
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return{"Error": "Item ID does not exist"}
    
    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand
    
    return{"Status": "Updated successfully!"}
    

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description= "The ID of the item you would like to delete")):
    if item_id not in inventory:
        return{"Error": "The item ID does not exist"}
    
    del inventory[item_id]
    return{"Status": "Deleted successfully!"}

