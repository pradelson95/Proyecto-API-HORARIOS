from locust import HttpUser, task, between
import random
from datetime import time


class EmployeeUser(HttpUser):

    wait_time = between(1, 2)  # tiempo entre requests

    @task(2)
    def get_employees(self):
        self.client.get("/employees")

    @task(1)
    def create_employee(self):

        # Hora de entrada entre 7:00 y 10:00
        check_in_hour = random.randint(7, 10)
        check_in = f"{check_in_hour:02d}:00"

        # Salida entre 1 y 8 horas después (nunca más de 8)
        duration = random.randint(1, 8)
        check_out_hour = check_in_hour + duration
        check_out = f"{check_out_hour:02d}:00"

        payload = {
            "id_identification": random.randint(100000, 999999),  # siempre 6 dígitos
            "full_name": f"User{random.randint(1,999)}",  # menos de 20 caracteres
            "check_in": check_in,
            "check_out": check_out
        }

        self.client.post("/employees", json=payload)