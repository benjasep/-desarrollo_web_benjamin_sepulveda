const mostrarDiv = (divFoto) =>{
    let divEspecial = document.getElementById('foto-adopcionActual');
    let fotoEspecial = divEspecial.querySelector("img");
    foto = divFoto.querySelector("img");
    fotoEspecial.src = foto.src;
    divEspecial.style.display = "block";
}

window.onload = () => {
    let divAllImg = document.getElementById('fotos-detalles-div').querySelectorAll('div');
    
    let divFoto = document.getElementById('foto-adopcionActual');
    let boton_cerrado = document.getElementById('close-foto');

    for(let i of divAllImg){
        i.addEventListener("click", () => {
        mostrarDiv(i);
    })
    }

    /*
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
    */

    boton_cerrado.addEventListener("click", () => {
        divFoto.style.display = "none";
    });
}