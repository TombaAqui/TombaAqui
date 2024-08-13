from typing import List

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from depends import get_db_session, authenticate_ms_token
from modules.equipment.dao import get_equipment_by_id
from modules.equipment_movement.modelo import EquipmentMovement

equipment_movements_router = APIRouter(prefix="/tomba")


@equipment_movements_router.get("/api/v1/equipment/{id_equipment}/movements/", response_model=List[dict])
async def get_equipment_movements(id_equipment: int, token: str | None = Header(default=None), db: Session = Depends(get_db_session)):
    await authenticate_ms_token(token)
    # Verifica se o equipamento existe
    equipment = get_equipment_by_id(db=db, equipment_id=id_equipment)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    # Busca as movimentações do equipamento
    movements = db.query(EquipmentMovement).filter(EquipmentMovement.equipment_id == id_equipment).all()
    response = [{
            "departmento": {
                "id": movement.department.id,
                "name": movement.department.name
            },
            "create_at": movement.get_formatted_created_at()
        } for movement in movements]
    return response
