from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, joinedload
from sqlalchemy import String, Integer, ForeignKey, Enum, DateTime, text, create_engine, Select
from markupsafe import escape
from werkzeug.utils import secure_filename
import datetime
import hashlib
import filetype
import os



UPLOAD_FOLDER = 'static/uploads'

class Base(DeclarativeBase):
    pass


class Region(Base):
    __tablename__ = "region"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)

    comunas: Mapped[list["Comuna"]] = relationship(back_populates="region")


class Comuna(Base):
    __tablename__ = "comuna"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)

    region_id: Mapped[int] = mapped_column(
        ForeignKey("region.id", ondelete="NO ACTION", onupdate="NO ACTION"),
        nullable=False,
        index=True,
    )
    region: Mapped["Region"] = relationship(back_populates="comunas")

    avisos: Mapped[list["Aviso_adopcion"]] = relationship(back_populates="comuna")


class Aviso_adopcion(Base):
    __tablename__ = "aviso_adopcion"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    fecha_ingreso: Mapped[datetime.datetime] = mapped_column(nullable=False)
    comuna_id: Mapped[int] = mapped_column(
        ForeignKey("comuna.id", ondelete="NO ACTION", onupdate="NO ACTION"),
        nullable=False,
        index=True,
    )
    sector: Mapped[str] = mapped_column(String(100), nullable=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    celular: Mapped[str] = mapped_column(String(15), nullable=True)
    tipo: Mapped[str] = mapped_column(Enum("gato", "perro"), nullable=False)
    cantidad: Mapped[int] = mapped_column(nullable=False)
    edad: Mapped[int] = mapped_column(nullable=False)
    unidad_medida: Mapped[str] = mapped_column(Enum("a", "m"), nullable=False)
    fecha_entrega: Mapped[datetime.datetime] = mapped_column(nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=True)

    comuna: Mapped["Comuna"] = relationship(back_populates="avisos")
    fotos: Mapped[list["Foto"]] = relationship(back_populates="aviso")
    contactos: Mapped[list["Contactar_por"]] = relationship(back_populates="aviso")
    comentarios: Mapped[list["comentario"]] = relationship(back_populates="aviso")

class Foto(Base):
    __tablename__ = "foto"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    ruta_archivo: Mapped[str] = mapped_column(String(300), nullable=False)
    nombre_archivo: Mapped[str] = mapped_column(String(300), nullable=False)
    aviso_id: Mapped[int] = mapped_column(
        ForeignKey("aviso_adopcion.id", ondelete="NO ACTION", onupdate="NO ACTION"),
        nullable=False,
        index=True,
    )

    aviso: Mapped["Aviso_adopcion"] = relationship(back_populates="fotos")


class Contactar_por(Base):
    __tablename__ = "contactar_por"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    nombre: Mapped[str] = mapped_column(
        Enum("whatsapp", "telegram", "X", "instagram", "tiktok", "otra"),
        nullable=False,
    )
    identificador: Mapped[str] = mapped_column(String(150), nullable=False)
    aviso_id: Mapped[int] = mapped_column(
        ForeignKey("aviso_adopcion.id", ondelete="NO ACTION", onupdate="NO ACTION"),
        nullable=False,
        index=True,
    )

    aviso: Mapped["Aviso_adopcion"] = relationship(back_populates="contactos")

class comentario(Base):
    __tablename__ = "comentario"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    contenido: Mapped[str] = mapped_column(String(500), nullable=False)
    fecha_publicacion: Mapped[datetime.datetime] = mapped_column(
        nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    aviso_id: Mapped[int] = mapped_column(
        ForeignKey("aviso_adopcion.id", ondelete="NO ACTION", onupdate="NO ACTION"),
        nullable=False,
        index=True,
    )
    aviso: Mapped["Aviso_adopcion"] = relationship(back_populates="comentarios")


DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8" 

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)


# -- query --

def getEstadisticasAdopciones():
    sesion = SessionLocal()
    total_avisos = sesion.query(Aviso_adopcion).all()
    datos_estadisticas = []
    for aviso in total_avisos:
            datos_estadisticas.append({
                'fecha': aviso.fecha_ingreso.strftime('%Y-%m-%d'),
                'tipo': aviso.tipo,
                'cantidad': aviso.cantidad,
                'comuna': aviso.comuna.nombre
            })
    sesion.close()
    return datos_estadisticas




def getAllAvisos():
    sesion = SessionLocal()
    avisos = sesion.query(Aviso_adopcion).options(joinedload(Aviso_adopcion.fotos)).all()
    sesion.close()
    return avisos

def getFirst5Avisos(limitN, offsetN):
    sesion = SessionLocal()
    avisos = sesion.query(Aviso_adopcion).options(joinedload(Aviso_adopcion.fotos)).offset(offsetN).limit(limitN).all()
    sesion.close()
    return avisos

def getAvisoById(id):
    sesion = SessionLocal()
    aviso = sesion.query(Aviso_adopcion).filter_by(id=id).first()
    sesion.close()
    return aviso

def getAllRegionesYComunasJSON():
    sesion = SessionLocal()
    regiones = sesion.query(Region).options(joinedload(Region.comunas)).all()
    data = []
    for r in regiones:
        dataComuna = []
        for comuna in r.comunas:
            dataComuna.append({"id": comuna.id, "nombre": comuna.nombre})
        data.append({"id": r.id, "nombre": r.nombre, "comunas": dataComuna})
    sesion.close()
    return data

def validacionRegionYComuna(region,comuna):
    sesion = SessionLocal()
    existeRegionyComuna = (sesion.query(Comuna).join(Region).filter(Region.nombre == region, Comuna.nombre == comuna).first())
    sesion.close()
    return bool(existeRegionyComuna)

def validacionRegion(region):
    sesion = SessionLocal()
    existeRegion = sesion.query(Region).filter_by(nombre=region).all()
    sesion.close()
    return bool(existeRegion)


def getAllComunas():
    sesion = SessionLocal()
    comunas = sesion.query(Comuna).all()
    sesion.close()
    return comunas

def getIdComunaByName(comuna):
    sesion = SessionLocal()
    comuna = sesion.query(Comuna).filter_by(nombre=comuna).first()
    sesion.close()
    return comuna.id

def getNameComunaById(id):
    sesion = SessionLocal()
    comuna = sesion.query(Comuna).filter_by(id=id).first()
    sesion.close()
    return comuna.nombre 

def getOneImageByAvisoId(AvisoId):
    sesion = SessionLocal()
    imagen = sesion.query(Foto).filter_by(aviso_id=AvisoId).first()
    sesion.close()
    return imagen

def getAllImagesByAvisoId(AvisoId):
    sesion = SessionLocal()
    imagen = sesion.query(Foto).filter_by(aviso_id=AvisoId).all()
    sesion.close()
    return imagen

def getContactoByIdAviso(avisoId):
    sesion = SessionLocal()
    contacto = sesion.query(Contactar_por).filter_by(aviso_id=avisoId).first()
    sesion.close()
    return contacto

def getFotosByIdAviso(avisoId):
    sesion = SessionLocal()
    fotos = sesion.query(Foto).filter_by(aviso_id=avisoId).all()
    sesion.close()
    return fotos 

def addAviso(comuna,sector,nombre,email,
    celular,tipo,cantidad,edad,unidad_medida,
    fecha_entrega,descripcion,nombreContacto,
    urlContacto,fotos, appVAR):

    sesion = SessionLocal()

    try:
        aviso = Aviso_adopcion(
            fecha_ingreso=datetime.datetime.now(),
            comuna_id=int(comuna),
            sector=sector,
            nombre=nombre,
            email=email,
            celular=celular,
            tipo=tipo,
            cantidad=float(cantidad),
            edad=float(edad),
            unidad_medida=unidad_medida,
            fecha_entrega=fecha_entrega,
            descripcion=descripcion
        )
        sesion.add(aviso)
        sesion.flush()

        contacto = Contactar_por(
            nombre=nombreContacto,
            identificador=urlContacto,
            aviso_id=aviso.id
        )
        sesion.add(contacto)
        listfotos=[]
        for i in fotos:
            _filename = hashlib.sha256(
            secure_filename(i.filename) # nombre del archivo
            .encode("utf-8") # encodear a bytes
            ).hexdigest()
            _extension = filetype.guess(i).extension
            img_filename = f"{_filename}.{_extension}"

            i.save(os.path.join(appVAR.config["UPLOAD_FOLDER"], img_filename))
            ruta=os.path.join(appVAR.config["UPLOAD_FOLDER"], img_filename)

            foto = Foto(
                ruta_archivo=ruta,
                nombre_archivo=img_filename,
                aviso_id=aviso.id)

            listfotos.append(foto)
        
        for j in listfotos:
            sesion.add(j)
        sesion.commit()
        sesion.close()
        return True
    except Exception as e: #se supone que aqui nunca deberian haber errores 
        #print(type(e))
        #print(e)
        sesion.rollback() 
        sesion.close()
        return False
