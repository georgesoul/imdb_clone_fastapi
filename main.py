from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

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
async def root():
    cursor.execute(""" SELECT * FROM products; """)
    products = cursor.fetchall()
    # return {"message": "Hello world!"}
    return products