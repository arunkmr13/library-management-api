from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from database import get_database
from auth import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post("/borrow/{book_id}")
async def borrow_book(
    book_id: str,
    current_user: dict = Depends(get_current_user)
):

    db = get_database()

    user = await db["users"].find_one({"username": current_user["username"]})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user["_id"]

    book = await db["books"].find_one({"_id": ObjectId(book_id)})

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not book["available"]:
        raise HTTPException(status_code=400, detail="Book already borrowed")

    loan = {
        "book_id": ObjectId(book_id),
        "user_id": user_id,
        "borrow_date": datetime.utcnow(),
        "return_date": None
    }

    await db["loans"].insert_one(loan)

    await db["books"].update_one(
        {"_id": ObjectId(book_id)},
        {"$set": {"available": False}}
    )

    return {"message": "Book borrowed successfully"}


@router.put("/return/{loan_id}")
async def return_book(loan_id: str):

    db = get_database()

    loan = await db["loans"].find_one({"_id": ObjectId(loan_id)})

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan["return_date"] is not None:
        raise HTTPException(status_code=400, detail="Book already returned")

    await db["loans"].update_one(
        {"_id": ObjectId(loan_id)},
        {"$set": {"return_date": datetime.utcnow()}}
    )

    await db["books"].update_one(
        {"_id": ObjectId(loan["book_id"])},
        {"$set": {"available": True}}
    )

    return {"message": "Book returned successfully"}




@router.get("/")
async def get_loans(
    skip: int = 0,
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()

    # fetch full user from database
    user = await db["users"].find_one({"username": current_user["username"]})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user["role"] == "admin":
        cursor = db["loans"].find().skip(skip).limit(limit)
    else:
        cursor = db["loans"].find(
            {"user_id": user["_id"]}
        ).skip(skip).limit(limit)

    loans = []

    async for loan in cursor:
        loans.append({
            "loan_id": str(loan["_id"]),
            "book_id": str(loan["book_id"]),
            "user_id": str(loan["user_id"]),
            "borrow_date": loan["borrow_date"],
            "return_date": loan["return_date"]
        })

    return loans
