from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import shutil
import os
import uuid

app = FastAPI()

# CORS (para que funcione en cualquier red)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carpeta imágenes
if not os.path.exists("imagenes"):
    os.makedirs("imagenes")

app.mount("/imagenes", StaticFiles(directory="imagenes"), name="imagenes")

reportes_db = []

class Reporte(BaseModel):
    descripcion: str
    lat: float
    lng: float
    tipo: Optional[str] = "Auto"
    foto: Optional[str] = None

# 🔥 IA SIMULADA (AUTO CLASIFICACIÓN)
def detectar_tipo(descripcion):
    desc = descripcion.lower()

    if "bache" in desc or "hoyo" in desc:
        return "Baches"
    elif "basura" in desc or "sucio" in desc:
        return "Basura"
    elif "luz" in desc or "luminaria" in desc:
        return "Luminaria"
    elif "limpieza" in desc:
        return "Limpieza"
    else:
        return "General"

@app.get("/")
def home():
    return {"mensaje": "CIVITAS IA ACTIVADA"}

@app.get("/reportes")
def obtener_reportes():
    return reportes_db

@app.post("/subir-imagen")
async def subir_imagen(file: UploadFile = File(...)):
    nombre = f"{uuid.uuid4()}.jpg"
    ruta = f"imagenes/{nombre}"

    with open(ruta, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"url": f"https://civitas-moci-production.up.railway.app/imagenes/{nombre}"}

@app.post("/reportes")
def crear_reporte(reporte: Reporte):

    # 🔥 IA decide tipo automáticamente
    tipo_detectado = detectar_tipo(reporte.descripcion)

    nuevo = reporte.dict()
    nuevo["tipo"] = tipo_detectado

    reportes_db.append(nuevo)

    return {
        "ok": True,
        "tipo_detectado": tipo_detectado
    }