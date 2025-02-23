from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DepartmentBase(BaseModel):
    id: int
    department: str


class DepartmentCreate(DepartmentBase):

    pass


class DepartmentResponse(DepartmentBase):

    class Config:
        from_attributes = True


class JobBase(BaseModel):

    id: int
    job: str


class JobCreate(JobBase):

    pass


class JobResponse(JobBase):

    class Config:

        from_attributes = True


class EmployeeBase(BaseModel):
    name: str
    datetime: str
    department_id: int
    job_id: int


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):

    id: int
    department: Optional[DepartmentResponse]
    job: Optional[JobResponse]

    class Config:

        from_attributes = True
