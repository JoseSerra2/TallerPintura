import logging
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv("queries.env")

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3307")
DB_NAME = os.getenv("DB_NAME", "taller_pintura")

DATABASE_URL = f"mariadb+mariadbconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configuración de logs
logging.basicConfig(
    filename="queries.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
logger = logging.getLogger("sqlalchemy_full_query")

# Motor y sesión
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Logging SQL
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    try:
        if parameters:
            if isinstance(parameters, (list, tuple)):
                query = statement % tuple(repr(p) for p in parameters)
            elif isinstance(parameters, dict):
                query = statement % {k: repr(v) for k, v in parameters.items()}
            else:
                query = statement
        else:
            query = statement
    except Exception:
        query = statement
    logger.info(query)

# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
