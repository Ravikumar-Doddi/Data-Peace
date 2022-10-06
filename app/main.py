from ast import While
from sqlite3 import Cursor
from turtle import pos
from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    id : int
    first_name : str
    last_name  : str
    company_name : str
    city : str
    state : str
    zip : int
    email : str
    web : str
    age : int

while True:
    try:
        connection = psycopg2.connect(host = "localhost",database = "fastapi" ,user = "postgres",password= "Navy7284@#",cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connected successfully")
        break

    except Exception as error:
        print("Database connection failed")
        print("Error was :", error )
        time.sleep(2)


my_posts = [{
    "id": 1,
    "first_name": "James",
    "last_name": "Butt",
    "company_name": "Benton, John B Jr",
    "city": "New Orleans",
    "state": "LA",
    "zip": 70116,
    "email": "jbutt@gmail.com",
    "web": "http://www.bentonjohnbjr.com",
    "age": 70
  },
  {
    "id": 2,
    "first_name": "Josephine",
    "last_name": "Darakjy",
    "company_name": "Chanay, Jeffrey A Esq",
    "city": "Brighton",
    "state": "MI",
    "zip": 48116,
    "email": "josephine_darakjy@darakjy.org",
    "web": "http://www.chanayjeffreyaesq.com",
    "age": 48
  },
  {
    "id": 3,
    "first_name": "Art",
    "last_name": "Venere",
    "company_name": "Chemel, James L Cpa",
    "city": "Bridgeport",
    "state": "NJ",
    "zip": 80514,
    "email": "art@venere.org",
    "web": "http://www.chemeljameslcpa.com",
    "age": 80
  },
  {
    "id": 4,
    "first_name": "Lenna",
    "last_name": "Paprocki",
    "company_name": "Feltz Printing Service",
    "city": "Anchorage",
    "state": "AK",
    "zip": 99501,
    "email": "lpaprocki@hotmail.com",
    "web": "http://www.feltzprintingservice.com",
    "age": 99
  }]

def find_post(id):
    for i in my_posts:
        if i["id"] == id:
            return i 

def find_index(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i 

@app.get("/users")
def get_posts():
    cursor.execute("""SELECT * FROM "Details" LIMIT  5 """)
    posts = cursor.fetchall()
    return{"data" : posts}

@app.post("/users",status_code=status.HTTP_201_CREATED)
def create_post(new_post : Post):
    cursor.execute("""INSERT INTO  "Details" (register_id,first_name,last_name,company_name,city,
    current_state,zip,email,
    web,age) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING * """,(new_post.id,new_post.first_name,new_post.last_name,new_post.company_name,
    new_post.city,new_post.state,new_post.zip,new_post.email,new_post.web,new_post.age)) 
    
    new_one = cursor.fetchone()
    connection.commit()
    return{"newpost" : new_one}


@app.get("/users/{id}")
def get_post(id : int):
    cursor.execute(""" SELECT * FROM "Details" WHERE register_id = {0} """.format(str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} notfound")
    return {"post" : post}
    
@app.delete("/users/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cursor.execute(""" DELETE FROM "Details" WHERE register_id = {0} RETURNING *""".format(str(id)))
    deleted_post = cursor.fetchone()
    connection.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with id : {id} does not exist")

    return {"message" : "your post successfully deleted"}

@app.put("/users/{id}")
def update_post(id : int,post : Post):
    cursor.execute(""" UPDATE "Details" SET register_id = {0},first_name = {1},last_name = {2},company_name = {3},
    city = {4},current_state = {5},zip = {6},email = {7},web = {8},age = {9} RETURNING *""".format(
    post.id,post.first_name,post.last_name,post.company_name,post.city,post.state,post.zip,post.email,post.web,post.age))
    updated_post = cursor.fetchone()
    connection.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with id : {id} does not exist")
    
    return {"data" : updated_post}
