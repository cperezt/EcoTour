from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Usuarios(Base):
    __tablename__ = 'usuarios'

    idusuario = Column(Integer, primary_key=True, index=True)
    nombreusuario = Column(String(100))
    documentousuario = Column(String(11))
    telefonousuario = Column(String(11))
    correousuario = Column(String(100))
    passwordusuario = Column(String(100))
    estadousuario = Column(String(10))

class Destinos(Base):
    __tablename__ = 'destinos'
    iddestino = Column(Integer, primary_key=True, index=True)
    nombredestino = Column(String(100))
    descripciondestino = Column(String(500))
    estadodestino = Column(String(20))
    fotodestino = Column(String(200))

class Operadores(Base):
    __tablename__ = 'operadores'
    idoperador = Column(Integer, primary_key=True, index=True)
    nitoperador = Column(String(14))
    razonsocialoperador = Column(String(100))
    descripcionoperador = Column(String(500))
    estadooperador = Column(String(20))
    idciudadoperador = Column(Integer)

class Tipoplan(Base):
    __tablename__="tipoplan"
    idtipoplan = Column(Integer,primary_key=True, index=True)
    nombretipoplan = Column(String(100))

class Rol(Base):
    __tablename__="rol"
    idrol = Column(Integer,primary_key=True, index=True)
    nombrerol = Column(String(100))

