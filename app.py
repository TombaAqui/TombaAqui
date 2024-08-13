from fastapi import FastAPI

from modules.company.controller import company_router
from modules.department.controller import department_router
from modules.equipment.controller import equipment_router
from modules.equipment_movement.controller import equipment_movements_router
from service.connect import Connect

app = FastAPI()
app.include_router(company_router)
app.include_router(department_router)
app.include_router(equipment_router)
app.include_router(equipment_movements_router)

if __name__ == "__main__":

    import uvicorn
    conn = Connect()
    conn.create_database()
    conn.create_tables()
    uvicorn.run("app:app", host="127.0.0.1", port=8001, log_level="debug", reload=True)
