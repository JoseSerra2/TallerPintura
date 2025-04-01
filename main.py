from fastapi import FastAPI
from app.controller.servicio_controller import router as servicio_router 
from app.controller.tipovehiculo_controller import router as tipovehiculo_router 
from app.controller.tipopintura_controller import router as tipopintura_router
from app.controller.tiposervicio_controller import router as tiposervicio_router
from app.controller.inventario_controller import router as inventario_router
from app.controller.vehiculoinventario_controller import router as vehiculoinventario_router

app = FastAPI(
    title="API de Pintura",
    description="Microservicio para gestionar taller de pintura",
    version="1.0"
)


app.include_router(servicio_router, tags=["Servicios"])  
app.include_router(tipovehiculo_router, tags=["Tipos de Vehículos"])
app.include_router(tipopintura_router, tags=["Tipos de Pintura"])  
app.include_router(tiposervicio_router, tags=["Tipos de Servicio"]) 
app.include_router(inventario_router, tags=["Inventarios"])
app.include_router(vehiculoinventario_router, tags=["Vehículo Inventarios"])


@app.get("/")
def home():
    return {"message": "Bienvenido a la API del Taller de Pintura"}
