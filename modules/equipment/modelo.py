from typing import Optional

from pydantic import BaseModel
from fastapi import UploadFile
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Equipment(Base):
    __tablename__ = "equipments"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    image = Column(String(255))

    department = relationship("Department", back_populates="equipments")


class EquipmentCreate(BaseModel):
    description: str
    department_id: int
    image: Optional[UploadFile] = None

