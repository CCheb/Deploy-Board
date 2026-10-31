from fastapi import FastAPI
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(default="Johnny", title="Name of the item", max_length=100)
    description: str = Field(default="", title="Description of the item")
    price: float = Field(default=10.0, gt=0, title="Price of the item")
    tax: float = Field(default=0.07, title="Tax of the item")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello backend!"}


@app.post("/items/")
async def create_item(item: Item):
    return {"item": item}