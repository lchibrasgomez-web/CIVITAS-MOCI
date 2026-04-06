from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

# 🔥 CORS TOTAL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 BASE DE DATOS SIMPLE (archivo)
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

@app.get("/")
def home():
    return {"ok": True}

@app.get("/reportes")
def get_reportes():
    return leer()

@app.post("/reportes")
def post_reporte(r: Reporte):
    data = leer()
    data.append(r.dict())
    guardar(data)
    return {"ok": True}