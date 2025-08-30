
const regionOption = () =>{
    let regionSelect = document.getElementById("region");
    region_comuna.regiones.forEach(R =>{
        let newRegion = document.createElement("option");
        newRegion.innerText = R.nombre;
        newRegion.value = R.numero;
        regionSelect.appendChild(newRegion)
    }
);
}

const crearOptionRedes = (contactoArray,selectOption) => {
    for (let i of contactoArray){
        let newRed = document.createElement('option');
        newRed.value = i;
        newRed.innerText = i;
        selectOption.appendChild(newRed);
    }
} //

const updateComunas = () => {
  let regionSelect = document.getElementById("region");
  let comunaSelect = document.getElementById("comuna");
  let selectedRegion = regionSelect.value -1;
  comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';
  if (region_comuna.regiones[selectedRegion]) {
      region_comuna.regiones[selectedRegion].comunas.forEach(regionSelected => {
          let option = document.createElement("option");
          option.value = regionSelected.id;
          option.text = regionSelected.nombre;
          comunaSelect.appendChild(option);
      });
  }
};

const updateContactoText = () =>{
    let inputText = document.getElementById('url-contacto');
    let contactSelect = document.getElementById('contacto');
    const reasonLabel = document.querySelector("label[for='url-contacto']");
    if (contactSelect.value !== ""){
        inputText.style.display = "block";
        reasonLabel.style.display = "block";
    } else {
        inputText.style.display = "none";
        reasonLabel.style.display = "none";
        
    }
};


const updateFoto1 = () =>{
    let foto2 = document.getElementById("lifoto2")
    foto2.style.display = "block";
}

const updateFoto2 = () =>{
    let foto3 = document.getElementById("lifoto3")
    foto3.style.display = "block";
}

const updateFoto3 = () =>{
    let foto4 = document.getElementById("lifoto4")
    foto4.style.display = "block";
}

const updateFoto4 = () =>{
    let foto5 = document.getElementById("lifoto5")
    foto5.style.display = "block";
}

const contactos = ['whatsapp', 'instagram', 'telegram', 'tiktok', 'X', 'otra']

window.onload = () => {

    let selectContacto = document.getElementById('contacto');
    crearOptionRedes(contactos, selectContacto);

    let selectRegion = document.getElementById('region');
    regionOption(selectRegion);

    selectRegion.addEventListener("change",() =>{
        updateComunas();
    })
    
    selectContacto.addEventListener("change", () =>{
        updateContactoText();
    }
    )
    selectFoto1 = document.getElementById('foto1').addEventListener("change", () =>{
        selectFoto1 = document.getElementById('foto1')
        if (selectFoto1.value !== '') updateFoto1();
    })

    
    selectFoto2 = document.getElementById('foto2').addEventListener("change", () =>{
        selectFoto2 = document.getElementById('foto2')
        if (selectFoto2.value !== '') updateFoto2();
    })

    
    selectFoto3 = document.getElementById('foto3').addEventListener("change", () =>{
        selectFoto3 = document.getElementById('foto3')
        if (selectFoto3.value !== '') updateFoto3();
    })

    
    selectFoto4 = document.getElementById('foto4').addEventListener("change", () =>{
        selectFoto4 = document.getElementById('foto4')
        if (selectFoto4.value !== '') updateFoto4();
    })


}
