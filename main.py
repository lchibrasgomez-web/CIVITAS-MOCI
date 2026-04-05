from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

reportes_db = []

class Reporte(BaseModel):
    descripcion: str
    lat: float
    lng: float
    foto: Optional[str] = None
    tipo: Optional[str] = "general"

@app.get("/")
def root():
    return {"mensaje": "API funcionando"}

@app.get("/reportes")
def obtener_reportes():
    return reportes_db

@app.post("/reportes")
def crear_reporte(reporte: Reporte):
    reportes_db.append(reporte.dict())
    return {"ok": True}