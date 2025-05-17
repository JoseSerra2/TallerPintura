from sqlalchemy.orm import Session
from app.model.inventario import Inventario
from app.model.movimiento import Movimiento 
from app.schema.inventario import InventarioCreate, InventarioUpdate
from datetime import datetime, timedelta
from fastapi import HTTPException
import httpx

def enviar_alerta_administracion(nombre_producto: str):
    try:
        url = "http://localhost:3000/api/administracion/POST/alertas/pintura"
        payload = {"nombre_producto": nombre_producto}
        response = httpx.post(url, json=payload, timeout=5)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] No se pudo enviar alerta: {e}")

def revisar_pinturas_por_vencer(db: Session, dias_antes: int = 30):
    fecha_alerta = datetime.now().date() + timedelta(days=dias_antes)
    inventarios_por_vencer = db.query(Inventario).filter(
        Inventario.FechaVencimiento != None,
        Inventario.FechaVencimiento <= fecha_alerta,
        Inventario.CantidadDisponible > 0
    ).all()

    for inv in inventarios_por_vencer:
        enviar_alerta_administracion(inv.NombreProducto)

def get_inventarios(db: Session):
    inventarios = db.query(Inventario).all()
    hoy = datetime.now().date()
    alerta_dias = 30  # días para avisar que está por vencer

    for inv in inventarios:
        # Alerta por cantidad baja
        if inv.CantidadDisponible <= 10:
            enviar_alerta_administracion(inv.NombreProducto)

        # Alerta por fecha de vencimiento
        if inv.FechaVencimiento:
            dias_para_vencer = (inv.FechaVencimiento - hoy).days
            if dias_para_vencer < 0:
                enviar_alerta_administracion(f"{inv.NombreProducto} está vencido ")
            elif dias_para_vencer <= alerta_dias:
                enviar_alerta_administracion(f"{inv.NombreProducto} vence pronto en {dias_para_vencer} días")

    return inventarios

def create_inventario(db: Session, inventario_data: InventarioCreate):
    data = inventario_data.dict()
    data.pop("accion", None)
    nuevo_inventario = Inventario(**data)
    db.add(nuevo_inventario)
    db.commit()
    db.refresh(nuevo_inventario)

    # Registrar movimiento de entrada
    movimiento = Movimiento(
        idInventario=nuevo_inventario.idInventario,
        TipoMovimiento="entrada",
        Cantidad=nuevo_inventario.CantidadDisponible,
        FechaMovimiento=datetime.now(),
        deleted=False
    )
    db.add(movimiento)
    db.commit()

    return nuevo_inventario

def update_inventario(db: Session, idInventario: int, inventario_data: InventarioUpdate):
    inventario = db.query(Inventario).filter(Inventario.idInventario == idInventario).first()
    if not inventario:
        return None

    for key, value in inventario_data.dict(exclude_unset=True).items():
        setattr(inventario, key, value)

    db.commit()
    db.refresh(inventario)
    return inventario

def procesar_solicitud_inventario(db: Session, idInventario: int, cantidad: int, origen: str):
    inventario = db.query(Inventario).filter(Inventario.idInventario == idInventario).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if origen == "admin":
        cantidad_total = inventario.CantidadDisponible + cantidad
        if cantidad_total > 50:
            sobrante = cantidad_total - 50
            inventario.CantidadDisponible = 50
            db.commit()
            db.refresh(inventario)

            # Registrar movimiento solo hasta el máximo permitido (50)
            movimiento = Movimiento(
                idInventario=inventario.idInventario,
                TipoMovimiento="entrada",
                Cantidad=(cantidad - sobrante),
                FechaMovimiento=datetime.now(),
                deleted=False
            )
            db.add(movimiento)
            db.commit()

            # Enviar alerta de sobrante
            enviar_alerta_administracion(
                f"Sobrante de {sobrante} unidades en {inventario.NombreProducto}"
            )
        else:
            inventario.CantidadDisponible += cantidad
            db.commit()
            db.refresh(inventario)

            movimiento = Movimiento(
                idInventario=inventario.idInventario,
                TipoMovimiento="entrada",
                Cantidad=cantidad,
                FechaMovimiento=datetime.now(),
                deleted=False
            )
            db.add(movimiento)
            db.commit()

        # Verificar si el inventario es bajo y enviar alerta
        if inventario.CantidadDisponible <= 10:
            enviar_alerta_administracion(inventario.NombreProducto)

        return {
            "mensaje": "Inventario actualizado por administración",
            "inventario": inventario
        }

    elif origen == "pintura":
        return {
            "mensaje": "Solicitud registrada, en espera de aprobación",
            "idInventario": idInventario,
            "cantidadSolicitada": cantidad
        }

    else:
        raise HTTPException(status_code=400, detail="Origen inválido")

def aplicar_descuento_desgaste(db: Session, porcentaje: float = 10.0):
    fecha_corte = datetime.now().date() - timedelta(days=6*30)
    inventarios_antiguos = db.query(Inventario).filter(
        Inventario.FechaAdquisicion <= fecha_corte,
        Inventario.CantidadDisponible > 0
    ).all()

    for inventario in inventarios_antiguos:
        descuento = int(inventario.CantidadDisponible * (porcentaje / 100))
        if descuento > 0:
            inventario.CantidadDisponible -= descuento
            if inventario.CantidadDisponible < 0:
                inventario.CantidadDisponible = 0

    db.commit()
