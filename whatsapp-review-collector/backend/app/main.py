from fastapi import FastAPI, Request, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .db import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="WhatsApp Product Review Collector")

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Simple in-memory conversation tracking
conversations = {}  
# Structure: { "whatsapp:+1234" : {"step":1, "product": "", "name": ""} }

@app.post("/webhook")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    sender = form.get("From")
    message = (form.get("Body") or "").strip()

    if not sender:
        return PlainTextResponse("No sender found")

    # Get or init conversation state
    state = conversations.get(sender, {"step": 0})

    step = state["step"]

    # Step 0 → Ask product
    if step == 0:
        conversations[sender] = {"step": 1}
        return PlainTextResponse("Which product is this review for?")

    # Step 1 → User sends product name
    if step == 1:
        state["product"] = message
        state["step"] = 2
        conversations[sender] = state
        return PlainTextResponse("What's your name?")

    # Step 2 → User sends name
    if step == 2:
        state["name"] = message
        state["step"] = 3
        conversations[sender] = state
        return PlainTextResponse(f"Please send your review for {state['product']}.")

    # Step 3 → User sends actual review
    if step == 3:
        review_data = schemas.ReviewCreate(
            contact_number=sender,
            user_name=state["name"],
            product_name=state["product"],
            product_review=message
        )

        crud.create_review(db, review_data)

        # Clear conversation
        conversations.pop(sender, None)

        return PlainTextResponse(
            f"Thanks {state['na]()
