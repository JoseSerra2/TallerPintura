from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.service.Venta_service import crear_venta, obtener_ventas, actualizar_venta
from app.service.DetalleVenta_service import crear_detalle
from app.schema.Venta import VentaResponse, VentaUpdate
from app.schema.Detalle_Venta import DetalleVentaCreate
import httpx
from app.model.servicio import Servicio
from app.schema.Venta import VentaSimpleRequest
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
def crear_venta_reenviada(venta: VentaSimpleRequest, db: Session = Depends(get_db)):
    try:
        # 1. Reenviar solicitud a Mockoon (servicio de pagos)
        detalle_pago = [
            {
                "producto": item.Producto,
                "cantidad": item.Cantidad,
                "precio": item.Precio,
                "descuento": item.Descuento
            }
            for item in venta.Detalle
        ]

        metodos_pago = [
            {
                "NoTarjeta": mp.NoTarjeta or "",
                "IdMetodo": mp.IdMetodo,
                "Monto": str(mp.Monto),
                "IdBanco": mp.IdBanco or ""
            }
            for mp in venta.MetodosPago
        ]

        data_para_pago = {
            "Nit": venta.Nit,
            "IdCaja": venta.IdCaja,
            "IdServicioTransaccion": venta.IdServicioTransaccion,
            "Detalle": detalle_pago,
            "MetodosPago": metodos_pago
        }

        response = httpx.post("http://localhost:3001/pagos/validar", json=data_para_pago)
        data = response.json()

        if "factura" not in data:
            raise HTTPException(status_code=400, detail="Respuesta inválida del servicio de pagos")

        # 2. Crear nuevo objeto tipo VentaConPagoRequest usando la respuesta de Mockoon
        from app.schema.Venta import VentaCreate  # Necesitamos VentaCreate para crear la venta

        # Crear el objeto de venta que acepta la base de datos (VentaCreate)
        venta_create = VentaCreate(
            idCliente=data["factura"]["cliente"]["idCliente"],  # Asumimos que idCliente es parte de la factura
            TotalVenta=data["factura"]["totalDescontado"]  # Asumimos que totalDescontado es el total de la venta
        )

        # 3. Llamar internamente a la función existente para crear la venta con la factura
        nueva_venta = crear_venta(db, venta_create)
        
        for item in data["factura"]["detalle"]:
            # Buscar el servicio por nombre (Producto)
            servicio = db.query(Servicio).filter(Servicio.NombreServicio == item["Producto"]).first()
            if not servicio:
                raise HTTPException(status_code=404, detail=f"Servicio '{item['Producto']}' no encontrado")

            subtotal = (item["Cantidad"] * item["Precio"]) - item["Descuento"]

            detalle_create = DetalleVentaCreate(
                idVenta=nueva_venta.idVenta,
                idServicio=servicio.idServicio,
                Cantidad=item["Cantidad"],
                Subtotal=subtotal,
                Devolucion=servicio.ValidoDev,  # o servicio.esDevolucion según tu modelo
                deleted=False
            )
            crear_detalle(db, detalle_create)

        # Si necesitas realizar algún procesamiento adicional con la factura o metodos de pago, hazlo aquí
        return nueva_venta

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reenviando a pagos: {str(e)}")

@router.put("/pintura/PUT/venta/{venta_id}", response_model=VentaResponse)
def actualizar_una_venta(venta_id: int, venta: VentaUpdate, db: Session = Depends(get_db)):
    venta_actualizada = actualizar_venta(db, venta_id, venta)
    if not venta_actualizada:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta_actualizada
