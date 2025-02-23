from sqlalchemy.orm import Session
from app import models

def insert_departments(db: Session, data: list[dict]):
    db.bulk_insert_mappings(models.Department, data)
    db.commit()

def insert_jobs(db: Session, data: list[dict]):
    db.bulk_insert_mappings(models.Job, data)
    db.commit()

def insert_employees(db: Session, data: list[dict]):
    db.bulk_insert_mappings(models.Employee, data)
    db.commit()
