from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import get_database
from schemas import AuthorCreate

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/")
async def create_author(author: AuthorCreate):

    db = get_database()

    result = await db["authors"].insert_one(author.dict())

    return {"id": str(result.inserted_id)}


@router.get("/")
async def get_authors(skip: int = 0, limit: int = 10):

    db = get_database()

    authors = []

    async for author in db["authors"].find().skip(skip).limit(limit):
        author["_id"] = str(author["_id"])
        authors.append(author)

    return authors


@router.get("/{author_id}")
async def get_author(author_id: str):

    db = get_database()

    author = await db["authors"].find_one({"_id": ObjectId(author_id)})

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    author["_id"] = str(author["_id"])

    return author


@router.delete("/{author_id}")
async def delete_author(author_id: str):

    db = get_database()

    result = await db["authors"].delete_one({"_id": ObjectId(author_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Author not found")

    return {"message": "Author deleted"}


@router.put("/{author_id}")
async def update_author(author_id: str, author: AuthorCreate):
    db = get_database()

    result = await db["authors"].update_one(
        {"_id": ObjectId(author_id)},
        {"$set": {"name": author.name}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Author not found")

    return {"message": "Author updated successfully"}
