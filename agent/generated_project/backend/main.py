from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import base64

from database.db import SessionLocal, Base, engine
from database.models import Image

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# GET IMAGES
# =========================
@app.get("/images")
def get_images(db: Session = Depends(get_db)):
    images = db.query(Image).all()

    return [
        {
            "id": img.id,
            "filename": img.filename,
            "content": img.content
        }
        for img in images
    ]

# =========================
# UPLOAD IMAGE
# =========================
@app.post("/upload")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()

        if not content:
            return {"error": "empty file"}

        encoded = base64.b64encode(content).decode("utf-8")

        new_img = Image(
            filename=file.filename,
            content=encoded
        )

        db.add(new_img)
        db.commit()
        db.refresh(new_img)

        print("✅ SAVED:", new_img.id)

        return {"message": "uploaded", "id": new_img.id}

    except Exception as e:
        print("❌ ERROR:", str(e))
        db.rollback()
        return {"error": str(e)}

# =========================
# DELETE IMAGE
# =========================
@app.delete("/image/{id}")
def delete_image(id: int, db: Session = Depends(get_db)):
    img = db.query(Image).filter(Image.id == id).first()

    if not img:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(img)
    db.commit()

    return {"message": "deleted"}

print("MAIN FILE LOADED")