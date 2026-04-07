from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USERS = "users.json"
DB = "db.json"

# crear archivos si no existen
for file in [USERS, DB]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)

def leer(file):
    with open(file, "r") as f:
        return json.load(f)

def guardar(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# 🔐 MODELOS
class Usuario(BaseModel):
    username: str
    password: str
    nombre: str = ""
    telefono: str = ""

class Reporte(BaseModel):
    descripcion: str
    lat: float
    lng: float
    user: str

# 🔥 REGISTER
@app.post("/register")
def register(u: Usuario):
    users = leer(USERS)

    # evitar duplicados
    for user in users:
        if user["username"] == u.username:
            return {"ok": False, "msg": "Usuario ya existe"}

    nuevo = {
        "username": u.username.strip(),
        "password": u.password.strip(),
        "nombre": u.nombre,
        "telefono": u.telefono,
        "admin": u.username.strip().lower() == "admin"
    }

    users.append(nuevo)
    guardar(USERS, users)

    return {"ok": True}

# 🔥 LOGIN (CORREGIDO)
@app.post("/login")
def login(u: Usuario):
    users = leer(USERS)

    for user in users:
        if (
            user["username"].strip() == u.username.strip()
            and user["password"].strip() == u.password.strip()
        ):
            return {
                "ok": True,
                "admin": user.get("admin", False)
            }

    return {"ok": False}

# 🔥 REPORTES
@app.get("/reportes/{user}")
def get_reportes(user: str):
    data = leer(DB)

    if user.lower() == "admin":
        return data

    return [r for r in data if r["user"] == user]

@app.post("/reportes")
def post_reporte(r: Reporte):
    data = leer(DB)
    data.append(r.dict())
    guardar(DB, data)
    return {"ok": True}