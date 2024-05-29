from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_book():
    response = client.post(
        "/books",
        json={
            "title": "Test Book",
            "author": "Author",
            "published_date": "2023-01-01T00:00:00",
            "isbn": "1234567890"
        },
        headers={"Authorization": "Bearer admin-token"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"


def test_update_book():
    # First create a book to update
    response = client.post(
        "/books",
        json={
            "title": "Another Test Book",
            "author": "Author",
            "published_date": "2023-01-01T00:00:00",
            "isbn": "1234567890"
        },
        headers={"Authorization": "Bearer admin-token"}
    )
    book_id = response.json()["_id"]

    # Then update the book
    response = client.put(
        f"/books/{book_id}",
        json={"title": "Updated Book", "author": "Updated Author", "published_date": "2023-01-01T00:00:00",
              "isbn": "0987654321"},
        headers={"Authorization": "Bearer admin-token"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Book"


def test_delete_book():
    # First create a book to delete
    response = client.post(
        "/books",
        json={
            "title": "Book to Delete",
            "author": "Author",
            "published_date": "2023-01-01T00:00:00",
            "isbn": "1234567890"
        },
        headers={"Authorization": "Bearer admin-token"}
    )
    book_id = response.json()["_id"]

    # Then delete the book
    response = client.delete(
        f"/books/{book_id}",
        headers={"Authorization": "Bearer admin-token"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"
