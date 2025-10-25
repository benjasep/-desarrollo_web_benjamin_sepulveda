const postComment = () => {  

    
    const validateName = (name) => {
        return name.length >= 3 && name.length <= 80;
    }

    const validateComentario = (comentario) => {
        return comentario.length >= 10 && comentario.length <= 500;
    }


    let name = document.getElementById("nombre").value;
    let comentario = document.getElementById("comentario").value;

    let errores = [];

    if (!validateName(name)) {
        errores.push("Nombre inválido");
    }

    if (!validateComentario(comentario)) {
        errores.push("Comentario inválido");
    }

    if (errores.length === 0) {
    let req = fetch(`${window.origin}/comments`, {  
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nombre: name, comentario: comentario, avisoId: currentAvisoId })  
    })
    .then(response => response.json())
    .then(data => {
        getComments();  
    })
    .catch(error => {
        let error = document.getElementById("error-form-comentario");
        error.textContent = "Error al enviar comentario.";
        console.error('Error al enviar comentario:', error);
    });
} else {
    let errorList = document.getElementById("error-list");
    errorList.innerHTML = "";  
    errores.forEach(error => {
        let li = document.createElement("li");
        li.textContent = error;
        errorList.appendChild(li);
    });
}}

const getComments = () => { 
    let req = fetch(`${window.origin}/comments`)  
        .then(response => response.json())
        .then(data => {
            let commentsList = document.getElementById("comments-list");
            let divComment = document.getElementById("hilo-comments");
            commentsList.innerHTML = "";  

            if (data.length === 0) {
                let noCommentsMsg = document.createElement("p");
                noCommentsMsg.textContent = "No hay comentarios aún.";
                divComment.appendChild(noCommentsMsg);
                return;
            } else {
                data.forEach(comment => {
                    let li = document.createElement("li");
                    li.textContent = comment;
                    commentsList.appendChild(li);
                });
            }
        })
        .catch(error => {
            let error = document.getElementById("error-form-comentario");
            error.textContent = "Error al cargar los comentarios.";
            console.error('Error fetching comments:', error);
        });
}