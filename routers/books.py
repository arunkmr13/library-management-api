from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from database import get_database
from schemas import BookCreate, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/")
async def create_book(book: BookCreate):

    db = get_database()

    # verify author exists
    author = await db["authors"].find_one({"_id": ObjectId(book.author_id)})
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    new_book = {
        "title": book.title,
        "author_id": ObjectId(book.author_id),
        "available": True
    }

    result = await db["books"].insert_one(new_book)

    return {"id": str(result.inserted_id)}


@router.get("/")
async def get_books(
    skip: int = 0,
    limit: int = 10,
    author_id: str | None = Query(None)
):

    db = get_database()

    query = {}

    if author_id:
        query["author_id"] = ObjectId(author_id)

    books = []

    async for book in db["books"].find(query).skip(skip).limit(limit):

        book["_id"] = str(book["_id"])
        book["author_id"] = str(book["author_id"])

        books.append(book)

    return books


@router.get("/{book_id}")
async def get_book(book_id: str):

    db = get_database()

    book = await db["books"].find_one({"_id": ObjectId(book_id)})

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book["_id"] = str(book["_id"])
    book["author_id"] = str(book["author_id"])

    return book


@router.delete("/{book_id}")
async def delete_book(book_id: str):

    db = get_database()

    result = await db["books"].delete_one({"_id": ObjectId(book_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")

    return {"message": "Book deleted"}



@router.put("/{book_id}")
async def update_book(book_id: str, book: BookUpdate):
    existing_book = await db["books"].find_one({"_id": ObjectId(book_id)})

    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = {k: v for k, v in book.dict().items() if v is not None}

    if "author_id" in update_data:
        author = await db["authors"].find_one({"_id": ObjectId(update_data["author_id"])})
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        update_data["author_id"] = ObjectId(update_data["author_id"])

    await db["books"].update_one(
        {"_id": ObjectId(book_id)},
        {"$set": update_data}
    )

    return {"message": "Book updated successfully"}


