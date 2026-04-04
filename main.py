from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

reportes_db = []

class Reporte(BaseModel):
    descripcion: str
    lat: float
    lng: float
    usuario: str
    imagen: str | None = None

def clasificar(descripcion: str):
    d = descripcion.lower()

    if "bache" in d:
        return "bache"
    elif "basura" in d:
        return "basura"
    elif "robo" in d:
        return "seguridad"
    else:
        return "otro"

@app.get("/")
def home():
    return {"mensaje": "CIVITAS API funcionando"}

@app.get("/reportes")
def obtener_reportes():
    return reportes_db

@app.post("/reportes")
def crear_reporte(reporte: Reporte):
    nuevo = {
        "descripcion": reporte.descripcion,
        "lat": reporte.lat,
        "lng": reporte.lng,
        "usuario": reporte.usuario,
        "categoria": clasificar(reporte.descripcion),
        "imagen": reporte.imagen
    }

    reportes_db.append(nuevo)
    return {"ok": True}