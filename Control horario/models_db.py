from sqlalchemy import Column, Integer, String, Time
from create_database import Base

class EmployeeDB(Base):
    __tablename__ = "employees"

    id_identification = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    check_in = Column(Time, nullable=False)
    check_out = Column(Time, nullable=False)