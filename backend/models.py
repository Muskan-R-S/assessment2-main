from sqlalchemy import create_engine, Column, Integer, String, Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from enum import Enum

# Database configuration
DATABASE_URL = "sqlite:///./orders.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Enum for allowed items
class AllowedItems(str, Enum):
    burger = "BURGER"
    fries = "FRIES"
    drink = "DRINK"


class OrderStatus(str, Enum):
    active = "ACTIVE"
    cancelled = "CANCELLED"


# OrderItem model
class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False, index=True)
    name = Column(SQLAlchemyEnum(AllowedItems), nullable=False)
    quantity = Column(Integer, nullable=False)


# Order model
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(SQLAlchemyEnum(OrderStatus), nullable=False)


# Create all tables
Base.metadata.create_all(bind=engine)
