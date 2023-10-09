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

class DetalleReservasBase(BaseModel):
    idreservadetalle:int
    idplandetaller:int
    fechaplanreserva:str

class DetalleReservasBaseUpdate(BaseModel):
    iddetallereserva:int
    idreservadetalle:int
    idplandetaller:int
    fechaplanreserva:str

class DetalleCotizacionBase(BaseModel):
    idcotizaciondetalle:int
    idplandetalle:int
    fechaplan:str

class DetalleCotizacionBaseUpdate(BaseModel):
    iddetallecotizacion:int
    idcotizaciondetalle:int
    idplandetalle:int
    fechaplan:str

class CotizacionBase(BaseModel):
    fechallegada: str
    fechasalida: str
    archivocotizacion: str
    estadocotizacion:str
    cantidadadultos: int
    cantidadninos: int
    ciudadorigen: str
    idusuariocotizacion: int

class CotizacionBaseUpdate(BaseModel):
    idcotizacion: int
    fehcallegada: str
    fechasalida: str
    archivocotizacion: str
    estadocotizacion:str
    cantidadadultos: int
    cantidadninos: int
    ciudadorigen: str
    idusuariocotizacion: int



class ReservaBase(BaseModel):
    saldoreserva: float
    fechareserva: str
    valorreserva: float
    estadoreserva: str
    idusuarioreserva: int

class ReservaBaseUpdate(BaseModel):
    idreserva:int
    saldoreserva: float
    fechareserva: str
    valorreserva: float
    estadoreserva: str
    idusuarioreserva: int

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
    rolusuario:int

class UsuarioBase2 (BaseModel):
    id_usuario:str
    nombreusuario:str
    documentousuario:str
    telefonousuario:str
    correousuario:str
    passwordusuario:str
    estadousuario:str
    rolusuario:int

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
    existerol = db.query(models.Rol).filter(models.Rol.idrol==usuario.rolusuario).first()
    if existerol is None:
        raise HTTPException(status_code=404, detail="Rol no existe")
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

@app.get("/usuariosporestado/{estado_usuario}", status_code=status.HTTP_200_OK)
async def mostrar_usuario_por_id(estado_usuario: str, db:db_dependency):
    usuario = db.query(models.Usuarios).filter(models.Usuarios.estadousuario==estado_usuario).all()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/listausuarios/", status_code=status.HTTP_200_OK)
async def mostrar_todos_los_usuarios(db:db_dependency):
    usuarios = db.query(models.Usuarios, models.Rol).join(models.Rol, models.Usuarios.rolusuario==models.Rol.idrol).all()
    #usuarios = db.query(models.Usuarios).all()
    return {"usuarios": [
        {
            "idusuario": usuario.idusuario,
            "nombreusuario": usuario.nombreusuario,
            "documentousuario": usuario.documentousuario,
            "telefonousuario": usuario.telefonousuario,
            "correousuario": usuario.correousuario,
            "passwordusuario": usuario.passwordusuario,
            "estadousuariousuario": usuario.estadousuario,
            "nombrerol": rol.nombrerol,
        } for usuario, rol in usuarios
    ]}
    

@app.delete("/usuarios/{id_usuario}", status_code=status.HTTP_200_OK)
async def borrar_usuario(id_usuario:int, db:db_dependency):
    usuarioaborrar = db.query(models.Usuarios).filter(models.Usuarios.idusuario== id_usuario).first()
    if usuarioaborrar is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuarioaborrar)
    db.commit()

