from sqlalchemy.orm import Session

from modules.equipment_movement.modelo import EquipmentMovement


def get_equipment_movements(db: Session, equipment_id: int):
    """
    Obtém todas as movimentações de um equipamento específico.

    Args:
        db (Session): Sessão do banco de dados.
        equipment_id (int): ID do equipamento.

    Returns:
        List[EquipmentMovement]: Lista de objetos EquipmentMovement.
    """
    return db.query(EquipmentMovement).filter(EquipmentMovement.equipment_id == equipment_id).all()

