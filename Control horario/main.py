from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List
from model import Employee, Employee_Public, EmployeeUpdate
from create_database import SessionLocal, Base, engine
from models_db import EmployeeDB


app = FastAPI()

# =============================
# CORS
# =============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# Static files
# =============================
app.mount("/static", StaticFiles(directory="static"), name="static")


Base.metadata.create_all(bind=engine) # Crea las tablas en la base de datos si no existen

# =============================
# GET index.html
# =============================
@app.get("/")
def read_index():
    return FileResponse("static/index.html")


# =============================
# CREATE
# =============================
@app.post("/employees", response_model=Employee_Public, status_code=status.HTTP_201_CREATED)
def create_employee(employee: Employee):

    db = SessionLocal()
    try:
        db_employee = EmployeeDB(
            id_identification=employee.id_identification,
            full_name=employee.full_name,
            check_in=employee.check_in,
            check_out=employee.check_out
        )
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


# =============================
# READ ALL
# =============================
@app.get("/employees", response_model=List[Employee_Public])
def get_employees():
    db = SessionLocal()
    try:
        employees = db.query(EmployeeDB).all()
        return employees
    finally:
        db.close()


# =============================
# UPDATE
# =============================
@app.put("/employees/{employee_id}", response_model=Employee_Public)
def update_employee(employee_id: int, updated_employee: EmployeeUpdate):

    db = SessionLocal()
    try:
        employee = db.query(EmployeeDB).filter(EmployeeDB.id_identification == employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        employee.full_name = updated_employee.full_name
        employee.check_in = updated_employee.check_in
        employee.check_out = updated_employee.check_out

        db.commit()
        db.refresh(employee)
        return employee
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


# =============================
# DELETE
# =============================
@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int):
    db = SessionLocal()
    try:
        employee = db.query(EmployeeDB).filter(EmployeeDB.id_identification == employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        db.delete(employee)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()