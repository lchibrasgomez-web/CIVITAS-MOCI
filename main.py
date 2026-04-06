from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json, os, shutil, uuid

app = FastAPI()

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

DB = "db.json"

if not os.path.exists(DB):
    with open(DB, "w") as f:
        json.dump([], f)

def leer():
    with open(DB, "r") as f:
        return json.load(f)

def guardar(data):
    with open(DB, "w") as f:
        json.dump(data, f)

class Reporte(BaseModel):
    descripcion: str
    lat: float
    lng: float
    tipo: str = "General"
    foto: str = ""

@app.get("/")
def home():
    return {"ok": True}

@app.get("/reportes")
def get_reportes():
    return leer()

@app.post("/subir-imagen")
async def subir_imagen(file: UploadFile = File(...)):
    nombre = f"{uuid.uuid4()}.jpg"
    ruta = f"imagenes/{nombre}"

    with open(ruta, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"url": f"https://civitas-moci-production.up.railway.app/imagenes/{nombre}"}

@app.post("/reportes")
def post_reporte(r: Reporte):
    data = leer()
    data.append(r.dict())
    guardar(data)
    return {"ok": True}