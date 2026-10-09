from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    skin_type = Column(
        String,
        nullable=False
    )

    concerns = Column(
        JSON,
        nullable=False
    )

    age_range = Column(
        String,
        nullable=True
    )

    product_preferences = Column(
        String,
        nullable=True
    )

    budget = Column(
        Integer,
        nullable=True
    )

    ingredients_to_avoid = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )