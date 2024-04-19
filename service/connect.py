from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


class Connect:

    def __init__(self):
        self.POSTGRES_DB = "bd_micro_service"
        self.POSTGRES_USER = "postgres"
        self.POSTGRES_PASSWORD = "postgres"

        self.DB_URL = f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost/{self.POSTGRES_DB}"

        self.engine = create_engine(self.DB_URL, pool_pre_ping=True)
        self.Session = sessionmaker(bind=self.engine)

        self.metadata = MetaData()

    def get_session(self):
        return self.Session()
