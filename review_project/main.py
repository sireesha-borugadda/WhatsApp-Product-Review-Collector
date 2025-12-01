from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from datetime import datetime

app = FastAPI()

# PostgreSQL Connection
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="assignment_db",
        user="postgres",
        password="YOUR_PASSWORD",  # <-- Put your PostgreSQL password here
        port=5432
    )

# Request Body (Review data)
class Review(BaseModel):
    customer_name: str
    phone_number: str
    product_name: str
    product_review: str
    rating: int

# HOME API
@app.get("/")
def home():
    return {"message": "FastAPI Working!"}

# POST API → Add a new review
@app.post("/add-review")
def add_review(data: Review):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reviews (customer_name, phone_number, product_name, product_review, rating, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data.customer_name,
        data.phone_number,
        data.product_name,
        data.product_review,
        data.rating,
        datetime.now()
    ))

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Review saved successfully!"}

# GET API → Fetch all reviews
@app.get("/get-reviews")
def get_reviews():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM reviews")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {"reviews": rows}
