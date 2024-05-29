from fastapi import FastAPI, HTTPException, Depends
from typing import List
from app.models import Book
from app.auth import authenticate_user, create_access_token, get_current_admin_user
from app.crud import fetch_all_books, fetch_book_by_id, add_book, update_book, delete_book
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

app = FastAPI()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": "$2b$12$W5nT.L5Yc2ytphl2jkNf2udpr3ZjJmZPVjQ4JiaJ/XuqzgQhHl0Iu", # "adminpassword"
        "disabled": False,
        "role": "admin"
    }
}
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/books", response_model=List[Book])
async def get_books():
    return await fetch_all_books()

@app.get("/books/{id}", response_model=Book)
async def get_book(id: str):
    book = await fetch_book_by_id(id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=Book)
async def create_book(book: Book, user: dict = Depends(get_current_admin_user)):
    if user:
        return await add_book(book.dict(by_alias=True))

@app.put("/books/{id}", response_model=Book)
async def update_book(id: str, book: Book, user: dict = Depends(get_current_admin_user)):
    if user:
        updated_book = await update_book(id, book.dict(by_alias=True))
        if updated_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return updated_book

@app.delete("/books/{id}", response_model=dict)
async def delete_book(id: str, user: dict = Depends(get_current_admin_user)):
    if user:
        deleted_count = await delete_book(id)
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": "Book deleted successfully"}
