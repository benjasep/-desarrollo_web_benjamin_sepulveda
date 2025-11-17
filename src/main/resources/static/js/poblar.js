
async function getData(){
    const url = "http://localhost:8080/avisos/all";
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
        const obj = await response.json();
        const table = document.getElementById('tablaAvisos');
        if (obj.length > 0){
            const myElement = document.getElementById('listaAvisos');
            myElement.style.display = "block";
            table.innerHTML = "";
        }
        let filas = "<tr class='fila-aviso'>\n" +
            "    <td><b>ID</b></td>\n" +
            "    <td><b>Fecha publicación</b></td>\n" +
            "    <td><b>Sector</b></td>\n" +
            "    <td><b>Cantidad Tipo Edad</b></td>\n" +
            "    <td><b>Comuna</b></td>\n" +
            "    <td><b>Nota</b></td>\n" +
            "    <td><b>Evaluar</b></td>\n" +
            "  </tr>";
            
        for (let i = 0; i < obj.length; i++) {
            let timeSplit = obj[i].fecha.split("T");
            let nota = obj[i].average === 0 ? "-" : obj[i].average.toFixed(1);

            filas = filas + "<tr><td>"+obj[i].id+"</td>\n"+
                "<td>"+timeSplit[0]+" "+timeSplit[1]+"</td>\n"+
                "<td>"+obj[i].sector+"</td>\n"+
                "<td>"+obj[i].cantidad+" "+obj[i].tipo+" "+obj[i].edad+" "+obj[i].unidad_medida+"</td>\n"+
                "<td>"+obj[i].comuna+"</td>\n"+
                "<td>"+nota+"</td>\n"+
                '<td><div id="div-'+obj[i].id+'"><button onclick="postFunction('+obj[i].id+')">Evaluar</button></div></td></tr>';
        }
        table.innerHTML = filas;
    } catch (error) {
        console.error(error.message);
    }
}

const validation = (nota) => {
    const validInt = (nota % 1 == 0) ? true : false; 
    return nota >=1 && nota <=7 && validInt;
}

const postFunction = (id) => {
    let divForm = document.getElementById("div-"+id);
    divForm.innerHTML = '<form class="form-nota" id="form-nota-'+id+'" onsubmit="mandarForm(event, '+id+')">\n' +
            'Nota: <input id="notaNueva-'+id+'" type="number" name="notaNueva" min="1" max="7" required /><br />\n' +
            '<input id="idAviso-'+id+'" type="hidden" name="idAviso" value="'+id+'" /><br />\n' +
            '<button type="submit">Mandar Nota</button>\n' +
            '</form>';
}

function mandarForm(event, id) {
    event.preventDefault();
    const nota = document.getElementById('notaNueva-'+id).value;
    const avisoId = document.getElementById('idAviso-'+id).value;
    addNota(avisoId, nota);
}

async function addNota(id, nota){
    let mensaje = document.getElementById('mensaje');
    mensaje.style.display = "none";
    let error = document.getElementById('error');
    error.style.display = "none";

    if (validation(parseFloat(nota)) && id){
        try {
            const response = await fetch("http://localhost:8080/notas/add", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({ nota: nota, aviso_id: id })
            });
            const data = response.json();
            if (!response.ok) {
                error.innerHTML = "<p>"+data.body.error+".</p>";
                error.style.display = "block";
                setTimeOut(() => {
                    error.innerHTML = "";
                    error.style.display = "none";
                },3000)
                throw new Error(`POST Response status: ${response.status}`);
            }
            
            const form = document.getElementById("div-"+id);
            form.innerHTML = "";  
            
            mensaje.innerHTML = "<p>Nota agregada exitosamente :D</p>";
            mensaje.style.display = "block";
            getData();
            setTimeout(() => {
            mensaje.innerHTML = "";
            mensaje.style.display = "none";
            }, 3000);
        } catch(error) {
            console.error(error);
        }
    } else {
        error.innerHTML = "<p>Por favor selecciona un valor válido de nota (número entero).</p>";
        error.style.display = "block";
        setTimeOut(() => {
            error.innerHTML = "";
            error.style.display = "none";
        },4000)
    }
}
