from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI()

# -----------------------------
# In-Memory Database (Temporary)
# -----------------------------
todos_db = []

# -----------------------------
# Pydantic Models
# -----------------------------

class TodoCreate(BaseModel):
    title: str
    description: str
    completed: bool = False


class TodoUpdate(BaseModel):
    title: str
    description: str
    completed: bool


class StandardResponse(BaseModel):
    status: bool
    message: str
    data: dict | list | None = None


# =============================
# CREATE TODO
# =============================
@app.post("/todos", response_model=StandardResponse)
def create_todo(todo: TodoCreate):
    try:
        new_todo = {
            "id": str(uuid4()),
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed
        }

        todos_db.append(new_todo)

        return {
            "status": True,
            "message": "Todo created successfully",
            "data": new_todo
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================
# GET ALL TODOS
# =============================
@app.get("/todos", response_model=StandardResponse)
def get_all_todos():
    try:
        return {
            "status": True,
            "message": "Todos fetched successfully",
            "data": todos_db
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================
# GET TODO BY ID
# =============================
@app.get("/todos/{todo_id}", response_model=StandardResponse)
def get_todo_by_id(todo_id: str):
    try:
        for todo in todos_db:
            if todo["id"] == todo_id:
                return {
                    "status": True,
                    "message": "Todo found",
                    "data": todo
                }

        raise HTTPException(status_code=404, detail="Todo not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================
# UPDATE TODO BY ID
# =============================
@app.put("/todos/{todo_id}", response_model=StandardResponse)
def update_todo(todo_id: str, updated_data: TodoUpdate):
    try:
        for todo in todos_db:
            if todo["id"] == todo_id:
                todo["title"] = updated_data.title
                todo["description"] = updated_data.description
                todo["completed"] = updated_data.completed

                return {
                    "status": True,
                    "message": "Todo updated successfully",
                    "data": todo
                }

        raise HTTPException(status_code=404, detail="Todo not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================
# DELETE TODO BY ID
# =============================
@app.delete("/todos/{todo_id}", response_model=StandardResponse)
def delete_todo(todo_id: str):
    try:
        for index, todo in enumerate(todos_db):
            if todo["id"] == todo_id:
                deleted_todo = todos_db.pop(index)

                return {
                    "status": True,
                    "message": "Todo deleted successfully",
                    "data": deleted_todo
                }

        raise HTTPException(status_code=404, detail="Todo not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))