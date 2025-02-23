from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
import pandas as pd
import numpy as np
from sqlalchemy import MetaData, Table, select, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoSuchTableError
from app.database import get_db
from app import crud

router = APIRouter()

TABLE_COLUMNS = {
    "departments": ["id", "department"],
    "jobs": ["id", "job"],
    "employees": ["id", "name", "datetime", "department_id", "job_id"]
}

VALID_TABLES = {
    "departments": crud.insert_departments,
    "jobs": crud.insert_jobs,
    "employees": crud.insert_employees
}

@router.post("/api/load/{table_name}")
async def upload_csv(
    table_name: str, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    

    if table_name not in VALID_TABLES:

        raise HTTPException(status_code=400, detail="Invalid table name")

    try:

        columns = TABLE_COLUMNS[table_name]
        df = pd.read_csv(file.file, header=None, names=columns)
        if df.shape[0] > 1000:
        
            raise HTTPException(
                status_code=400,
                detail=f"Error: The csv file has more than 1000 rows",
            )

        else:

            df = df.replace(np.nan, None)
            data = df.to_dict(orient="records")
            VALID_TABLES[table_name](db, data)

        return {"message": f"{len(df)} records inserted into {table_name}"}

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"Could not load the information for table '{table_name}'. Error: {str(e)}",
        )

metadata = MetaData()

ALLOWED_TABLES = ["departments", "jobs", "employees"]

@router.get("/api/view")
async def get_table(
    table_name: str = Query(..., description="Name of the table to query"),
    db: Session = Depends(get_db)
):

    if table_name not in ALLOWED_TABLES:
        raise HTTPException(status_code=400, detail="Invalid table name")
    
    metadata = MetaData()
    try:
        table = Table(table_name, metadata, autoload_with=db.bind)
    except NoSuchTableError:
        raise HTTPException(status_code=404, detail="Table not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading table: {e}")
    
    query = select(table)

    try:
        result = db.execute(query)
        rows = [dict(row._mapping.items()) for row in result]
        return {"table": table_name, "data": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing query: {e}")
    
@router.delete("/api/delete")
async def delete_table(
    table_name: str = Query(..., description="Name of the table to delete rows from"),
    db: Session = Depends(get_db)
):
    if table_name not in ALLOWED_TABLES:
        raise HTTPException(status_code=400, detail="Invalid table name")
    
    metadata = MetaData()

    try:
        table = Table(table_name, metadata, autoload_with=db.bind)
    except NoSuchTableError:
        raise HTTPException(status_code=404, detail="Table not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading table: {e}")
    
    try:
        delete_stmt = table.delete()
        result = db.execute(delete_stmt)
        db.commit()

        rows_deleted = result.rowcount

        return {
            "table": table_name,
            "rows_deleted": rows_deleted,
            "message": "All rows deleted successfully"
        }

    except Exception as e:
        db.rollback()  # Revertir cambios si hay error
        raise HTTPException(status_code=500, detail=f"Error executing delete: {e}")
    
@router.get("/api/query/{query}")
async def get_table(
    query: str,
    db: Session = Depends(get_db)
):
    if query == "handleFirstQuery":

        sql_query = """
            with temporal_employees_sql as (
                select
                    a.*,
                    datetime::timestamptz::date as date_employees
                from employees_sql as a
                where extract(year from datetime::timestamptz::date) = 2021
            ), temporal_cruce as ( 
                select
                    a.*,
                    b.department,
                    c.job
                from temporal_employees_sql as a
                left join departments_sql as b
                on (a.department_id = b.id)
                left join jobs as c
                on (a.job_id = c.id)
            )
            select
                department,
                job,
                sum(case when extract(quarter from date_employees) = 1 then 1 else 0 end) as q1,
                sum(case when extract(quarter from date_employees) = 2 then 1 else 0 end) as q2,
                sum(case when extract(quarter from date_employees) = 3 then 1 else 0 end) as q3,
                sum(case when extract(quarter from date_employees) = 4 then 1 else 0 end) as q4
            from temporal_cruce
            group by department, job
            order by department, job
        """

    elif query == "handleSecondQuery":

        sql_query = """
             with temporal_employees_sql as (
                select
                    a.*,
                    datetime::timestamptz::date as date_employees
                from employees_sql as a
                where extract(year from datetime::timestamptz::date) = 2021
            ), cantidad_contrataciones_por_departamento as (
                select
                    department_id,
                    count(*) as quantity
                from temporal_employees_sql
                group by department_id
            ), promedio_contrataciones as (
                select
                    avg(quantity) as avg_quantity
                from cantidad_contrataciones_por_departamento
            )
            select
                a.department_id as id,
                b.department,
                a.quantity as hired
            from cantidad_contrataciones_por_departamento as a
            left join departments_sql as b
            on (a.department_id = b.id)
            where a.quantity > (select avg_quantity from promedio_contrataciones)
            order by quantity desc
        """

    try:
        result = db.execute(text(sql_query))
        rows = result.fetchall()
        columns = result.keys()

        data = [dict(zip(columns, row)) for row in rows]
        print(data)
        return data

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))