@app.post("/usuariosupdate/", status_code=status.HTTP_200_OK)
async def actualizar_datos_usuario(usuario: UsuarioBase2, db:db_dependency):
    existerol = db.query(models.Rol).filter(models.Rol.idrol==usuario.rolusuario).first()
    if existerol is None:
        raise HTTPException(status_code=404, detail="Rol no existe")
    usuarioactualizar = db.query(models.Usuarios).filter(models.Usuarios.idusuario==usuario.id_usuario).first()
    if usuarioactualizar is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuarioactualizar.nombreusuario=usuario.nombreusuario
    usuarioactualizar.documentousuario=usuario.documentousuario
    usuarioactualizar.telefonousuario = usuario.telefonousuario
    usuarioactualizar.correousuario = usuario.correousuario
    usuarioactualizar.passwordusuario = usuario.passwordusuario
    usuarioactualizar.estadousuario = usuario.estadousuario
    usuarioactualizar.rolusuario = usuario.rolusuario
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
    tipoplan = db.query(models.Tipoplan).filter(models.Tipoplan.idtipoplan==plan.idtipoplanplanes).first()
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

    plan = models.Planes(**plan.dict())
    db.add(plan)
    db.commit()
    return "Plan creado exitosamente"

@app.get("/planes/", status_code=status.HTTP_200_OK)
async def listar_planes(db:db_dependency):
    listaPlanes = db.query(models.Planes).all()
    return listaPlanes

@app.get("/planes/{id_plan}", status_code=status.HTTP_200_OK)
async def buscar_plan_por_id(id_plan:int, db:db_dependency):
    plan = db.query(models.Planes).filter(models.Planes.idplan==id_plan).first()
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return plan

@app.delete("/planes/{id_plan}", status_code=status.HTTP_200_OK)
async def eliminar_plan(id_plan:int, db:db_dependency):
    planAEliminar = db.query(models.Planes).filter(models.Planes.idplan==id_plan).first()
    if planAEliminar is None:
        raise HTTPException (status_code=404, detail="Plan no encontrado")
    db.delete(planAEliminar)
    db.commit()
    return "Plan eliminado exitosamente"

@app.post("/planesupdate/", status_code=status.HTTP_200_OK)
async def actualizar_plan(plan:PlanBaseUpdate, db:db_dependency):
    # Validamos que el valor del campo idtipoplanes exista en la tabla tipoplan
    tipoplan = db.query(models.Tipoplan).filter(models.Tipoplan.idtipoplan==plan.idtipoplanplanes).first()
    if tipoplan is None:
        raise HTTPException(status_code=404, detail="Tipo de plan no existe")
    destino = db.query(models.Destinos).filter(models.Destinos.iddestino==plan.iddestinoplan).first()
    if destino is None:
        raise HTTPException(status_code=404, detail="El destino no existe")

    # Validamos que el valor en el campo idoperadorplan exista en la tabla operadores
    operador = db.query(models.Operadores).filter(models.Operadores.idoperador==plan.idoperadorplan).first()
    if operador is None:
        raise HTTPException(status_code=404, detail="El operador no existe")

    planAActualizar = db.query(models.Planes).filter(models.Planes.idplan==plan.idplan).first()
    if planAActualizar is None:
        raise HTTPException(status_code=404, detail="Plan no encontrado")

    planAActualizar.nombreplan=plan.nombreplan
    planAActualizar.idtipoplanplanes=plan.idtipoplanplanes
    planAActualizar.valorplan=plan.valorplan
    planAActualizar.descripcionplan=plan.descripcionplan
    planAActualizar.estadoplan=plan.estadoplan
    planAActualizar.fotoplan=plan.fotoplan
    planAActualizar.idoperadorplan=plan.idoperadorplan
    planAActualizar.iddestinoplan=plan.iddestinoplan
    db.commit()
    return "Plan actualizado correctamente"
    
'''------------------***************************************************----------------------------------
                                    API RESERVAS                               
---------------------***************************************************---------------------------------'''

@app.post("/reservas/", status_code=status.HTTP_201_CREATED)
async def crear_reserva(reserva: ReservaBase, db:db_dependency):
    reserva = models.Reservas(**reserva.dict())
    db.add(reserva)
    db.commit()
    return "Reserva creada exitosamente"

@app.get("/reservas/", status_code=status.HTTP_200_OK)
async def listar_reservas(db: db_dependency):
    listaReservas = db.query(models.Reservas).all()
    return listaReservas

