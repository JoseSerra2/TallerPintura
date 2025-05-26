from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import httpx

from app.database import SessionLocal
from app.service.Venta_service import crear_venta, obtener_ventas, actualizar_venta
from app.service.DetalleVenta_service import crear_detalle
from app.schema.Venta import VentaResponse, VentaUpdate, VentaCreate, VentaSimpleRequest
from app.schema.Detalle_Venta import DetalleVentaCreate
from app.model.servicio import Servicio
from app.model.tipovehiculo import TipoVehiculo
from app.model.inventario import Inventario
from app.model.vehiculoinventario import VehiculoInventario
from app.model.movimiento import Movimiento

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
        # Validar Detalle
        for item in venta.Detalle:
            if not item.Producto:
                raise HTTPException(status_code=400, detail="Campo 'Producto' vacío en detalle de venta")
            if item.Cantidad <= 0 or item.Precio <= 0:
                raise HTTPException(status_code=400, detail=f"Cantidad o Precio inválido para el producto: {item.Producto}")

        # Preparar datos para el servicio de pagos
        detalle_pago = [
            {
                "Producto": item.Producto,
                "Cantidad": item.Cantidad,
                "Precio": item.Precio,
                "Descuento": item.Descuento
            }
            for item in venta.Detalle
        ]

        metodos_pago = [
            {
                "NoTarjeta": mp.NoTarjeta or "",
                "IdMetodo": mp.IdMetodo,
                "Monto": mp.Monto,
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

        print("📤 Enviando datos al servicio de pagos:")
        print(data_para_pago)

        # Llamada al servicio de pagos
        try:
            response = httpx.post("http://64.23.169.22:3001/pagos/transacciones/crear", json=data_para_pago)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"❌ Error HTTP al contactar servicio de pagos: {e.response.status_code}")
            print(f"📩 Respuesta de error: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Servicio de pagos rechazó la solicitud: {e.response.text}")
        except httpx.RequestError as e:
            print(f"❌ Error de conexión al servicio de pagos: {e}")
            raise HTTPException(status_code=500, detail=f"No se pudo conectar al servicio de pagos: {str(e)}")

        try:
            data = response.json()
        except Exception as e:
            print("❌ No se pudo interpretar la respuesta JSON del servicio de pagos")
            raise HTTPException(status_code=500, detail=f"Respuesta inválida del servicio de pagos: {response.text}")

        print("✅ Respuesta recibida de pagos:", data)

        if "factura" not in data or "cliente" not in data["factura"]:
            raise HTTPException(status_code=500, detail=f"Respuesta incompleta del servicio de pagos: {data}")

        venta_create = VentaCreate(
            idCliente=data["factura"]["cliente"]["idCliente"],
            noTransaccion=data["noTransaccion"],
            TotalVenta=data["factura"]["total"]
        )

        nueva_venta = crear_venta(db, venta_create)

        for item in data["factura"]["detalle"]:
            detalle_normalizado = {k.lower(): v for k, v in item.items()}
            if "producto" not in detalle_normalizado:
                raise HTTPException(status_code=500, detail=f"Detalle sin campo 'Producto': {item}")

            producto = detalle_normalizado["producto"]
            cantidad = detalle_normalizado.get("cantidad", 0)
            precio = detalle_normalizado.get("precio", 0)
            descuento = detalle_normalizado.get("descuento", 0)

            if not isinstance(cantidad, (int, float)) or not isinstance(precio, (int, float)) or not isinstance(descuento, (int, float)):
                raise HTTPException(status_code=400, detail=f"Tipos inválidos en detalle: {detalle_normalizado}")

            servicio = db.query(Servicio).filter(Servicio.NombreServicio == producto).first()
            if not servicio:
                raise HTTPException(status_code=404, detail=f"Servicio '{producto}' no encontrado")

            subtotal = cantidad * precio * (1 - descuento)

            detalle_create = DetalleVentaCreate(
                idVenta=nueva_venta.idVenta,
                idServicio=servicio.idServicio,
                Cantidad=cantidad,
                Subtotal=subtotal,
                Devolucion=servicio.ValidoDev,
                deleted=False
            )
            crear_detalle(db, detalle_create)

        # 🔁 DESCUENTO DE INVENTARIO Y REGISTRO DE MOVIMIENTO (FIFO)
        tipo_vehiculo = db.query(TipoVehiculo).filter(TipoVehiculo.NombreTipoVehiculo == venta.TipoVehiculo).first()
        if not tipo_vehiculo:
            raise HTTPException(status_code=404, detail=f"Tipo de vehículo '{venta.TipoVehiculo}' no encontrado")

        relaciones = db.query(VehiculoInventario).filter(VehiculoInventario.idTipoVehiculo == tipo_vehiculo.idTipoVehiculo).all()
        if not relaciones:
            raise HTTPException(status_code=404, detail=f"No se encontraron insumos asociados al tipo de vehículo '{venta.TipoVehiculo}'")

        for relacion in relaciones:
            cantidad_requerida = relacion.CantidadRequerida
            # Consultar lotes con stock > 0, activos y ordenados por FechaAdquisicion ascendente
            inventarios = db.query(Inventario).filter(
                Inventario.idInventario == relacion.idInventario,
                Inventario.CantidadDisponible > 0,
                Inventario.deleted == False,
                Inventario.EstadoInventario == True
            ).order_by(Inventario.FechaAdquisicion.asc()).all()

            for inventario in inventarios:
                if cantidad_requerida <= 0:
                    break

                disponible = inventario.CantidadDisponible

                if disponible >= cantidad_requerida:
                    inventario.CantidadDisponible -= cantidad_requerida

                    movimiento = Movimiento(
                        idInventario=inventario.idInventario,
                        TipoMovimiento="Salida",
                        Cantidad=cantidad_requerida,
                        FechaMovimiento=datetime.now(),
                        deleted=False
                    )
                    db.add(movimiento)
                    cantidad_requerida = 0
                else:
                    inventario.CantidadDisponible = 0
                    movimiento = Movimiento(
                        idInventario=inventario.idInventario,
                        TipoMovimiento="Salida",
                        Cantidad=disponible,
                        FechaMovimiento=datetime.now(),
                        deleted=False
                    )
                    db.add(movimiento)
                    cantidad_requerida -= disponible

            if cantidad_requerida > 0:
                raise HTTPException(status_code=400, detail=f"Inventario insuficiente para '{inventario.NombreProducto}'")

        db.commit()

        return nueva_venta

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print("❌ Error inesperado:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error inesperado reenviando a pagos: {str(e)}")

@router.put("/pintura/PUT/venta/{venta_id}", response_model=VentaResponse)
def actualizar_una_venta(venta_id: int, venta: VentaUpdate, db: Session = Depends(get_db)):
    venta_actualizada = actualizar_venta(db, venta_id, venta)
    if not venta_actualizada:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta_actualizada
