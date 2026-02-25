from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
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


# se crea una función para obtener una sesión de la base de datos. Esta función se usará como dependencia en las rutas para interactuar con la base de datos de manera segura y eficiente.
def get_db():
    db = SessionLocal() # Crea una nueva sesión de la base de datos
    try:
        yield db # Devuelve la sesión de la base de datos para que pueda ser utilizada en las rutas
    finally:
        db.close()


# =============================
# CREATE 
# =============================
@app.post("/employees", response_model=Employee_Public, status_code=status.HTTP_201_CREATED)
def create_employee(employee: Employee, db: Session = Depends(get_db)):

        # Verifica si ya existe un empleado con el mismo id_identification en la base de datos
        existing_employee = db.query(EmployeeDB).filter(EmployeeDB.id_identification == employee.id_identification).first()
        if existing_employee:
            raise HTTPException(status_code=400, detail="Employee with this ID already exists")

        # Crea un nuevo objeto EmployeeDB con los datos del empleado recibido en la solicitud
        db_employee = EmployeeDB(
            id_identification=employee.id_identification,
            full_name=employee.full_name,
            check_in=employee.check_in,
            check_out=employee.check_out
        )
        db.add(db_employee) # Agrega el nuevo empleado a la sesión de la base de datos
        db.commit() # Guarda los cambios a la base de datos
        db.refresh(db_employee) # Refresca el objeto db_employee con los datos de la base de datos (incluyendo el ID generado automáticamente)

        return db_employee 

# =============================
# READ ALL
# =============================
@app.get("/employees", response_model=List[Employee_Public])
def get_employees(db: Session = Depends(get_db)):
    
    return db.query(EmployeeDB).all() # devuelve todos los empleados de la DB

# =============================
# UPDATE
# =============================
@app.put("/employees/{employee_id}", response_model=Employee_Public)
def update_employee(employee_id: int, updated_employee: EmployeeUpdate, db: Session = Depends(get_db)):
        # Busca el empleado por su ID en la base de datos
        employee = db.query(EmployeeDB).filter(EmployeeDB.id_identification == employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        # Actualiza los campos del empleado con los datos proporcionados en el cuerpo de la solicitud
        employee.full_name = updated_employee.full_name 
        employee.check_in = updated_employee.check_in
        employee.check_out = updated_employee.check_out

        db.commit()
        db.refresh(employee)
        return employee
    
# =============================
# DELETE
# =============================
@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
        # Busca el empleado por su ID en la base de datos
        employee = db.query(EmployeeDB).filter(EmployeeDB.id_identification == employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        db.delete(employee)
        db.commit()