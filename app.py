from flask import Flask, request, render_template, redirect, url_for, session, flash
from markupsafe import escape
from werkzeug.utils import secure_filename
from database import bd_ORM
from utils import validaciones
from datetime import datetime
import hashlib
import filetype
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}

app.secret_key = "s3cr3t_k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/') # GET
def index():
    avisos = bd_ORM.getFirst5Avisos(5,0)

    for j in avisos:
        comunaName = bd_ORM.getNameComunaById(j.comuna_id) 
        j.comuna_id = comunaName

        if j.unidad_medida == "m":
            j.unidad_medida = "meses" if j.edad > 1 else "mes"

        if j.unidad_medida == "a":
            j.unidad_medida = "años" if j.edad > 1 else "año"

    renderizado = render_template("auth/index.html", adopciones=avisos)
    return renderizado


@app.route('/listadoAdopciones')
def listadoAdopciones():
    actualPage = request.args.get("page", 1, type=int)
    avisos = bd_ORM.getFirst5Avisos(5, actualPage*5)

    for j in avisos:
        comunaName = bd_ORM.getNameComunaById(j.comuna_id) 
        j.comuna_id = comunaName
        if j.unidad_medida == "m": 
            j.unidad_medida = "meses" if j.edad > 1 else "mes"

        if j.unidad_medida == "a":
            j.unidad_medida = "años" if j.edad > 1 else "año"

    avisosAll = bd_ORM.getAllAvisos()
    largePaginas = (len(avisosAll) // 5) if len(avisosAll) % 5 != 0 else (len(avisosAll) // 5) - 1
    anteriores = list(range(1, actualPage))
    siguientes = list(range(actualPage+1, largePaginas +1 ))

    if len(anteriores) > 5:
        anterioresInversos = anteriores[-5:]
        anterioresLimitados = anterioresInversos[::]
        anterioresLimitados[0] = 1 
    elif len(anteriores) >= 1:
        anterioresLimitados = anteriores[:5]
    else:
        anterioresLimitados = anteriores

    siguientesLimitados = siguientes[:5]
    return render_template("/auth/lista.html",
    avisos=avisos, page=actualPage, anteriores=anterioresLimitados,
    siguientes=siguientesLimitados)

@app.route('/detallesAdopcion')
def detallesAdopcion():
    lastPage = request.args.get("page", 1, type=int)
    idDetalle = request.args.get("detalle", type=int)
    contactoDetalle = bd_ORM.getContactoByIdAviso(idDetalle)
    fotosDetalle = bd_ORM.getFotosByIdAviso(idDetalle)
    infoAviso = bd_ORM.getAvisoById(idDetalle)

    
    if infoAviso:
        comunaName = bd_ORM.getNameComunaById(infoAviso.comuna_id) 
        infoAviso.comuna_id = comunaName

        if infoAviso.unidad_medida == "m":
            infoAviso.unidad_medida = "meses" if infoAviso.edad > 1 else "mes"
        if infoAviso.unidad_medida == "a":
            infoAviso.unidad_medida = "años" if infoAviso.edad > 1 else "año"


    return render_template("auth/infoplantilla.html",
    adopcion=infoAviso,
    contacto=contactoDetalle,
    fotos=fotosDetalle,
    page=lastPage
    )

@app.route('/estadisticas')
def estadisticas():
    return render_template("auth/estadisticas.html")

@app.route('/formulario', methods=["GET", "POST"])
def formulario():
    if request.method == "GET": 
        regionesJSON = bd_ORM.getAllRegionesYComunasJSON()
        return render_template("auth/formulario.html", regionesYcomunas = regionesJSON)

    elif request.method == "POST":

        # validamos
        def validateFoto(file):
            ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
            ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

            if file is None:
                return False

            if file.filename == "":
                return False
            
            ftype_guess = filetype.guess(file)
            if ftype_guess.extension not in ALLOWED_EXTENSIONS:
                return False

            if ftype_guess.mime not in ALLOWED_MIMETYPES:
                return False
            return True
                
        # recuperamos los inputs #
        region = request.form.get("region")
        comuna = request.form.get("comuna")
        sector = request.form.get("sector")
        username = request.form.get("username")
        email = request.form.get("email")
        celular = request.form.get("celular")
        contacto = request.form.get("contacto")
        url_contacto = request.form.get("url-contacto")
        animal = request.form.get("animal")
        cantidad = request.form.get("cantidad")
        edad = request.form.get("edad")
        meses_anios = request.form.get("tiempo-animal")
        fecha = request.form.get("fecha")
        descripcion = request.form.get("descripcion")
        foto1 = request.files.get("foto1")
        foto2 = request.files.get("foto2")
        foto3 = request.files.get("foto3")
        foto4 = request.files.get("foto4")
        foto5 = request.files.get("foto5")
        fotosBool = True

        # inputs que si contienen fotos
        fotos = []
        validacionFotos= []

        # revisamos las validaciones de las fotos
        for i in [foto1,foto2,foto3,foto4,foto5]:
            if validateFoto(i):
                fotos.append(i)

            # falla la validacion total si una sola imagen no vacia falla
            elif not validateFoto(i) and i is not None and i.filename != "" : # fotos que estan malas
                fotosBool = False
        
        # guardamos los archivos que fallan
        if not fotosBool:
            for j in [foto1,foto2,foto3,foto4,foto5]:
                    if not validateFoto(j) and j.filename != "":
                        validacionFotos.append(j)

        # el otro caso donde no hay fotos realmente
        if not fotos and fotosBool:
            fotosBool = False
            validacionFotos = ["no hay fotos"]

        # validacion de todo los inputs que no sean la foto
        validacionTotal = validaciones.validateAll(region, comuna, sector, username, email, celular,
        contacto, url_contacto, animal, cantidad, edad, meses_anios,
        fecha, descripcion)

        # si ambas validaciones cumplen
        if  fotosBool and not validacionTotal:

            # agregamos el input a la bd
            idComuna = bd_ORM.getIdComunaByName(comuna)

            #tiempo default
            fechaDatetime = datetime.strptime(fecha, "%Y-%m-%dT%H:%M")

            agregacion = bd_ORM.addAviso(
                    comuna=idComuna,
                    sector=sector,
                    nombre=username,
                    email=email,
                    celular=celular,
                    tipo=animal,
                    cantidad=cantidad,
                    edad=edad,
                    unidad_medida=meses_anios,
                    fecha_entrega=fechaDatetime,
                    descripcion=descripcion,
                    nombreContacto=contacto,
                    urlContacto=url_contacto,
                    fotos=fotos,
                    appVAR=app)
                
            if agregacion:
                flash("Tu aviso de adopcion se registro exitosamente","exitoso")
                return redirect(url_for('index'))
            else:
                flash("ocurrió un error con el form y el servidor","error")    
                return redirect(url_for('index'))

        # en caso de que  haya fallado las validaciones
        else:
            if (validacionTotal and not fotosBool):
                print("fallo inputs e imagenes")
                validacionTotal = validacionTotal + validacionFotos  
                flash(validacionTotal, "errorBackendInputsFotos")
            elif not fotosBool:
                print("fallo imagenes")
                flash(validacionFotos, "errorBackendFotos")
            else:
                print("fallo en el input")
                flash(validacionTotal, "errorBackendInputs")

            regionesComunas = bd_ORM.getAllRegionesYComunasJSON()
            return render_template('auth/formulario.html', regionesYcomunas=regionesComunas,
            regionInput=region,
            comunaInput=comuna,
            sectorInput=sector,
            usernameInput=username,
            emailInput=email,
            celularInput=celular,
            contactoInput=contacto,
            url_contactoInput=url_contacto,
            animalInput=animal,
            cantidadInput=cantidad,
            edadInput=edad,
            meses_aniosInput=meses_anios,
            fechaInput=fecha,
            descripcionInput=descripcion)

if __name__ == "__main__":
    app.run(debug=True)

'''
    print("region: ")
    print(region)
    print("--------")
    print("")
        
    print("comuna: ")
    print(comuna)
    print("--------")
    print("")
        
    print("sector: ")
    print(sector)
    print("--------")
    print("")
        
    print("username: ")
    print(username)
    print("--------")
    print("")
        
    print("email: ")
    print(email)
    print("--------")
    print("")
        
    print("celular: ")
    print(celular)
    print("--------")
    print("")
        
    print("contacto: ")
    print(contacto)
    print("--------")
    print("")
        
    print("url_contacto: ")
    print(url_contacto)
    print("--------")
    print("")
        
    print("animal: ")
    print(animal)
    print("--------")
    print("")
        
    print("cantidad: ")
    print(cantidad)
    print("--------")
    print("")
        
    print("edad: ")
    print(edad)
    print("--------")
    print("")
        
    print("meses anios: ")
    print(meses_anios)
    print("--------")
    print("")
        
    print("fecha: ")
    print(fecha)
    print("--------")
    print("")
        
    print("descripcion: ")
    print(descripcion)
    print("--------")
    print("")
'''
