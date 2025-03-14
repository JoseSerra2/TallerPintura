from sqlalchemy.orm import Session
from app.model.cliente import Cliente
from app.schema.cliente import ClienteCreate, ClienteUpdate


def get_clientes(db: Session):
    return db.query(Cliente).all()


def create_cliente(db: Session, cliente_data: ClienteCreate):
    nuevo_cliente = Cliente(**cliente_data.dict())  
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)  
    return nuevo_cliente


def update_cliente(db: Session, idCliente: int, cliente_data: ClienteUpdate):
    cliente = db.query(Cliente).filter(Cliente.idCliente == idCliente).first()
    if not cliente:
        return None  
    
    
    for key, value in cliente_data.dict(exclude_unset=True).items():
        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)
    return cliente
