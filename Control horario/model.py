from pydantic import BaseModel
from datetime import time, datetime, timedelta
from pydantic import model_validator, field_validator


class EmployeeUpdate(BaseModel):
    full_name: str
    check_in: time
    check_out: time


class EmployeeDelete(BaseModel):
    full_name: str
    check_in: time
    check_out: time

class Employee_Public(BaseModel):
    full_name: str
    check_in: time
    check_out: time 


# Este modelo valida automáticamente los datos
# que vienen desde el frontend
class Employee(BaseModel):
    id_identification: int
    full_name: str
    check_in: time
    check_out: time 


    @model_validator(mode="after")
    def validate_hours(self):
        if self.check_out <= self.check_in: # Si la hora de salida es menor o igual a la hora de entrada, lanza un error
            raise ValueError("check_out must be later than check_in")
        return self
    

    @field_validator("full_name")
    @classmethod
    def validate_full_name_not_empty(cls, value):
        if not value.strip():
            raise ValueError("full_name cannot be empty")
        return value

    
    @field_validator("id_identification")
    @classmethod
    def validate_length_identification(cls, value):
        if len(str(value)) > 6:
            raise ValueError("id_identification must be at most 6 digits long")
        return value
    

    @field_validator("check_in")
    @classmethod
    def validate_check_cannot_be_before_7am(cls, value):
        if value < time(7, 0):
            raise ValueError("check_in cannot be before 7:00 AM")
        return value

    
    @field_validator("full_name")
    @classmethod
    def validate_full_name_length(cls, value):
        if len(value) > 20:
            raise ValueError("full_name must be at most 20 characters long")
        return value
     
    
    
    @model_validator(mode="after") # valida los campos luego de que se hayan validado individualmente
    def validate_hours_range(self):
        # Combina la fecha de hoy con las horas de check_in y check_out para calcular la duración
        start = datetime.combine(datetime.today(), self.check_in)
        end = datetime.combine(datetime.today(), self.check_out)

        # Si la duración es mayor a 8 horas, lanza un error
        if end - start > timedelta(hours=8):
            raise ValueError("Working hours cannot exceed 8 hours")
        
        return self