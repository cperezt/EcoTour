from fastapi import FastAPI, HTTPException, Depends, status
from mangum import Mangum
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session, exc
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

class PlanBase(BaseModel):
    nombreplan: str
    idtipoplanplanes: int
    valorplan: float
    descripcionplan: str
    estadoplan: str
    fotoplan: str
    idoperadorplan: int
    iddestinoplan: int

class PlanBaseUpdate(BaseModel):
    idplan: int
    nombreplan: str
    idtipoplanplanes: int
    valorplan: float
    descripcionplan: str
    estadoplan: str
    fotoplan: str
    idoperadorplan: int
    iddestinoplan: int


class RolBase(BaseModel):
    nombrerol: str

class RolBaseUpdate(BaseModel):
    idrol: int
    nombrerol: str

class TipoPlanBase(BaseModel):
    nombretipoplan:str

class TipoPlanBaseUpdate(BaseModel):
    idtipoplan:str
    nombretipoplan:str

class OperadorBase(BaseModel):
    nitoperador:str
    razonsocialoperador:str
    descripcionoperador:str
    estadooperador:str
    idciudadoperador:int

class OperadorBaseUpdate(BaseModel):
    idoperador:str
    nitoperador:str
    razonsocialoperador:str
    descripcionoperador:str
    estadooperador:str
    idciudadoperador:int

class DestinoBase (BaseModel):
    nombredestino:str
    descripciondestino:str
    estadodestino:str
    fotodestino:str

