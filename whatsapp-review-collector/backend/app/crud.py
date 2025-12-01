from sqlalchemy.orm import Session
from . import models, schemas

def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.Review(
        contact_number=review.contact_number,
        user_name=review.user_name,
        product_name=review.product_name,
        product_review=review.product_review,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_reviews(db: Session):
    return db.query(models.Review).order_by(models.Review.created_at.desc()).all()
