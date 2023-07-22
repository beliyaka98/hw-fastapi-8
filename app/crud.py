from sqlalchemy.orm import Session

from . import models, schemas 

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, full_name=user.full_name, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def add_flower(db: Session, flower: schemas.Flower):
    db_flower = models.Flower(name=flower.name, count=flower.count, cost=flower.cost)
    db.add(db_flower)
    db.commit()
    db.refresh(db_flower)
    return db_flower

def get_flowers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flower).offset(skip).limit(limit).all()

def get_flower_by_id(db: Session, id: int):
    return db.query(models.Flower).filter(models.Flower.id==id).first()