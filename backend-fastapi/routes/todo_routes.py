from fastapi import APIRouter, Depends, HTTPException
from database import todo_collection
from models import TodoCreate, TodoUpdate, StandardResponse
from auth import get_current_user
from bson import ObjectId

router = APIRouter()

# -----------------------
# CREATE TODO (Auth Required)
# -----------------------
@router.post("/todos", response_model=StandardResponse)
def create_todo(todo: TodoCreate, current_user=Depends(get_current_user)):
    try:
        new_todo = {
            "title": todo.title,
            "description": todo.description,
            "user_id": str(current_user["_id"])
        }

        result = todo_collection.insert_one(new_todo)

        new_todo["_id"] = str(result.inserted_id)

        return {
            "status": True,
            "message": "Todo created successfully",
            "data": new_todo
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------
# GET ALL USER TODOS
# -----------------------
@router.get("/todos", response_model=StandardResponse)
def get_my_todos(current_user=Depends(get_current_user)):
    try:
        todos = list(todo_collection.find({"user_id": str(current_user["_id"])}))

        for todo in todos:
            todo["_id"] = str(todo["_id"])

        return {
            "status": True,
            "message": "User todos fetched",
            "data": todos
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------
# GET TODO BY ID
# -----------------------
@router.get("/todos/{todo_id}", response_model=StandardResponse)
def get_todo_by_id(todo_id: str, current_user=Depends(get_current_user)):
    try:
        todo = todo_collection.find_one({"_id": ObjectId(todo_id), "user_id": str(current_user["_id"])})
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        todo["_id"] = str(todo["_id"])
        return {
            "status": True,
            "message": "Todo fetched successfully",
            "data": todo
        }
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------
# UPDATE TODO BY ID
# -----------------------
@router.put("/todos/{todo_id}", response_model=StandardResponse)
def update_todo(todo_id: str, todo_update: TodoUpdate, current_user=Depends(get_current_user)):
    try:
        update_data = {k: v for k, v in todo_update.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        result = todo_collection.update_one(
            {"_id": ObjectId(todo_id), "user_id": str(current_user["_id"])},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Todo not found")

        updated_todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        updated_todo["_id"] = str(updated_todo["_id"])

        return {
            "status": True,
            "message": "Todo updated successfully",
            "data": updated_todo
        }
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------
# DELETE TODO BY ID
# -----------------------
@router.delete("/todos/{todo_id}", response_model=StandardResponse)
def delete_todo(todo_id: str, current_user=Depends(get_current_user)):
    try:
        result = todo_collection.delete_one({"_id": ObjectId(todo_id), "user_id": str(current_user["_id"])})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Todo not found")

        return {
            "status": True,
            "message": "Todo deleted successfully",
            "data": None
        }
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))