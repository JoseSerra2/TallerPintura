import logging
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(
    filename="queries.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

logger = logging.getLogger("sqlalchemy_full_query")

DATABASE_URL = "mariadb+mariadbconnector://root:1234@127.0.0.1:3307/taller_pintura"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    try:
        if parameters:
            # Esta línea intenta reemplazar placeholders por valores
            # Es simple y funciona para parámetros posicionales o diccionarios simples
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
