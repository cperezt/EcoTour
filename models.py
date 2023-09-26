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