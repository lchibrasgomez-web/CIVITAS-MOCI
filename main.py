from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

reportes = []

# 🔥 GET (ARREGLA ERROR)
@app.get("/reportes")
def obtener_reportes():
    return reportes

# 🔥 POST
@app.post("/reportes")
def crear_reporte(data: dict):
    reportes.append(data)
    return {"ok": True}

@app.post("/login")
def login():
    return {"ok": True, "admin": True}

@app.post("/register")
def register():
    return {"ok": True}