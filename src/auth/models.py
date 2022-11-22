from sqlalchemy import Column, Integer, String, ForeignKey, SMALLINT
from sqlalchemy.orm import relationship
from config.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String(24), primary_key=True)
    email = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    state = Column(SMALLINT, nullable=False)
    photo = Column(String(500), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(15), nullable=False)
    description = Column(String(50), nullable=False)