function login(idToken){

    let email = document.getElementById('email');
    let password = document.getElementById('password');


    let payload = {
        "username" : email.value,
        "password" : password.value
    }

    var request = new XMLHttpRequest();
    request.open("POST","https://8000-andreatellez-apirest-7qyzbm3hdnt.ws-us59.gitpod.io/user/token/",true);
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
            window.location.replace("clientes.html");
            sessionStorage.setItem("token", json.user);  
        }       
        else{
            alert(json.detail);
        }

    };
    request.send(JSON.stringify(payload));
};