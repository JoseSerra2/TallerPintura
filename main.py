from fastapi import FastAPI
from app.controller.Venta_controller import router as Venta_router
from app.controller.servicio_controller import router as servicio_router 
from app.controller.tipovehiculo_controller import router as tipovehiculo_router 
from app.controller.tipopintura_controller import router as tipopintura_router
from app.controller.tiposervicio_controller import router as tiposervicio_router
from app.controller.inventario_controller import router as inventario_router
from app.controller.vehiculoinventario_controller import router as vehiculoinventario_router
from app.controller.cliente_controller import router as cliente_router #temporal
from app.controller.Devolucion_controller import router as Devolucion_router
from app.controller.Detalleventa_controller import router as DetalleVenta_router
from app.controller.movimiento_controller import router as Movimiento_router
from app.controller.psvcontroller import router as precio_servicio
from app.controller.broker_controller import router as broker_router #broker


app = FastAPI(
    title="API de Pintura",
    description="Microservicio para gestionar taller de pintura",
    version="1.0"
)

app.include_router(cliente_router, tags=["Clientes"]) #temporal
app.include_router(servicio_router, tags=["Servicios"])  
app.include_router(Venta_router, tags=["Venta"])  
app.include_router(tipovehiculo_router, tags=["Tipos de Vehículos"])
app.include_router(tipopintura_router, tags=["Tipos de Pintura"])  
app.include_router(tiposervicio_router, tags=["Tipos de Servicio"]) 
app.include_router(inventario_router, tags=["Inventarios"])
app.include_router(vehiculoinventario_router, tags=["Vehículo Inventarios"])
app.include_router(Devolucion_router, tags= ["Devoluciones"])
app.include_router(DetalleVenta_router, tags = ["Detalle Venta"])
app.include_router(Movimiento_router, tags = ["Movimiento"])
app.include_router(precio_servicio, tags = ["Precio Servicio"])
app.include_router(broker_router, tags=["Broker"]) #broker



@app.get("/")
def home():
    return {"message": "Bienvenido a la API del Taller de Pintura"}
