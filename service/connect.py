from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from base import Base
from modules.company.modelo import Company
from modules.department.modelo import Department
from modules.equipment.modelo import Equipment
from modules.equipment_movement.modelo import EquipmentMovement


class Connect:

    def __init__(self):
        self.POSTGRES_DB = "bd_tomba_aqui"
        self.POSTGRES_USER = "postgres"
        self.POSTGRES_PASSWORD = "postgres"

        self.DB_URL = f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost/{self.POSTGRES_DB}"

        self.engine = create_engine(self.DB_URL, pool_pre_ping=True)
        self.Session = sessionmaker(bind=self.engine)

        self.metadata = MetaData()

    def create_database(self):
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            print("Database created successfully.")

    def create_tables(self):
        # Carrega as informações do banco de dados existente
        self.metadata.reflect(bind=self.engine)

        if "companies" not in self.metadata.tables:
            Base.metadata.create_all(bind=self.engine, tables=[Company.__table__])
            print("Table 'companies' created.")
        if "departments" not in self.metadata.tables:
            Base.metadata.create_all(bind=self.engine, tables=[Department.__table__])
            print("Table 'departments' created.")
        if "equipments" not in self.metadata.tables:
            Base.metadata.create_all(bind=self.engine, tables=[Equipment.__table__])
            print("Table 'equipments' created.")
        if "equipment_movements" not in self.metadata.tables:
            Base.metadata.create_all(bind=self.engine, tables=[EquipmentMovement.__table__])
            print("Table 'equipment_movements' created.")

    def get_session(self):
        return self.Session()
