function put_cliente(){

    var request = new XMLHttpRequest();

    let id_cliente = window.location.search.substring(1);
    let nombre = document.getElementById("nombre");
    let email = document.getElementById("email");

    console.log('Id: ' + id_cliente);
    console.log('Nombre: ' + nombre.value);
    console.log('Email: ' + email.value);

    let payload = {
        "id_cliente": id_cliente, 
        "nombre": nombre.value ,
        "email": email.value
    }

    token = sessionStorage.getItem("token")

    request.open('PUT','https://8000-andreatellez-apirest-7qyzbm3hdnt.ws-us59.gitpod.io/clientes/' + id_cliente.value, true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("content-type", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + token);
    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;

        console.log("Response: " + response);
        console.log("JSON: " + json);
        console.log("Status: " + status);
        
    };
    request.send(JSON.stringify(payload));
};