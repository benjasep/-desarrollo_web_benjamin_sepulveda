let divFoto = document.getElementById('foto-adopcionActual');

let divFoto1 = document.getElementById('foto-adopcion1');
let divFoto2 = document.getElementById('foto-adopcion2');
let divFoto3 = document.getElementById('foto-adopcion3');
let divFoto4 = document.getElementById('foto-adopcion4');

const mostrarDiv = (divFoto) =>{
    let divEspecial = document.getElementById('foto-adopcionActual');
    let fotoEspecial = divEspecial.querySelector("img");
    foto = divFoto.querySelector("img");
    fotoEspecial.src = foto.src;
    divEspecial.style.display = "block";
}

window.onload = () => {
    let divFoto1 = document.getElementById('foto-adopcion1');
    let divFoto2 = document.getElementById('foto-adopcion2');
    let divFoto3 = document.getElementById('foto-adopcion3');
    let divFoto4 = document.getElementById('foto-adopcion4');
    let divFoto = document.getElementById('foto-adopcionActual');
    let boton_cerrado = document.getElementById('close-foto');

    divFoto1.addEventListener("click", () => {
        mostrarDiv(divFoto1);
    })
    
    divFoto2.addEventListener("click", () => {
        mostrarDiv(divFoto2);
    })
    
    divFoto3.addEventListener("click", () => {
        mostrarDiv(divFoto3);
    })

    divFoto4.addEventListener("click", () => {
        mostrarDiv(divFoto4);
    })

    boton_cerrado.addEventListener("click", () => {
        divFoto.style.display = "none";
    });
}