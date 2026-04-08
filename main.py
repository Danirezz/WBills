from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from datetime import date

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

#Modelo de datos (PYDANTIC)
class Gasto(BaseModel):
    id: int                   
    monto: float              
    categoria: str            
    descripcion: str          
    fecha: str                
    pagado: bool = True       

# Base de datos temporal (lista en memoria)
gastos_db = []

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# 1. GET - Leer todos los gastos
@app.get("/api/gastos")
def obtener_todos_gastos():
    """Devuelve todos los gastos almacenados"""
    return {"total": len(gastos_db), "gastos": gastos_db}

# 2. POST - Crear un nuevo gasto
@app.post("/api/gastos")
def crear_gasto(gasto: Gasto):
    """Crea un nuevo gasto y lo guarda en la lista"""
    # Convertir el objeto Pydantic a diccionario
    gasto_dict = gasto.dict()
    gastos_db.append(gasto_dict)
    return {
        "mensaje": "Gasto creado exitosamente",
        "gasto": gasto_dict,
        "total_gastos": len(gastos_db)
    }

# 3. GET - Buscar gasto específico por ID (Path Parameter)
@app.get("/api/gastos/{gasto_id}")
def obtener_gasto_por_id(gasto_id: int):
    """Busca un gasto específico por su ID"""
    for gasto in gastos_db:
        if gasto["id"] == gasto_id:
            return {"gasto": gasto}
    
    # Si no existe, lanzar error 404
    raise HTTPException(
        status_code=404,
        detail=f"Gasto con ID {gasto_id} no encontrado"
    )

# 4. DELETE - Eliminar gasto por ID
@app.delete("/api/gastos/{gasto_id}")
def eliminar_gasto(gasto_id: int):
    """Elimina un gasto por su ID"""
    for i, gasto in enumerate(gastos_db):
        if gasto["id"] == gasto_id:
            gasto_eliminado = gastos_db.pop(i)
            return {
                "mensaje": "Gasto eliminado exitosamente",
                "gasto": gasto_eliminado
            }
    
    raise HTTPException(
        status_code=404,
        detail=f"Gasto con ID {gasto_id} no encontrado"
    )

# 5. GET - Filtrado dinámico por categoría (Query Parameter)
@app.get("/api/gastos/filtrar/categoria")
def filtrar_gastos_por_categoria(categoria: Optional[str] = None):
    """Filtra gastos por categoría (opcional)"""
    if categoria is None:
        return {"gastos": gastos_db, "total": len(gastos_db)}
    
    gastos_filtrados = [
        gasto for gasto in gastos_db 
        if gasto["categoria"].lower() == categoria.lower()
    ]
    
    return {
        "categoria": categoria,
        "gastos": gastos_filtrados,
        "total": len(gastos_filtrados)
    }

@app.get("/api/test")
def test():
    return {"mensaje": "API OK"}

