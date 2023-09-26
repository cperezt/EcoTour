from fastapi import FastAPI, HTTPException, Depends, status
from mangum import Mangum
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Config CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
handler = Mangum(app)
models.Base.metadata.create_all(bind=engine)



class UsuarioBase (BaseModel):
    nombreusuario:str
    documentousuario:str
    telefonousuario:str
    correousuario:str
    passwordusuario:str
    estadousuario:str

class UsuarioBase2 (BaseModel):
    id_usuario:str
    nombreusuario:str
    documentousuario:str
    telefonousuario:str
    correousuario:str
    passwordusuario:str
    estadousuario:str
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/usuarios/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: UsuarioBase, db: db_dependency ):
    db_usuario = models.Usuarios(**usuario.dict())
    db.add(db_usuario)
    db.commit()

@app.get("/usuarios/{id_usuario}", status_code=status.HTTP_200_OK)
async def mostrar_usuario_por_id(id_usuario: int, db:db_dependency):
    usuario = db.query(models.Usuarios).filter(models.Usuarios.idusuario==id_usuario).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/listausuarios/", status_code=status.HTTP_200_OK)
async def mostrar_todos_los_usuarios(db:db_dependency):
    usuarios = db.query(models.Usuarios).all()
    return usuarios

@app.delete("/usuarios/{id_usuario}", status_code=status.HTTP_200_OK)
async def borrar_usuario(id_usuario:int, db:db_dependency):
    usuarioaborrar = db.query(models.Usuarios).filter(models.Usuarios.idusuario== id_usuario).first()
    if usuarioaborrar is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuarioaborrar)
    db.commit()

@app.post("/usuariosupdate/", status_code=status.HTTP_200_OK)
async def actualizar_datos_usuario(usuario: UsuarioBase2, db:db_dependency):
    usuarioactualizar = db.query(models.Usuarios).filter(models.Usuarios.idusuario==usuario.id_usuario).first()
    if usuarioactualizar is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuarioactualizar.nombreusuario=usuario.nombreusuario
    usuarioactualizar.documentousuario=usuario.documentousuario
    usuarioactualizar.telefonousuario = usuario.telefonousuario
    usuarioactualizar.correousuario = usuario.correousuario
    usuarioactualizar.passwordusuario = usuario.passwordusuario
    usuarioactualizar.estadousuario = usuario.estadousuario
    db.commit()
    

