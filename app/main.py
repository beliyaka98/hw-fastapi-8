from fastapi import Cookie, FastAPI, Form, Request, Response, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine, Base

from .purchases_repository import Purchase, PurchasesRepository


from pydantic import BaseModel, EmailStr

from typing import List
from jose import jwt
import json


app = FastAPI()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

purchases_repository = PurchasesRepository()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_jwt(user_id: int) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, "TorTokaeva", "HS256")
    return token

def decode_jwt(token: str) -> int:
    data = jwt.decode(token, "TorTokaeva", "HS256")
    return data["user_id"]

@app.post("/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def post_login(
    username: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, username)
    if not db_user or password != db_user.password:
        return HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_jwt(db_user.id)
    return {"access_token": token, "type": "bearer"}

@app.get("/profile", response_model=schemas.User)
def get_profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = decode_jwt(token)
    user = crud.get_user_by_id(db, user_id)
    return user


@app.get("/flowers", response_model=List[schemas.Flower])
def get_flowers(db: Session = Depends(get_db)):
    db_flowers = crud.get_flowers(db=db)
    return db_flowers


@app.post("/flowers", response_model=schemas.Flower)
def post_flowers(flower: schemas.Flower, db: Session = Depends(get_db)):
    db_flower = crud.add_flower(db=db, flower=flower)
    return db_flower

@app.post("/cart/items")
def post_cart_items(
    response: Response,
    flower_id: int,
    cart_items: str = Cookie(default="[]"),
):
    cart_items = json.loads(cart_items)
    cart_items.append(flower_id)
    cart_items = json.dumps(cart_items)
    response.set_cookie(key="cart_items", value=cart_items)
    return {cart_items}

@app.get("/cart/items", response_model=schemas.Flowers)
def get_cart_items(
    request: Request,
    cart_items: str = Cookie(default="[]"),
    db: Session = Depends(get_db),
):
    cart_items = json.loads(cart_items)
    flowers = [crud.get_flower_by_id(db=db, id=id) for id in cart_items]
    total_cost = sum(flower.cost for flower in flowers)
    print(flowers)

    return { "flowers": flowers, "total_cost": total_cost }