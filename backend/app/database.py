import os
import psycopg2
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definida")

DATABASE_URL_PG = DATABASE_URL.replace("postgresql+psycopg2", "postgresql")

conn = psycopg2.connect(DATABASE_URL_PG)
cursor = conn.cursor()
engine = create_engine(DATABASE_URL)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():

    drop_table_query = """
        DROP TABLE IF EXISTS departments;
    """

    create_table_query = """
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY,
        department TEXT
    );
    """

    cursor.execute("SET search_path TO public;")
    cursor.execute(drop_table_query)
    conn.commit()
    cursor.execute(create_table_query)
    conn.commit()

    cursor.execute("DELETE FROM departments")
    conn.commit()

    df = pd.read_csv("/Users/franciscolozano/Documents/Challenge/backend/app/data/departments.csv", sep=",", names=["id", "department"])
    df.to_sql("departments", con=engine, if_exists='append', index=False)
    conn.commit()

    drop_table_query = """
        DROP TABLE IF EXISTS jobs;
    """

    create_table_query = """
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY,
        job TEXT
    );
    """

    cursor.execute("SET search_path TO public;")
    cursor.execute(drop_table_query)
    conn.commit()
    cursor.execute(create_table_query)
    conn.commit()

    cursor.execute("DELETE FROM jobs")
    conn.commit()

    df = pd.read_csv("/Users/franciscolozano/Documents/Challenge/backend/app/data/jobs.csv", sep=",", names=["id", "job"])
    df.to_sql("jobs", con=engine, if_exists='append', index=False)
    conn.commit()

    drop_table_query = """
        DROP TABLE IF EXISTS employees;
    """

    create_table_query = """
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        datetime TEXT,
        department_id INTEGER,
        job_id INTEGER
    );
    """

    cursor.execute("SET search_path TO public;")
    cursor.execute(drop_table_query)
    conn.commit()
    cursor.execute(create_table_query)
    conn.commit()

    cursor.execute("DELETE FROM employees")
    conn.commit()

    df = pd.read_csv("/Users/franciscolozano/Documents/Challenge/backend/app/data/hired_employees.csv", sep=",", names=["id", "name", "datetime", "department_id", "job_id"])
    df.to_sql("employees", con=engine, if_exists='append', index=False)
    conn.commit()

def create_tables_sql():

    drop_table_query = """
        DROP TABLE IF EXISTS departments_sql;
    """

    create_table_query = """
    CREATE TABLE IF NOT EXISTS departments_sql (
        id INTEGER PRIMARY KEY,
        department TEXT
    );
    """

    cursor.execute("SET search_path TO public;")
    cursor.execute(drop_table_query)
    conn.commit()
    cursor.execute(create_table_query)
    conn.commit()

    cursor.execute("DELETE FROM departments_sql")
    conn.commit()

    df = pd.read_csv("/Users/franciscolozano/Documents/Challenge/backend/app/data/departments.csv", sep=",", names=["id", "department"])
    df.to_sql("departments_sql", con=engine, if_exists='append', index=False)
    conn.commit()

    drop_table_query = """
        DROP TABLE IF EXISTS jobs_sql;
    """

    create_table_query = """
    CREATE TABLE IF NOT EXISTS jobs_sql (
        id INTEGER PRIMARY KEY,
        job TEXT
    );
    """

    cursor.execute("SET search_path TO public;")
    cursor.execute(drop_table_query)
    conn.commit()
    cursor.execute(create_table_query)
    conn.commit()

    cursor.execute("DELETE FROM jobs_sql")
    conn.commit()

    df = pd.read_csv("/Users/franciscolozano/Documents/Challenge/backend/app/data/jobs.csv", sep=",", names=["id", "job"])
    df.to_sql("jobs_sql", con=engine, if_exists='append', index=False)
    conn.commit()

    drop_table_query = """
        DROP TABLE IF EXISTS employees_sql;
    """

    create_table_query = """
    CREATE TABLE IF NOT EXISTS employees_sql (
        id INTEGER PRIMARY KEY,
        name TEXT,
        datetime TEXT,
        department_id INTEGER,
        job_id INTEGER
    );
    """

    cursor.execute("SET search_path TO public;")
    cursor.execute(drop_table_query)
    conn.commit()
    cursor.execute(create_table_query)
    conn.commit()

    cursor.execute("DELETE FROM employees_sql")
    conn.commit()

    df = pd.read_csv("/Users/franciscolozano/Documents/Challenge/backend/app/data/hired_employees.csv", sep=",", names=["id", "name", "datetime", "department_id", "job_id"])
    df.to_sql("employees_sql", con=engine, if_exists='append', index=False)
    conn.commit()

create_tables_sql()
create_tables()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
