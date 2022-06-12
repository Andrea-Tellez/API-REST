from fastapi import FastAPI
import sqlite3
from typing import List 
from pydantic import BaseModel

class Respuesta(BaseModel):
    message: str

app=FastAPI()

@app.get("/", response_model=Respuesta)
async def index():
    return{"message": "API REST"}

@app.get("/clientes/")
async def clientes():
    with sqlite3.connect("sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes") 
        response = cursor.fetchall()
        return response 

@app.get("/clientes/{id}")
async def clientes(id):
    with sqlite3.connect("sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(int(id))) 
        response = cursor.fetchall()
        return response