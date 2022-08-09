function crear_usuario(){

    let email = document.getElementById('email');
    let password = document.getElementById('password');

    console.log('Correo: ' + email.value);
    console.log('Contraseña: ' + password.value);

    let payload = {
        "username" : email.value,
        "password" : password.value,
    }
    var request = new XMLHttpRequest();
    request.open("POST","https://8000-andreatellez-apirest-7qyzbm3hdnt.ws-us54.gitpod.io/user/",true);
    request.setRequestHeader('Accept', 'application/json');
    request.setRequestHeader('Content-Type', 'application/json');

    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;

        console.log("Response: " + response);
        console.log("JSON: " + json);
        console.log("Status: " + status);

        if (status == 202){
            alert("Usuario creado exitosamente");
            window.location.replace("index.html");
        }
        else{
            alert(json.detail);
        }

    };
    request.send(JSON.stringify(payload));
};