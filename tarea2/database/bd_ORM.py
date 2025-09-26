from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy import String, Integer, ForeignKey, Enum, DateTime, text, create_engine, Select
import datetime


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


DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8" 

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

'''
def get_session():
    engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}", echo=True)
    session = Session(engine)
    return session
'''



# -- query --
'''
def getAllAvisos():
    session = SessionLocal()
    avisos = session.query(select(Aviso_adopcion)).all()
    session.close()
    return avisos 
'''

def getFirst5Avisos():
    sesion = SessionLocal()
    avisos = sesion.query(Aviso_adopcion).limit(5).all()
    sesion.close()
    return avisos

'''    
def getAvisobyId(idAviso):
    session = SessionLocal()
    cursor = session.cursor()
    stmt = select(Aviso_adopcion).where(Aviso_adopcion.id == idAviso)
    aviso = sesion.scalars(stmt)
    session.close()
    return aviso
'''   

def getAllRegionesYComunasJSON():
    sesion = SessionLocal()
    regiones = sesion.query(Region).all()
    data = [
    {
        "id": r.id,
        "nombre": r.nombre,
        "comunas": [{"id": c.id, "nombre": c.nombre} for c in r.comunas]
    }
    for r in regiones
    ]
    #dataRyC = []
    #for r in regiones:
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
    comuna = sesion.query(Comuna).filter_by(nombre == comuna).first()
    sesion.close()
    return comuna.id

def addAviso(comuna,
            sector,
            nombre,
            email,
            celular,
            tipo,
            cantidad,
            edad,
            unidad_medida,
            fecha_entrega,
            descripcion,
            ## entidad contactar_por
            
            nombreContacto,
            urlContacto,

            ## foto (lista de fotos)
            fotos):
            
    try:
        aviso = Aviso_adopcion(
            comuna,
            sector,
            nombre,
            email,
            celular,
            tipo,
            cantidad,
            edad,
            unidad_medida,
            fecha_entrega,
            descripcion
        )

        contacto = Contactar_por(
            nombreContacto,
            urlContacto,
            aviso.id
        )

        for i in foto:
            _filename = hashlib.sha256(
            secure_filename(i.filename) # nombre del archivo
            .encode("utf-8") # encodear a bytes
            ).hexdigest()
            _extension = filetype.guess(i).extension
            img_filename = f"{_filename}.{_extension}"

                    # 2. save img as a file
            i.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))

            foto = Foto(
                os.path.join(app.config["UPLOAD_FOLDER"], img_filename,
                img_filename,
                aviso.id)
            )

        sesion.close()
        return True
    except Exception as e: #se supone que aqui nunca deberian 
        sesion.rollback() # haber errores
        sesion.close()
        return False

'''
def addContacto():
    return'''

'''
def addAviso(fecha_ingreso, comuna_id, sector, nombre,
    email, celular, tipo, cantidad,edad,
    unidad_medida,fecha_entrega,descripcion):
    session = get_session()
    cursor = session.cursor()
    aviso = Aviso_adopcion(
        fecha_ingreso=fecha_ingreso,
        comuna_id=comuna_id
        sector=sector
        nombre=nombre
        email=email
        celular=celular
        tipo=tipo
        cantidad=cantidad
        edad=edad
        unidad_medida=unidad_medida
        fecha_entrega=fecha_entrega
        descripcion=descripcion
    )
    try:
        session.add(aviso)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
            

def addFoto(id, ruta_archivo, nombre_archivo, aviso_id):
    session = get_session()
    cursor = session.cursor()
    foto = Foto(
        ruta_archivo=ruta_archivo,
        nombre_archivo=nombre_archivo,
        aviso_id= aviso_id
    )
    try:
        session.add(foto)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False

def addContacto(nombre, identificador, actividad_id):
    session = get_session()
    cursor = session.cursor()
    contacto = Contactar_por(
        nombre = nombre,
        identificador = identificador,
        actividad_id = actividad_id
    )
    try:
        session.add(contacto)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    

def addAllAvisoCompleto():
    session = get_session()
    cursor = session.cursor()
    # aqui deben hacerse las validaciones para las adopciones, fotos y contacto
'''
