from fastapi import FastAPI
import sqlite3
from typing import List 
from pydantic import BaseModel
import os
import hashlib 
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import pyrebase

class Respuesta(BaseModel):
    message: str

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

class ClienteIN(BaseModel):
    nombre:str
    email:str

class Usuarios(BaseModel):
    username: str
    level: int

class Usuario(BaseModel):
    username: str
    password: str


DATABASE_URL = os.path.join("sql/usuarios.sqlite")

app=FastAPI()
security = HTTPBasic()
securityBearer = HTTPBearer()

origins = {
    "https://8000-andreatellez-apirest-7qyzbm3hdnt.ws-us53.gitpod.io/",
    "https://8080-andreatellez-apirest-7qyzbm3hdnt.ws-us53.gitpod.io/"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

firebaseConfig = {
  'apiKey': "AIzaSyAxqxiXiSyRhp1JSPHWp0ZmigR0KuTW7cs",
  'authDomain': "fastapi-c5f98.firebaseapp.com",
  'databaseURL': "https://fastapi-c5f98-default-rtdb.firebaseio.com",
  'projectId': "fastapi-c5f98",
  'storageBucket': "fastapi-c5f98.appspot.com",
  'messagingSenderId': "373126825537",
  'appId': "1:373126825537:web:dbc0af6a34fdb9540ee8c0"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

def get_current_level(credentials: HTTPBasicCredentials = Depends(security)):
    password_b = hashlib.md5(credentials.password.encode())
    password = password_b.hexdigest()
    with sqlite3.connect(DATABASE_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level FROM usuarios WHERE username = ? and password = ?",
            (credentials.username, password),
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    return user[0]


@app.get("/", response_model=Respuesta)
async def index():
    return{"message": "API REST"}

@app.get("/clientes/",  status_code=status.HTTP_202_ACCEPTED,
    summary="Metodo para ver todos los clientes de la base de datos",
    description="Metodo para ver todos los clientes de la base de datos",
)
async def clientes(credentials:HTTPAuthorizationCredentials = Depends(securityBearer)):
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    level = db.child("users").child(uid).child("Nivel").get().val()
    if level==1:
         with sqlite3.connect("sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes") 
            response = cursor.fetchall()
            return response 
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso",
            headers={"WWW-Authenticate": "Basic"},
        )

   
@app.get("/clientes/{id}",status_code=status.HTTP_202_ACCEPTED,
    summary="Metodo para regresar a un cliente indicado  por el ID",
    description="Metodo para regresar a un cliente indicado  por el ID", )
async def id_clientes(id: int, credentials:HTTPAuthorizationCredentials = Depends(securityBearer)):
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    level = db.child("users").child(uid).child("Nivel").get().val()
    if level==1:
        with sqlite3.connect("sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(int(id))) 
            response = cursor.fetchone()
            return response
    else:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso",
            headers={"WWW-Authenticate": "Basic"},
        )

"""segunda parte"""

@app.post("/clientes/",response_model=Respuesta, status_code=status.HTTP_202_ACCEPTED,
    summary="Metodo POST para insertar nuevos registros",
    description="Metodo POST para insertar nuevos registros",
) 
async def post_cliente(cliente:ClienteIN, credentials:HTTPAuthorizationCredentials = Depends(securityBearer)):
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    level = db.child("users").child(uid).child("Nivel").get().val()
    if level==1:
        with sqlite3.connect("sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("INSERT INTO clientes(nombre,email) VALUES ('{}','{}')".format(cliente.nombre,cliente.email))
            response = cursor.fetchone()
            message = {"message" : "Cliente agregado"}
            return message
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.put("/clientes/{id_cliente}",response_model=Respuesta, summary="Metodo para actualizar un registro indicando el id",
    description="Metodo para actualizar un registro indicando el id",)
async def put_cliente(cliente:Cliente,credentials:HTTPAuthorizationCredentials = Depends(securityBearer)):
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    level = db.child("users").child(uid).child("Nivel").get().val()
    if level==1:
        with sqlite3.connect("sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("UPDATE clientes SET nombre = '{}', email = '{}' WHERE id_cliente={}".format(cliente.nombre,cliente.email,cliente.id_cliente))
            response = cursor.fetchone()
            message = {"message" : "Cliente actualizado"}
            return message
    else:
          raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso",
            headers={"WWW-Authenticate": "Basic"},
        )
  
@app.delete("/clientes/{id_cliente}",response_model=Respuesta,summary="Metodo para eliminar un registro indicando el id",
    description="Metodo para eliminar un registro indicando el id",)
async def delete_cliente(id_cliente:int,credentials:HTTPAuthorizationCredentials = Depends(securityBearer)):
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    level = db.child("users").child(uid).child("Nivel").get().val()
    if level==1:
        with sqlite3.connect("sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente={}".format(id_cliente))
            response = cursor.fetchone()
            message = {"message" : "Cliente borrado"}
            return message
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso",
            headers={"WWW-Authenticate": "Basic"},
        ) 

   
"""firebase"""

@app.get(
    "/user/validate/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get a token for a user",
    description="Get a token for a user",
    tags=["auth"]
)
def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        email = credentials.username
        password = credentials.password
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email,password)
        response = {
            "token" : user['idToken']
        }
        return response

    except Exception as error:
        print(f"ERROR: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get(
    "/user/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get a user",
    description="Get a user",
    tags=["auth"]
)
async def get_user(credentials:HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']

        db = firebase.database()
        user_data = db.child("users").child(uid).get().val()

        response = {
            "user_data" : user_data
        }
        return response
        
    except Exception as error:
        print(f"ERROR: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.post(
    "/user/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Agrega un nuevo usuario",
    description="Agrega un nuevo usuario",
    tags=["Agregar"]
)
def agregar_usuario(usuario:Usuario):
    correos = usuario.username
    passwords = usuario.password
    auth = firebase.auth()
    db = firebase.database()

    try:
	   
        user = auth.create_user_with_email_and_password(correos, passwords)
        Token = user["idToken"]
        Informacion = auth.get_account_info(Token)
        uid = Informacion["users"][0]["localId"]
        email = Informacion["users"][0]["email"]
        info = {"email" : email, "Nivel" : 1}
        user_data = db.child("users").child(uid).set(info)
        response = {"userdata": user}
        return response

    except Exception as error:
        print(f"Error : {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.post(
    "/user/token/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Metodo de inicio de sesion",
    description="Metodo de inicio de sesion",
    tags=["Iniciar_sesion"],
)
async def inicio_sesion(usuario:Usuario):
    correos = usuario.username
    passwords = usuario.password
    auth = firebase.auth()
   
    try:
    	
        user = auth.sign_in_with_email_and_password(correos, passwords)
        Tokenuser = user["idToken"]
        response = {f"user": Tokenuser}
        return response

    except Exception as error:
        print(f"Error : {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)