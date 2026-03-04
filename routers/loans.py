from fastapi import APIRouter, HTTPException
from datetime import datetime
from database import get_database

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post("/borrow/{book_id}")
async def borrow_book(book_id:str, user_id:str):

    db = get_database()

    book = await db["books"].find_one({"_id":ObjectId(book_id)})

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not book["available"]:
        raise HTTPException(status_code=400, detail="Book already borrowed")

    loan = {
        "book_id": book_id,
        "user_id": user_id,
        "borrow_date": datetime.utcnow(),
        "return_date": None
    }

    result = await db["loans"].insert_one(loan)

    await db["books"].update_one(
        {"_id":ObjectId(book_id)},
        {"$set":{"available":False}}
    )

    return {"loan_id":str(result.inserted_id)}


from bson import ObjectId

@router.put("/return/{loan_id}")
async def return_book(loan_id: str):

    db = get_database()

    loan = await db["loans"].find_one({"_id": ObjectId(loan_id)})

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan.get("returned"):
        raise HTTPException(status_code=400, detail="Book already returned")

    await db["loans"].update_one(
        {"_id": ObjectId(loan_id)},
        {"$set": {"returned": True}}
    )

    return {"message": "Book returned successfully"}


from bson import ObjectId
from fastapi import Query

@router.get("/loans/")
async def list_loans(user_id: str = Query(None)):

    db = get_database()

    query = {}

    if user_id:
        query["user_id"] = ObjectId(user_id)

    loans = []

    async for loan in db["loans"].find(query):

        loans.append({
            "loan_id": str(loan["_id"]),
            "book_id": str(loan["book_id"]),
            "user_id": str(loan["user_id"]),
            "returned": loan.get("returned", False)
        })

    return loans


