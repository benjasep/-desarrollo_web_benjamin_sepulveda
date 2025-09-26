from flask import Flask, request, render_template, redirect, url_for, session, flash
from markupsafe import escape
from werkzeug.utils import secure_filename
from database import bd_ORM
from utils import validaciones
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
    avisos = []
    avisos = bd_ORM.getFirst5Avisos()
    for i in avisos:
        id_comuna = i[2]
        comuna = bd_ORM.getComunaById(id_comuna)
        i[2] = comuna  

    renderizado = render_template("auth/index.html", adopciones=avisos)
    return renderizado


@app.route('/listadoAdopciones/<int:page>')
def listadoAdopciones(page):
    #page = request.args.get(page, 1)
    #adopcionesAll = getAllAvisos()
    #adopcionesPage = (adopcionesAll[page*5:])[:5] # las primeras 5 de esa pagina

    return render_template("/auth/lista.html", avisos=[], actual=1)

'''
@app.route('/adopcion/<int:page>')
def listadoAdopciones(page):
    #page = request.args.get(page, 1)
    #adopcionesAll = getAllAvisos()
    #adopcionesPage = (adopcionesAll[page*5:])[:5] # las primeras 5 de esa pagina

    return render_template("/auth/lista.html")
'''

@app.route('/estadisticas')
def estadisticas():
    return render_template("auth/estadisticas.html")

@app.route('/formulario', methods=["GET", "POST"])
def formulario():
    if request.method == "GET": 
        regionesJSON = bd_ORM.getAllRegionesYComunasJSON()
        #print(regionesJSON[0])
        #comunas = bd_ORM.getAllComunas()
        return render_template("auth/formulario.html", regionesYcomunas = regionesJSON)

    elif request.method == "POST":
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #tiporeal = filetype.guess(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        def validateFoto(file):
            ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
            ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

            # check if a file was submitted
            if file is None:
                return False

            # check if the browser submitted an empty file
            if file.filename == "":
                return False
            
            # check file extension
            ftype_guess = filetype.guess(file)
            if ftype_guess.extension not in ALLOWED_EXTENSIONS:
                return False
            # check mimetype
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
        
        # inputs que si contienen fotos
        fotos = []
        for i in [foto1,foto2,foto3,foto4,foto5]:
            if i:
                fotos.append(i)
        # validacion de todo los inputs que no sean la foto

        validacionTotal = validaciones.validateAll(region, comuna, sector, username, email, celular,
        contacto, url_contacto, animal, cantidad, edad, meses_anios,
        fecha, descripcion)

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

        return "Datos recibidos correctamente", 200
        '''
        # validamos las validas

        validacionFotos = []

        if bool(foto1) or bool(foto2) or bool(foto3) or bool(foto4) or bool(foto5):            
            for j in fotos:
                if not validateFoto(j):
                    validacionFotos.append(j.filename)
        else:
            validacionFotos = ["no hay fotos"]

        if not validacionFotos and not validacionTotal:
            # agregamos el input a la bd


                #if validacionFotos(conf_text, conf_img):
                '''
                    # 1. generate random name for img
                    _filename = hashlib.sha256(
                        secure_filename(conf_img.filename) # nombre del archivo
                        .encode("utf-8") # encodear a bytes
                        ).hexdigest()
                    _extension = filetype.guess(conf_img).extension
                    img_filename = f"{_filename}.{_extension}"

                    # 2. save img as a file
                    conf_img.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))

                    # 3. save confession in db
                    user = db.get_user_by_username(username)
                    db.create_confession(conf_text, img_filename, user.id)
                    
                        
            #bd_ORM.addAviso(comuna,sector,username,email,celular,animal,cantidad,edad,meses_anios,fecha,descripcion
            #contacto,url_contacto,fotoadd)
            
            print("-----")
            print("DEBUG1")
            print("-----")
            '''
            addAviso(comuna=comuna,
                sector=sector,
                nombre=username,
                email=email,
                celular=celular,
                tipo=animal,
                cantidad=cantidad,
                edad=edad,
                unidad_medida=meses_anios,
                fecha_entrega=fecha,
                descripcion=descripcion,
                ## entidad contactar_por
                
                nombreContacto=contacto,
                urlContacto=url_contacto,
                fotos=validacionFotos)

            flash("Tu aviso de adopcion se registro exitosamente","exitoso")
            return redirect(url_for('index'))

        else:
            print("-----")
            print("DEBUG2")
            print("-----")

            print(validacionTotal)                                  
            if (validacionTotal and validacionFotos):
                print("fallo inputs e imagenes")
                validacionTotal = validacionTotal + validacionFotos  
                flash(validacionTotal, "errorBackendInputsFotos")
            elif validacionFotos:
                print("fallo imagenes")
                flash(validacionFotos, "errorBackendFotos")
            else:
                print("fallo en el input")
                flash("validacionTotal", "errorBackendInputs")

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
            descripcionInput=descripcion
            )

if __name__ == "__main__":
    app.run(debug=True)

