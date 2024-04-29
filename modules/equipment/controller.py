from fastapi import APIRouter, UploadFile, File, Depends, Form, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from depends import get_db_session, authenticate_ms_token
from modules.department.modelo import Department
from modules.equipment.dao import create_equipment_in_db

equipment_router = APIRouter(prefix="/tomba")


@equipment_router.post("/resgister/api/v1/equipment/")
async def create_equipment(token: str = Form(...), description: str = Form(...), department_id: int = Form(...), image: UploadFile = File(None), db_session: Session = Depends(get_db_session)):
    await authenticate_ms_token(token)
    if image is None or image.filename == "" or image.size == 0:
        return JSONResponse({"error": "No image provided or corrupted file"}, status_code=status.HTTP_400_BAD_REQUEST)
    if not any(ext in image.filename.lower() for ext in ('.jpg', '.jpeg', '.png')):
        return JSONResponse({"error": "Unsupported file type. Please upload only jpg, jpeg, or png files."},
                            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    department = db_session.query(Department).filter(Department.id == department_id).first()
    if not department:
        return JSONResponse({"error": f"Department with ID {department_id} not found"}, status_code=status.HTTP_404_NOT_FOUND)
    create_equipment_in_db(description, department_id, image, db_session)
    return JSONResponse(content={"message": "Equipment created successfully."}, status_code=status.HTTP_201_CREATED)

