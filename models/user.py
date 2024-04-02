from database import db
from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80),unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(80), unique=True, nullable=True)