from fastapi import FastAPI

from modules.company.controller import company_router
from service.connect import Connect

app = FastAPI()
if __name__ == '__main__':
    print(company_router.routes)
app.include_router(company_router)

# conn.create_database()
# conn.create_user_table()
if __name__ == "__main__":
    import uvicorn
    conn = Connect()
    uvicorn.run("app:app", host="127.0.0.1", port=8001, log_level="debug", reload=True)

