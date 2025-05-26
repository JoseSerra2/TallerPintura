from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import httpx

router = APIRouter()

@router.post("/broker/api/rest")
async def broker_handler(request: Request):
    try:
        body = await request.json()
        metadata = body.get("metadata", {})
        uri = metadata.get("uri")
        payload = body.get("request", {})

        if not uri:
            return JSONResponse(
                status_code=400,
                content={
                    "metadata": {"uri": uri},
                    "response": {
                        "data": {},
                        "_broker_status": 400,
                        "_broker_message": "metadata.uri faltante"
                    }
                }
            )

        try:
            _, method, endpoint = uri.strip("/").split("/", 2)
        except ValueError:
            return JSONResponse(
                status_code=400,
                content={
                    "metadata": {"uri": uri},
                    "response": {
                        "data": {},
                        "_broker_status": 400,
                        "_broker_message": "URI inválida. Formato esperado: /pintura/METODO/endpoint"
                    }
                }
            )

        url = f"http://64.23.169.22:8000/pintura/{method}/{endpoint}"
        print(f"➡️ Reenviando a {url} con método {method} y payload: {payload}")

        async with httpx.AsyncClient() as client:
            if method == "POST":
                response = await client.post(url, json=payload)
            elif method == "PUT":
                response = await client.put(url, json=payload)
            elif method == "GET":
                response = await client.get(url, params=payload)
            else:
                return JSONResponse(
                    status_code=405,
                    content={
                        "metadata": {"uri": uri},
                        "response": {
                            "data": {},
                            "_broker_status": 405,
                            "_broker_message": f"Método {method} no soportado"
                        }
                    }
                )

        response_data = response.json()

        return JSONResponse(
            status_code=response.status_code,
            content={
                "metadata": {"uri": uri},
                "response": {
                    "data": response_data,
                    "_broker_status": response.status_code,
                    "_broker_message": "OK" if response.status_code < 400 else "Error"
                }
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "metadata": {"uri": None},
                "response": {
                    "data": {},
                    "_broker_status": 500,
                    "_broker_message": f"Error interno: {str(e)}"
                }
            }
        )
