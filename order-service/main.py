from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
  
@app.get('/api/v1/users')
async def user():
  users = [
    {
      'name': 'kamal',
      'age': 21
    },
    {
      'name': 'mostafa',
      'age': 27
    }
  ]
  return { "users": users }

@app.get('/api/v1/users/{user_id}')
async def get_user_by_id(user_id: int):
  return {'name': 'kamal is here', 'id': user_id}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


    
# @app.get('/api/v1/items/')
# async def items(item_id: int = None):
#     return {'a': ''}
  

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float


@app.post("/items/")
async def create_item(item: Item):
    #return item
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
  
from typing import Annotated
from fastapi import Header, Response, status
from fastapi.responses import JSONResponse
@app.get("/api/v1/itemsmk")
async def read_items(user_agent: Annotated[str , Header()] = None) -> Response:
    #return {"User-Agent": user_agent}
    return JSONResponse(content={"message": user_agent}, status_code= status.HTTP_200_OK)

from fastapi import Form
@app.post("/api/v1/login")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
  ):
    return {"username": username, 'password': password}