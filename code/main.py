from fastapi import FastAPI
import sqlite3
from typing import List 
from pydantic import BaseModel
import os
import hashlib 
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

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

DATABASE_URL = os.path.join("sql/usuarios.sqlite")

app=FastAPI()
security = HTTPBasic()

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
async def clientes(level: int = Depends(get_current_level)):
    if level==0:
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
async def id_clientes(id: int, level: int = Depends(get_current_level)):
    if level==0:
        with sqlite3.connect("code/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(int(id))) 
            response = cursor.fetchall()
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
    description="Metodo POST para insertar nuevos registros",) 
async def post_cliente(nombre:str,email:str,level: int = Depends(get_current_level)):
    if level==0:
        with sqlite3.connect("code/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("INSERT INTO clientes(nombre,email) VALUES ('{}','{}')".format(nombre,email))
            response = cursor.fetchone()
            message = {"mensaje" : "Cliente agregado"}
            return message
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.put("/clientes/{id_cliente}",response_model=Respuesta, summary="Metodo para actualizar un registro indicando el id",
    description="Metodo para actualizar un registro indicando el id",)
async def put_cliente(id_cliente:int,nombre:str,email:str,level: int = Depends(get_current_level)):
    if level==0:
        with sqlite3.connect("code/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("UPDATE clientes SET nombre = '{}', email = '{}' WHERE id_cliente={}".format(nombre,email,id_cliente))
            response = cursor.fetchone()
            message = {"mensaje" : "Cliente actualizado"}
            return message
    else:
          raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso",
            headers={"WWW-Authenticate": "Basic"},
        )
  
@app.delete("/clientes/{id_cliente}",response_model=Respuesta,summary="Metodo para eliminar un registro indicando el id",
    description="Metodo para eliminar un registro indicando el id",)
async def delete_cliente(id_cliente:int,level: int = Depends(get_current_level)):
    if level==0:
        with sqlite3.connect("code/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente={}".format(id_cliente))
            response = cursor.fetchone()
            message = {"mensaje" : "Cliente borrado"}
            return message
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso",
            headers={"WWW-Authenticate": "Basic"},
        ) 

   





