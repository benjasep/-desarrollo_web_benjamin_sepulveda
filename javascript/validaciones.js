const validateRegion = (region) => {
    return region !=='';
};

const validateComuna = (comuna) =>{
    return comuna !=='';
};

const validateSector = (sector) =>{
    if (sector.length === 0) return true;
    return sector.length <=100;
};

const validateName = (name) => {
  if(!name) return false;
  let lengthValid = name.trim().length >= 3 && name.trim().length <= 200;
  return lengthValid;
};

const validateEmail = (email) => {
  if (!email) return false;
  let lengthValid = email.length < 100;
  let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
  let formatValid = re.test(email);
  return lengthValid && formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
  if (!phoneNumber) return false;
  let lengthValid = phoneNumber.trim().length >= 8;
  let re = /^\+\d{3}\.\d{8}$/;
  let formatValid = re.test(phoneNumber.trim());
  return lengthValid && formatValid;
};

const validateContact = (selectContacto, url) => {
    if (selectContacto === '') return false;
    let lengthValid = url.length >=4 && url.length <=50;
    return lengthValid;
};

const validateTypeAnimal = (selectPerro, selectGato) =>{
    let select = selectPerro.checked || selectGato.checked;
    return select;
};

const validateCantidad = (cantidad) =>{
    let minValid = cantidad >= 1;
    return minValid;
};

const validateEdad = (edad) => {
    let minValid = edad >= 1;
    return minValid;
};

const validateUnidadEdad = (meses, anios) => {
return meses.checked || anios.checked;
};

const validateDate = (entregaDate) =>{
    let input = new Date(entregaDate.value);
    let defaultDate = new Date("2025-09-02T08:00:00");
    let diference =  (input.getTime() - defaultDate.getTime())/3600000;
    return diference <=3 && diference >=0;
};

const validateDescription = (descripcion) =>{
    /*
    let countCols = descripcion.split("\n").length;
    let countRows = descripcion.split(" ").length + 1;
    return countCols <=10 && countRows <=50;
    */
   return descripcion.length <=500; // total de 10x50 caracteres
};

const validateFoto = (fotos) =>{
  if (fotos.value === '') return true;
  let typeValid = true;
  let fotoFamily = fotos.type.split("/")[0];
  typeValid &&= fotoFamily == "image" || fotos.type == "application/pdf" || fotos.type == "file";
  return typeValid;
  }

const validateAllfotos = (foto1, foto2, foto3, foto4, foto5) =>{  
  let valid1 = foto1.value !== '' && validateFoto(foto1);
  let valid2 = validateFoto(foto2);
  let valid3 = validateFoto(foto3);
  let valid4 = validateFoto(foto4);
  let valid5 = validateFoto(foto5);
  return valid1 && valid2 && valid3 && valid4 && valid5;
};


const validateSelect = (select) => {
  if(!select) return false;
  return true;
};

const validateForm = () => {
    let myForm = document.forms["login-form"];
    let region = document.getElementById('region');
    let comuna = document.getElementById('comuna');
    let sector = document.getElementById('sector');
    let name = document.getElementById('username');
    let mail = document.getElementById('email');
    let celular = document.getElementById('celular');
    let contactoOption = document.getElementById('contacto');
    let url = document.getElementById('url-contacto');
    let tipoPerro = document.getElementById('perro');
    let tipoGato = document.getElementById('gato');
    let cantidad = document.getElementById('cantidad');
    let edad = document.getElementById('edad');
    let unidadMeses = document.getElementById('meses');
    let unidadAnios = document.getElementById('anios');
    let entregaDate = document.getElementById('fecha');
    let description = document.getElementById('descripcion');
    let foto1 = document.getElementById('foto1');
    let foto2 = document.getElementById('foto2');    
    let foto3 = document.getElementById('foto3');    
    let foto4 = document.getElementById('foto4');
    let foto5 = document.getElementById('foto5');

  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  if (!validateRegion(region.value)) {
    setInvalidInput("Region");
  };

  if (!validateComuna(comuna.value)) {
    setInvalidInput("Comuna");
  };

  if (!validateSector(sector.value)) {
    setInvalidInput("Sector");
  };

  if (!validateName(name.value)) {
    setInvalidInput("Nombre");
  };

  if (!validateEmail(mail.value)) {
    setInvalidInput("Email");
  };

  if (!validatePhoneNumber(celular.value)) {
    setInvalidInput("Número telefonico");
  };

  if (!validateContact(contactoOption.value, url.value)) {
    setInvalidInput("medio de contacto");
  };

  if (!validateTypeAnimal(tipoPerro , tipoGato)) {
    setInvalidInput("tipo de animal");
  };

  if (!validateCantidad(cantidad.value)) {
    setInvalidInput("cantidad de animales");
  };

  if (!validateEdad(edad.value)) {
    setInvalidInput("edad de animal(es)");
  };

  if (!validateUnidadEdad(unidadMeses, unidadAnios)) {
    setInvalidInput("unidad de edad");
  };

  if (!validateDate(entregaDate)) {
    setInvalidInput("fecha de entrega");
  };

  if (!validateDescription(description.value)) {
    setInvalidInput("descripcion");
  };
  
  if (!validateAllfotos(foto1, foto2, foto3, foto4, foto5)) {
    setInvalidInput("fotos");
  };

  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");
  let formContainer = document.querySelector(".main-container");

  if (!isValid) {
    validationListElem.textContent = "";
    for (let input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    };
    validationMessageElem.innerText = "Los siguientes campos son inválidos:";

    validationBox.style.backgroundColor = "#ffdddd";
    validationBox.style.borderLeftColor = "#f44336";

    validationBox.hidden = false;
  } else {
    myForm.style.display = "none";

    validationMessageElem.innerText = "¡Formulario válido! ¿Deseas enviarlo o volver?";
    validationListElem.textContent = "";

    validationBox.style.backgroundColor = "#ddffdd";
    validationBox.style.borderLeftColor = "#4CAF50";

    let submitButton = document.createElement("button");
    submitButton.innerText = "Enviar";
    submitButton.style.marginRight = "10px";
    submitButton.addEventListener("click", () => {
      window.location.href = "./portada.html";
      alert("Hemos recibido la informacion de adopcion, muchas gracias y suerte");
    });

    let backButton = document.createElement("button");
    backButton.innerText = "Volver al formulario";
    backButton.addEventListener("click", () => {
      myForm.style.display = "block";
      validationBox.hidden = true;
    });
    validationListElem.appendChild(submitButton);
    validationListElem.appendChild(backButton);
    validationBox.hidden = false;
  };
};


let submitBtn = document.getElementById("envio");
submitBtn.addEventListener("click", validateForm);
