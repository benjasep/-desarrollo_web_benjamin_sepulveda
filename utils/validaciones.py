import re
import filetype
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from database import bd_ORM 

### validaciones de input ###

def validateRegion(region):
    validacion = bd_ORM.validacionRegion(region)
    return validacion

def validateComuna(region, comuna):
    validacion = bd_ORM.validacionRegionYComuna(region,comuna)
    return validacion
            
def validateSector(sector):
    validacion = True if len(sector) == 0 else len(sector) <=100
    return validacion

def validateName(name):
    validacion = len(name.strip()) >=3 and len(name.strip()) <=200 
    return validacion

def validateEmail(email):
    if (not email):
         return False
    largo = len(email) < 100
    regular = re.compile(r"^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$")
    valido = bool(regular.match(email))
    return largo and valido

def validatePhoneNumber(phoneNumber):
    if (not phoneNumber):
         return False
    largo = len(phoneNumber.strip()) >= 8 and len(phoneNumber.strip()) <= 15
    regular =  re.compile(r"^\+\d{3}\.\d{8}$")
    valido = bool(regular.match(phoneNumber.strip()))
    return largo and valido

def validateContacto(selectContacto, url):
    if (not selectContacto):
         return False
    largo = len(url) >= 4 and len(url) <= 50
    return largo 

def validateTypeAnimal(select):
    if (not select):
        return False 
    return select == "gato" or select == "perro"

def validateCantidad(cantidad):
    if not cantidad:
        return False
    
    booleano = float(cantidad) >=1 and float(cantidad) % 1 == 0 
    return booleano

def validateEdad(edad):
    if not edad:
        return False
    booleano = float(edad) >=1 and float(edad) % 1 == 0
    return booleano

def validateUnidadEdad(meses_anios):
    if not meses_anios:
        return False
    valido = meses_anios != "" and (meses_anios=="a" or meses_anios=="m")
    return valido
    
def validateDate(entregaDate):
    if not entregaDate:
        return False   
    inputDate = datetime.strptime(entregaDate, "%Y-%m-%dT%H:%M")
    defaultDate = datetime.now()
    diference = (inputDate.timestamp() - defaultDate.timestamp())/3600
    booleano = diference >=0
    return booleano

def validateDescription(descripcion):
    if descripcion == '':
        return True
        
    boolean = len(descripcion) <=500
    return len(descripcion) <=500



### validaciones de input ###

def validateAll(region, comuna, sector, name, email, phoneNumber,
    selectContacto, url, select, cantidad, edad, meses_anios,
    entregaDate, descripcion):
    
    mensajesError = []

    if not validateRegion(region):
        mensajesError.append("region")

    if not validateComuna(region, comuna):
        mensajesError.append("comuna")

    if not validateSector(sector):
        mensajesError.append("sector")
    
    if not validateName(name):
        mensajesError.append("sector")
        
    if not validateEmail(email):
        mensajesError.append("email")

    if not validatePhoneNumber(phoneNumber):
        mensajesError.append("numero telefonico")
        
    if not validateContacto(selectContacto, url):
        mensajesError.append("medio de contacto")
        
    if not validateTypeAnimal(select):
        mensajesError.append("tipo de animal")
        
    if not validateCantidad(cantidad):
        mensajesError.append("cantidad de animales")
    
    if not validateEdad(edad):
        mensajesError.append("edad de animales")
    
    if not validateUnidadEdad(meses_anios):
        mensajesError.append("meses o anios")
    
    if not validateDate(entregaDate):
        mensajesError.append("fecha de entrega")
    
    if not validateDescription(descripcion):
        mensajesError.append("descripcion")

    return mensajesError
    
    

