from fastapi import APIRouter, HTTPException
from database import user_collection
from models import UserSignup, UserLogin, StandardResponse
from auth import hash_password, verify_password, create_access_token

router = APIRouter()

# -----------------------
# SIGNUP
# -----------------------
@router.post("/signup", response_model=StandardResponse)
def signup(user: UserSignup):
    try:
        existing = user_collection.find_one({"email": user.email})
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

        new_user = {
            "email": user.email,
            "password": hash_password(user.password)
        }

        result = user_collection.insert_one(new_user)

        return {
            "status": True,
            "message": "User registered successfully",
            "data": {"user_id": str(result.inserted_id)}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------
# LOGIN
# -----------------------
@router.post("/login", response_model=StandardResponse)
def login(user: UserLogin):
    try:
        db_user = user_collection.find_one({"email": user.email})
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid email")

        if not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=400, detail="Invalid password")

        token = create_access_token({"id": str(db_user["_id"])})

        return {
            "status": True,
            "message": "Login successful",
            "data": {"access_token": token}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))