@app.get("/reservas/{id_reserva}", status_code=status.HTTP_200_OK)
async def buscar_reserva_por_id(id_reserva: int, db: db_dependency):
    reserva = db.query(models.Reservas).filter(models.Reservas.idreserva==id_reserva).first()
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@app.delete("/reservas/{id_reserva}", status_code=status.HTTP_200_OK)
async def eliminar_reserva(id_reserva: int, db: db_dependency):
    reservaAEliminar = db.query(models.Reservas).filter(models.Reservas.idreserva==id_reserva).first()
    if reservaAEliminar is None:
        raise HTTPException (status_code=404, detail="Reserva no encontrada")
    db.delete(reservaAEliminar)
    db.commit()
    return "Reserva eliminada exitosamente"

@app.post("/reservasupdate/", status_code=status.HTTP_200_OK)
async def actualizar_reserva(reserva: ReservaBaseUpdate, db: db_dependency):
    usuarioExiste = db.query(models.Usuarios).filter(models.Usuarios.idusuario==reserva.idusuarioreserva).first()
    if usuarioExiste is None:
        raise HTTPException(status_code=404, detail="Usuario no existe")
    reservaAActualizar = db.query(models.Reservas).filter(models.Reservas.idreserva==reserva.idreserva).first()
    if reservaAActualizar is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    reservaAActualizar.saldoreserva=reserva.saldoreserva
    reservaAActualizar.fechareserva=reserva.fechareserva
    reservaAActualizar.valorreserva=reserva.valorreserva
    reservaAActualizar.estadoreserva=reserva.estadoreserva
    reservaAActualizar.idusuarioreserva=reserva.idusuarioreserva
    db.commit()
    return "Reserva actualizada correctamente"

@app.get("/estadoreservaupdate/{id_reserva}", status_code=status.HTTP_200_OK)
async def actualizar_datos_destino(id_reserva:int, db:db_dependency):
    reservaactualizar = db.query(models.Reservas).filter(models.Reservas.idreserva==id_reserva).first()
    if reservaactualizar is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrado")
    if reservaactualizar.estadoreserva == "Activo":
        reservaactualizar.estadoreserva = "Inactivo"
        valor = "Inactivo"
    else:
        reservaactualizar.estadoreserva = "Activo"
        valor = "Activo"
    db.commit()
    return "Estado destino actualizado exitosamente a: "+valor
'''------------------***************************************************----------------------------------
                                    API COTIZACIONES                               
---------------------***************************************************---------------------------------'''

@app.post("/cotizaciones/", status_code=status.HTTP_201_CREATED)
async def crear_cotizacion(cotizacion: CotizacionBase, db:db_dependency):
    cotizacion = models.Cotizaciones(**cotizacion.dict())
    db.add(cotizacion)
    db.commit()
    return "Cotización creada exitosamente"

@app.get("/cotizaciones/", status_code=status.HTTP_200_OK)
async def listar_cotizaciones(db:db_dependency):
    listaCotizaciones = db.query(models.Cotizaciones).all()
    return listaCotizaciones

@app.get("/cotizaciones/{id_cotizacion}", status_code=status.HTTP_200_OK)
async def buscar_cotizacion_por_id(id_cotizacion: int, db:db_dependency):
    cotizacion = db.query(models.Cotizaciones).filter(models.Cotizaciones.idcotizacion==id_cotizacion).first()
    if cotizacion is None:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    return cotizacion

@app.delete("/cotizaciones/{id_cotizacion}", status_code=status.HTTP_200_OK)
async def eliminar_cotizacion(id_cotizacion: int, db:db_dependency):
    cotizacionAEliminar = db.query(models.Cotizaciones).filter(models.Cotizaciones.idcotizacion==id_cotizacion).first()
    if cotizacionAEliminar is None:
        raise HTTPException (status_code=404, detail="Cotización no encontrada")
    db.delete(cotizacionAEliminar)
    db.commit()
    return "Cotización eliminada exitosamente"

