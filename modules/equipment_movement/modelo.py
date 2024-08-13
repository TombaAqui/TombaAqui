from datetime import datetime
import pytz

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from base import Base


def get_brasilia_time():
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    return datetime.now(brasilia_tz)


class EquipmentMovement(Base):
    __tablename__ = "equipment_movements"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipments.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    created_at = Column(DateTime, default=get_brasilia_time)

    equipment = relationship("Equipment", back_populates="movements")
    department = relationship("Department")

    def get_formatted_created_at(self):
        return self.created_at.strftime('%d/%m/%Y %H:%M')