class DestinoBase2 (BaseModel):
    iddestino:int
    nombredestino:str
    descripciondestino:str
    estadodestino:str
    fotodestino:str

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
'''------------------***************************************************----------------------------------
                                    API USUARIOS                                 
---------------------***************************************************---------------------------------'''
#API Usuarios
@app.post("/usuarios/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: UsuarioBase, db: db_dependency ):
    db_usuario = models.Usuarios(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    return "Usuario creado exitosamente"

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
    
'''------------------***************************************************----------------------------------
                                    API DESTINOS                                 
---------------------***************************************************---------------------------------'''

@app.post("/destinos/", status_code=status.HTTP_201_CREATED)
async def crear_destino(destino: DestinoBase, db: db_dependency ):
    db_destino = models.Destinos(**destino.dict())
    db.add(db_destino)
    db.commit()
    return "Destino creado exitosamente"

@app.delete("/destinos/{id_destino}", status_code=status.HTTP_200_OK)
async def borrar_usuario(id_destino:int, db:db_dependency):
    destinoBorrar = db.query(models.Destinos).filter(models.Destinos.iddestino== id_destino).first()
    if destinoBorrar is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(destinoBorrar)
    db.commit()
    return "Destino eliminado exitosamente"

@app.get("/listardestinos/", status_code=status.HTTP_200_OK)
async def mostrar_todos_los_destinos(db:db_dependency):
    destinos = db.query(models.Destinos).all()
    return destinos

@app.get("/destinos/{id_destino}", status_code=status.HTTP_200_OK)
async def mostrar_destino_por_id(id_destino: int, db:db_dependency):
    destino = db.query(models.Destinos).filter(models.Destinos.iddestino==id_destino).first()
    if destino is None:
        raise HTTPException(status_code=404, detail="destino no encontrado")
    return destino

@app.post("/destinoupdate/", status_code=status.HTTP_200_OK)
async def actualizar_datos_destino(destino: DestinoBase2, db:db_dependency):
    destinoactualizar = db.query(models.Destinos).filter(models.Destinos.iddestino==destino.iddestino).first()
    if destinoactualizar is None:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    destinoactualizar.nombredestino = destino.nombredestino
    destinoactualizar.descripciondestino = destino.descripciondestino
    destinoactualizar.estadodestino = destino.estadodestino
    destinoactualizar.fotodestino = destino.fotodestino
    db.commit()
    return "Destino actualizado exitosamente"

@app.get("/estadodestinoupdate/{id_destino}", status_code=status.HTTP_200_OK)
async def actualizar_datos_destino(id_destino:int, db:db_dependency):
    destinoactualizar = db.query(models.Destinos).filter(models.Destinos.iddestino==id_destino).first()
    if destinoactualizar is None:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    if destinoactualizar.estadodestino == "Activo":
        destinoactualizar.estadodestino = "Inactivo"
        valor = "Inactivo"
    else:
        destinoactualizar.estadodestino = "Activo"
        valor = "Activo"
    db.commit()
    return "Estado destino actualizado exitosamente a: "+valor

'''------------------***************************************************----------------------------------
                                    API OPERADORES                               
---------------------***************************************************---------------------------------'''

@app.post("/operador/", status_code=status.HTTP_201_CREATED)
async def crear_operador(operador: OperadorBase, db: db_dependency ):
    iddestinoexiste = db.query(models.Destinos).filter(models.Destinos.iddestino==operador.idciudadoperador).first()
    if iddestinoexiste is None:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    db_operador = models.Operadores(**operador.dict())
    db.add(db_operador)
    db.commit()  
    return "Operador creado exitosamente"

@app.delete("/operador/{id_operador}", status_code=status.HTTP_200_OK)
async def borrar_operador (id_operador:int, db:db_dependency):
    operadorBorrar = db.query(models.Operadores).filter(models.Operadores.idoperador==id_operador).first()
    if operadorBorrar is None:
        raise HTTPException(status_code=404, detail="Operador no encontrado")
    db.delete(operadorBorrar)
    db.commit()
    return "Operador eliminado exitosamente"

@app.get("/listaroperadores/", status_code=status.HTTP_200_OK)
async def listar_operadores (db:db_dependency):
    listaOperadores = db.query(models.Operadores).all()
    return listaOperadores

@app.get("/operadores/{id_operador}", status_code=status.HTTP_200_OK)
async def buscar_operador_por_id(id_operador:int, db:db_dependency):
    operador = db.query(models.Operadores).filter(models.Operadores.idoperador==id_operador).first()
    if operador is None:
        raise HTTPException(status_code=404, detail="Operador no encontrado")
    return operador

@app.get("/operadoresciudad/{id_ciudad}", status_code=status.HTTP_200_OK)
async def buscar_operadores_por_ciudad(id_ciudad:int, db:db_dependency):
    operador = db.query(models.Operadores).filter(models.Operadores.idciudadoperador==id_ciudad).all()
    if operador is None:
        raise HTTPException(status_code=404, detail="Operador no encontrado")
    return operador

@app.post("/operadorupdate/", status_code=status.HTTP_200_OK)
async def actualizar_datos_destino(operador: OperadorBaseUpdate, db:db_dependency):
    iddestinoexiste = db.query(models.Destinos).filter(models.Destinos.iddestino==operador.idciudadoperador).first()
    if iddestinoexiste is None:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    operadoraactualizar = db.query(models.Operadores).filter(models.Operadores.idoperador==operador.idoperador).first()
    if operadoraactualizar is None:
        raise HTTPException(status_code=404, detail="operadora no encontrado")
    operadoraactualizar.nitoperador=operador.nitoperador
    operadoraactualizar.razonsocialoperador = operador.razonsocialoperador
    operadoraactualizar.descripcionoperador = operador.descripcionoperador
    operadoraactualizar.estadooperador = operador.estadooperador
    operadoraactualizar.idciudadoperador = operador.idciudadoperador
    db.commit()
    return "Operador actualizado exitosamente"

@app.get("/estadooperadorupdate/{id_operador}", status_code=status.HTTP_200_OK)
async def actualizar_datos_operador(id_operador:int, db:db_dependency):
    operadoractualizar = db.query(models.Operadores).filter(models.Operadores.idoperador==id_operador).first()
    if operadoractualizar is None:
        raise HTTPException(status_code=404, detail="Operador no encontrado")
    if operadoractualizar.estadooperador == "Activo":
        operadoractualizar.estadooperador = "Inactivo"
        valor = "Inactivo"
    else:
        operadoractualizar.estadooperador = "Activo"
        valor = "Activo"
    db.commit()
    return "Estado operador actualizado exitosamente a: "+valor

'''------------------***************************************************----------------------------------
                                    API TIPO PLAN                               
---------------------***************************************************---------------------------------'''

@app.post("/tipoplan/", status_code=status.HTTP_201_CREATED)
async def crear_tipo_plan (tipoplan: TipoPlanBase, db:db_dependency):
    tipoplan = models.Tipoplan(**tipoplan.dict())
    db.add(tipoplan)
    db.commit()
    return "Tipo de plan creado exitosamente"

  
@app.get("/tipoplan/", status_code=status.HTTP_200_OK)
async def listar_tipos_de_planes (db:db_dependency):
    listaTiposPlan = db.query(models.Tipoplan).all()
    return listaTiposPlan

@app.get("/tipoplan/{id_tipoplan}", status_code=status.HTTP_200_OK)
async def buscar_tipo_plan_por_id(id_tipoplan:int, db:db_dependency):
    tipoPlan = db.query(models.Tipoplan).filter(models.Tipoplan.idtipoplan==id_tipoplan).first()
    if tipoPlan is None:
        raise HTTPException(status_code=404, detail="Tipo de plan no encontrado")
    return tipoPlan

@app.delete("/tipoplan/{id_tipoplan}", status_code=status.HTTP_200_OK)
async def eliminar_tipo_plan (id_tipoplan:int, db:db_dependency):
    tipoPlanAEliminar = db.query(models.Tipoplan).filter(models.Tipoplan.idtipoplan==id_tipoplan).first()
    if tipoPlanAEliminar is None:
        raise HTTPException (status_code=404, detail="Tipo de plan no encontrado")
    db.delete(tipoPlanAEliminar)
    db.commit()
    return "Tipo de plan eliminado exitosamente"

@app.post("/tipoplanupdate/", status_code=status.HTTP_200_OK)
async def actualizar_tipo_plan(tipoplan:TipoPlanBaseUpdate, db:db_dependency):
    tipoPlanAActualizar = db.query(models.Tipoplan).filter(models.Tipoplan.idtipoplan==tipoplan.idtipoplan).first()
    if tipoPlanAActualizar is None:
        raise HTTPException(status_code=404, detail="Tipo de plan no encontrado")
    tipoPlanAActualizar.nombretipoplan=tipoplan.nombretipoplan
    db.commit()
    return "Tipo de plan actualizado correctamente"

  
'''------------------***************************************************----------------------------------
                                    API ROL                                 
---------------------***************************************************---------------------------------'''

@app.post("/roles/", status_code=status.HTTP_201_CREATED)
async def crear_rol(rol: RolBase, db:db_dependency):
    rol = models.Rol(**rol.dict())
    db.add(rol)
    db.commit()
    return "Rol creado exitosamente"

@app.get("/roles/", status_code=status.HTTP_200_OK)
async def listar_roles(db:db_dependency):
    listaRoles = db.query(models.Rol).all()
    return listaRoles

@app.get("/roles/{id_rol}", status_code=status.HTTP_200_OK)
async def buscar_rol_por_id(id_rol:int, db:db_dependency):
    rol = db.query(models.Rol).filter(models.Rol.idrol==id_rol).first()
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@app.delete("/roles/{id_rol}", status_code=status.HTTP_200_OK)
async def eliminar_rol(id_rol:int, db:db_dependency):
    rolAEliminar = db.query(models.Rol).filter(models.Rol.idrol==id_rol).first()
    if rolAEliminar is None:
        raise HTTPException (status_code=404, detail="Rol no encontrado")
    db.delete(rolAEliminar)
    db.commit()
    return "Rol eliminado exitosamente"

@app.post("/rolesupdate/", status_code=status.HTTP_200_OK)
async def actualizar_rol(rol:RolBaseUpdate, db:db_dependency):
    rolAActualizar = db.query(models.Rol).filter(models.Rol.idrol==rol.idrol).first()
    if rolAActualizar is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    rolAActualizar.nombrerol=rol.nombrerol
    db.commit()
    return "Rol actualizado correctamente"

'''------------------***************************************************----------------------------------
                                    API PLANES                               
---------------------***************************************************---------------------------------'''

@app.post("/planes/", status_code=status.HTTP_201_CREATED)
async def crear_plan(plan: PlanBase, db:db_dependency):
    # Validamos que el valor del campo idtipoplanes exista en la tabla tipoplan
    tipoplan = db.query(models.Tipoplan).filter(models.Tipoplan.idtipoplans==plan.idtipoplanplanes).first()
    if tipoplan is None:
        raise HTTPException(status_code=404, detail="El tipo de plan no existe")

    # Validamos que el valor del campo iddestinoplan exista en la tabla destinos
    destino = db.query(models.Destinos).filter(models.Destinos.iddestino==plan.iddestinoplan).first()
    if destino is None:
        raise HTTPException(status_code=404, detail="El destino no existe")

    # Validamos que el valor en el campo idoperadorplan exista en la tabla operadores
    operador = db.query(models.Operadores).filter(models.Operadores.idoperador==plan.idoperadorplan).first()
    if operador is None:
        raise HTTPException(status_code=404, detail="El operador no existe")

    plan = models.Plan(**plan.dict())
    db.add(plan)
    db.commit()
    return "Plan creado exitosamente"
