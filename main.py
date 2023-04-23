from fastapi import FastAPI
from fastapi.params import Body
import psycopg2
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    

while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='root123!', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)
        

@app.get('/')
def root():
    return {"message": "It works!"}


@app.get('/posts')
async def get_posts():
    cursor.execute(""" SELECT * FROM products; """)
    posts = cursor.fetchall()
    return posts