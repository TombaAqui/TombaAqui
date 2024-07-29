from typing import Optional
from pydantic import BaseModel
from fastapi import UploadFile


class EquipmentResponse(BaseModel):
    id: int
    description: str
    department_id: int
    image: Optional[str] = None

    class Config:
        from_attributes = True # Permite que modelo use instâncias ORM e para usar o método from_orm com objetos que têm atributos (não apenas dicionários).


class EquipmentCreate(BaseModel):
    description: str
    department_id: int
    image: Optional[UploadFile] = None
