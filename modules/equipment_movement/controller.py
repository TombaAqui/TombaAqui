from typing import List

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from depends import get_db_session, authenticate_ms_token
from modules.equipment.dao import get_equipment_by_id_or_404
from modules.equipment_movement.dao import get_equipment_movements

equipment_movements_router = APIRouter(prefix="/tomba")


@equipment_movements_router.get("/api/v1/equipment/{id_equipment}/movements/", response_model=List[dict])
async def get_equipment_movements_endpoint(id_equipment: int, token: str | None = Header(default=None), db: Session = Depends(get_db_session)):
    await authenticate_ms_token(token)
    # Verifica se o equipamento existe
    get_equipment_by_id_or_404(db=db, equipment_id=id_equipment)
    # Busca as movimentações do equipamento
    movements = get_equipment_movements(db=db, equipment_id=id_equipment)
    response = [{
            "departmento": {
                "id": movement.department.id,
                "name": movement.department.name
            },
            "created_at": movement.get_formatted_created_at()
        } for movement in movements]
    return response
