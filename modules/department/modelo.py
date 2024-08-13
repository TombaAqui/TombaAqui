from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))

    company = relationship("Company", back_populates="departments")
    equipments = relationship("Equipment", back_populates="department")
    movements = relationship("EquipmentMovement", back_populates="department")