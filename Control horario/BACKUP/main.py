from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List

from model import Employee, Employee_Public, EmployeeUpdate


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


# =============================
# Base de datos en memoria
# =============================
employees: List[Employee] = [
    Employee(
        id_identification=102026,
        full_name="Carlos Mendes",
        check_in="08:00:00",
        check_out="16:00:00"
    ),
    Employee(
        id_identification=202026,
        full_name="Ana Ribeiro",
        check_in="09:00:00",
        check_out="17:00:00"
    ),
    Employee(
        id_identification=302026,
        full_name="Marcos Silva",
        check_in="07:30:00",
        check_out="15:30:00"
    )
]


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

    # Verificar que no exista un ID repetido
    for existing_employee in employees:
        if existing_employee.id_identification == employee.id_identification:
            raise HTTPException(
                status_code=400,
                detail="Employee with this ID already exists"
            )

    employees.append(employee)
    return employee


# =============================
# READ ALL
# =============================
@app.get("/employees", response_model=List[Employee_Public])
def get_employees():
    return employees


# =============================
# UPDATE
# =============================
@app.put("/employees/{employee_id}", response_model=Employee_Public)
def update_employee(employee_id: int, updated_employee: EmployeeUpdate):

    for employee in employees:
        if employee.id_identification == employee_id:
            employee.full_name = updated_employee.full_name
            employee.check_in = updated_employee.check_in
            employee.check_out = updated_employee.check_out
            return employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )


# =============================
# DELETE
# =============================
@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int):

    for index, employee in enumerate(employees):
        if employee.id_identification == employee_id:
            employees.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )