from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import shutil
import os
import uuid
import json

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# carpeta imágenes
if not os.path.exists("imagenes"):
    os.makedirs("imagenes")

app.mount("/imagenes", StaticFiles(directory="imagenes"), name="imagenes")

# archivo base de datos
DB_FILE = "db.json"

# crear archivo si no existe
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)

# funciones DB
def leer_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def guardar_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

class Reporte(BaseModel):
    descripcion: str
    lat: float
    lng: float
    tipo: Optional[str] = "General"
    foto: Optional[str] = None

# IA simple
def detectar_tipo(descripcion):
    desc = descripcion.lower()
    if "bache" in desc or "hoyo" in desc:
        return "Baches"
    elif "basura" in desc:
        return "Basura"
    elif "luz" in desc:
        return "Luminaria"
    elif "limpieza" in desc:
        return "Limpieza"
    else:
        return "General"

@app.get("/")
def home():
    return {"ok": True}

@app.get("/reportes")
def obtener_reportes():
    return leer_db()

@app.post("/subir-imagen")
async def subir_imagen(file: UploadFile = File(...)):
    nombre = f"{uuid.uuid4()}.jpg"
    ruta = f"imagenes/{nombre}"

    with open(ruta, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "url": f"https://civitas-moci-production.up.railway.app/imagenes/{nombre}"
    }

@app.post("/reportes")
def crear_reporte(reporte: Reporte):

    data = leer_db()

    nuevo = reporte.dict()
    nuevo["tipo"] = detectar_tipo(reporte.descripcion)

    data.append(nuevo)

    guardar_db(data)

    return {"ok": True}