@app.post("/cotizacionesupdate/", status_code=status.HTTP_200_OK)
async def actualizar_cotizacion(cotizacion: CotizacionBaseUpdate, db:db_dependency):
    cotizacionAActualizar = db.query(models.Cotizaciones).filter(models.Cotizaciones.idcotizacion==cotizacion.idcotizacion).first()
    if cotizacionAActualizar is None:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    cotizacionAActualizar.fechallegada=cotizacion.fehcallegada
    cotizacionAActualizar.fechasalida=cotizacion.fechasalida
    cotizacionAActualizar.archivocotizacion=cotizacion.archivocotizacion
    cotizacionAActualizar.estadocotizacion=cotizacion.estadocotizacion
    cotizacionAActualizar.cantidadadultos=cotizacion.cantidadadultos
    cotizacionAActualizar.cantidadninos=cotizacion.cantidadninos
    cotizacionAActualizar.ciudadorigen=cotizacion.ciudadorigen
    cotizacionAActualizar.idusuariocotizacion=cotizacion.idusuariocotizacion
    db.commit()
    return "Cotización actualizada correctamente"

'''------------------***************************************************----------------------------------
                                    API DETALLECOTIZACIONES                               
---------------------***************************************************---------------------------------'''

@app.post("/detallecotizaciones/", status_code=status.HTTP_201_CREATED)
async def crear_detallecotizacion(detallecotizacion: DetalleCotizacionBase, db: db_dependency):
    cotizacionexiste = db.query(models.Cotizaciones).filter(models.Cotizaciones.idcotizacion==detallecotizacion.idcotizaciondetalle).first()
    if cotizacionexiste is None:
        raise HTTPException(status_code=404, detail="No existe la cotizacion")
    planexiste = db.query(models.Planes).filter(models.Planes.idplan==detallecotizacion.idplandetalle).first()
    if planexiste is None:
        raise HTTPException(status_code=404, detail="No existe el plan")
    detallecotizacion = models.DetalleCotizacion(**detallecotizacion.dict())
    db.add(detallecotizacion)
    db.commit()
    return "Detalle de cotización creada exitosamente"

@app.get("/detallecotizaciones/", status_code=status.HTTP_200_OK)
async def listar_detallecotizaciones(db: db_dependency):
    listaDetalleCotizaciones = db.query(models.DetalleCotizacion).all()
    return listaDetalleCotizaciones

@app.get("/detallecotizaciones/{id_detallecotizacion}", status_code=status.HTTP_200_OK)
async def buscar_detallecotizacion_por_id(id_detallecotizacion: int, db: db_dependency):
    detallecotizacion = db.query(models.DetalleCotizacion).filter(models.DetalleCotizacion.iddetallecotizacion == id_detallecotizacion).first()
    if detallecotizacion is None:
        raise HTTPException(status_code=404, detail="Detalle de cotización no encontrado")
    return detallecotizacion

@app.delete("/detallecotizaciones/{id_detallecotizacion}", status_code=status.HTTP_200_OK)
async def eliminar_detallecotizacion(id_detallecotizacion: int, db: db_dependency):
    detallecotizacionAEliminar = db.query(models.DetalleCotizacion).filter(models.DetalleCotizacion.iddetallecotizacion == id_detallecotizacion).first()
    if detallecotizacionAEliminar is None:
        raise HTTPException(status_code=404, detail="Detalle de cotización no encontrado")
    db.delete(detallecotizacionAEliminar)
    db.commit()
    return "Detalle de cotización eliminada exitosamente"

