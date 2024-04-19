from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from base import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    sigla = Column(String(255), nullable=False, unique=True)

    departments = relationship("Department", back_populates="company")
