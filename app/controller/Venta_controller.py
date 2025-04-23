from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.service.Venta_service import crear_venta, obtener_ventas, actualizar_venta
from app.service.DetalleVenta_service import crear_detalle
from app.schema.Venta import VentaConPagoRequest, VentaResponse, VentaCreate, VentaUpdate
from app.schema.Detalle_Venta import DetalleVentaCreate
import httpx
from sqlalchemy import text

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/pintura/GET/venta", response_model=List[VentaResponse])
def listar_ventas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return obtener_ventas(db, skip, limit)

@router.post("/pintura/POST/venta", response_model=VentaResponse)
def crear_una_venta_con_pago(venta: VentaConPagoRequest, db: Session = Depends(get_db)):
    try:
        response = httpx.post("http://localhost:3001/pagos/validar", json=venta.dict())
        data = response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comunicándose con pagos: {str(e)}")

    if "factura" not in data:
        raise HTTPException(status_code=400, detail="Respuesta inválida del servicio de pagos")

    factura = data["factura"]
    cliente_info = factura.get("cliente", {})
    cliente_id = cliente_info.get("idCliente")

    # Obtener servicios y mapearlos por nombre normalizado
    servicios = db.execute(text('SELECT NombreServicio, idServicio FROM servicio')).fetchall()
    nombres_validos = {
        s[0].strip().lower(): s[1]
        for s in servicios
    }

    total = 0
    detalles_a_guardar = []

    for item in venta.Detalle:
        producto_normalizado = item.Producto.strip().lower()

        if producto_normalizado not in nombres_validos:
            raise HTTPException(
                status_code=400,
                detail=f"Producto '{item.Producto}' no coincide con ningún servicio registrado."
            )

        subtotal = (item.Precio - item.Descuento) * item.Cantidad
        total += subtotal

        detalles_a_guardar.append({
            "idServicio": nombres_validos[producto_normalizado],
            "Cantidad": item.Cantidad,
            "Subtotal": subtotal
        })

    nueva_venta = VentaCreate(idCliente=cliente_id, TotalVenta=total)
    venta_creada = crear_venta(db, nueva_venta)

    for d in detalles_a_guardar:
        detalle_data = DetalleVentaCreate(
            idVenta=venta_creada.idVenta,
            idServicio=d["idServicio"],
            Cantidad=d["Cantidad"],
            Subtotal=d["Subtotal"],
            Devolucion=False
        )
        crear_detalle(db, detalle_data)

    return venta_creada

@router.put("/pintura/PUT/venta/{venta_id}", response_model=VentaResponse)
def actualizar_una_venta(venta_id: int, venta: VentaUpdate, db: Session = Depends(get_db)):
    venta_actualizada = actualizar_venta(db, venta_id, venta)
    if not venta_actualizada:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta_actualizada