@app.post("/detallecotizacionesupdate/", status_code=status.HTTP_200_OK)
async def actualizar_detallecotizacion(detallecotizacion: DetalleCotizacionBaseUpdate, db: Session = Depends(get_db)):
    cotizacionexiste = db.query(models.Cotizaciones).filter(models.Cotizaciones.idcotizacion==detallecotizacion.idcotizaciondetalle).first()
    if cotizacionexiste is None:
        raise HTTPException(status_code=404, detail="No existe la cotizacion")
    planexiste = db.query(models.Planes).filter(models.Planes.idplan==detallecotizacion.idplandetalle).first()
    if planexiste is None:
        raise HTTPException(status_code=404, detail="No existe el plan")
    detallecotizacionAActualizar = db.query(models.DetalleCotizacion).filter(models.DetalleCotizacion.iddetallecotizacion == detallecotizacion.iddetallecotizacion).first()
    if detallecotizacionAActualizar is None:
        raise HTTPException(status_code=404, detail="Detalle de cotización no encontrado")
    detallecotizacionAActualizar.idcotizaciondetalle = detallecotizacion.idcotizaciondetalle
    detallecotizacionAActualizar.idplandetalle = detallecotizacion.idplandetalle
    detallecotizacionAActualizar.fechaplan = detallecotizacion.fechaplan
    db.commit()
    return "Detalle de cotización actualizada correctamente"

'''------------------***************************************************----------------------------------
                                    API DETALLERESERVAS                               
---------------------***************************************************---------------------------------'''

@app.post("/detallereservas/", status_code=status.HTTP_201_CREATED)
async def crear_detallereserva(detallereserva: DetalleReservasBase, db: Session = Depends(get_db)):
    reservaexiste = db.query(models.Reservas).filter(models.Reservas.idreserva==detallereserva.idreservadetalle).first()
    if reservaexiste is None:
        raise HTTPException(status_code=404, detail="No existe la reserva")
    planexiste = db.query(models.Planes).filter(models.Planes.idplan==detallereserva.idplandetaller).first()
    if planexiste is None:
        raise HTTPException(status_code=404, detail="No existe el plan")
    detallereserva = models.DetalleReservas(**detallereserva.dict())
    db.add(detallereserva)
    db.commit()
    return "Detalle de reserva creada exitosamente"

@app.get("/detallereservas/", status_code=status.HTTP_200_OK)
async def listar_detallereservas(db: Session = Depends(get_db)):
    listaDetalleReservas = db.query(models.DetalleReservas).all()
    return listaDetalleReservas

@app.get("/detallereservas/{id_detallereserva}", status_code=status.HTTP_200_OK)
async def buscar_detallereserva_por_id(id_detallereserva: int, db: Session = Depends(get_db)):
    detallereserva = db.query(models.DetalleReservas).filter(models.DetalleReservas.iddetallereserva == id_detallereserva).first()
    if detallereserva is None:
        raise HTTPException(status_code=404, detail="Detalle de reserva no encontrado")
    return detallereserva

@app.delete("/detallereservas/{id_detallereserva}", status_code=status.HTTP_200_OK)
async def eliminar_detallereserva(id_detallereserva: int, db: Session = Depends(get_db)):
    detallereservaAEliminar = db.query(models.DetalleReservas).filter(models.DetalleReservas.iddetallereserva == id_detallereserva).first()
    if detallereservaAEliminar is None:
        raise HTTPException(status_code=404, detail="Detalle de reserva no encontrado")
    db.delete(detallereservaAEliminar)
    db.commit()
    return "Detalle de reserva eliminada exitosamente"

@app.post("/detallereservasupdate/", status_code=status.HTTP_200_OK)
async def actualizar_detallereserva(detallereserva: DetalleReservasBaseUpdate, db: Session = Depends(get_db)):
    detallereservaAActualizar = db.query(models.DetalleReservas).filter(models.DetalleReservas.iddetallereserva == detallereserva.iddetallereserva).first()
    if detallereservaAActualizar is None:
        raise HTTPException(status_code=404, detail="Detalle de reserva no encontrado")
    
    detallereservaAActualizar.idreservadetalle = detallereserva.idreservadetalle
    detallereservaAActualizar.idplandetaller = detallereserva.idplandetaller
    detallereservaAActualizar.fechaplanreserva = detallereserva.fechaplanreserva
    db.commit()
    return "Detalle de reserva actualizada correctamente"