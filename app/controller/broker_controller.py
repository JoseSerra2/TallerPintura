from fastapi import APIRouter, Request
import httpx

router = APIRouter()

@router.post("/broker")
async def broker_handler(request: Request):
    body = await request.json()
    print("📩 Solicitud recibida:", body)

    uri = body.get("metadata", {}).get("uri")
    payload = body.get("request")

    if not uri:
        return {"error": "metadata.uri faltante"}
    if payload is None:
        return {"error": "request faltante"}

    try:
        _, method, endpoint = uri.strip("/").split("/", 2)
        method = method.upper()  # Aceptamos post, POST, Put, etc.
    except ValueError:
        return {"error": "URI inválida. Formato esperado: /pintura/METODO/endpoint"}

    url = f"http://localhost:8000/pintura/{method}/{endpoint}"
    print(f"➡️ Reenviando a {url} con método {method} y payload: {payload}")

    try:
        async with httpx.AsyncClient() as client:
            if method == "POST":
                response = await client.post(url, json=payload)
            elif method == "PUT":
                response = await client.put(url, json=payload)
            elif method == "GET":
                response = await client.get(url, params=payload)
            else:
                return {"error": f"Método {method} no soportado"}

        print("✅ Respuesta del microservicio:", response.status_code, response.text)
        return {
            "status_code": response.status_code,
            "data": response.json()
        }

    except httpx.RequestError as e:
        print("❌ Error al contactar al microservicio:", e)
        return {"error": "No se pudo contactar al servicio interno", "detalle": str(e)}
