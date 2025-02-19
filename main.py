from fastapi import FastAPI, HTTPException
import mysql.connector
import csv
import os
from fastapi import  Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request


# Set up Jinja2 for templates
templates = Jinja2Templates(directory="templates")
app = FastAPI()

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Benak@2010",
    "database": "employee_db"
}

CSV_FILE = "employees.csv"

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def load_csv_to_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if not os.path.exists(CSV_FILE):
        print("⚠️ CSV file not found, skipping import.")
        return
    
    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            cursor.execute(
                """
                INSERT IGNORE INTO employees (first_name, last_name, email, age, contact_number, dob)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                row
            )

    conn.commit()
    cursor.close()
    conn.close()
    print(" CSV data loaded into MySQL.")


def save_db_to_csv():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT first_name, last_name, email, age, contact_number, dob FROM employees")
    employees = cursor.fetchall()

    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["First", "Last", "Email", "Age", "ContactNumber", "DOB"])
        writer.writerows(employees)

    cursor.close()
    conn.close()
    print(" MySQL data saved to CSV.")


load_csv_to_db()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    cursor.close()
    connection.close()

    return templates.TemplateResponse("index.html", {"request": request, "employees": employees})


@app.get("/employees/")
def get_all_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()

    if not employees:
        return {"message": "No employees found"}

    return employees


@app.post("/employees/")
def add_employee(first_name: str, last_name: str, email: str, age: int, contact_number: str, dob: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO employees (first_name, last_name, email, age, contact_number, dob)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (first_name, last_name, email, age, contact_number, dob)
        )
        conn.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Database Error: {str(err)}")
    finally:
        cursor.close()
        conn.close()

    save_db_to_csv()  
    return {"message": "Employee added successfully"}


@app.put("/employees/{email}")
def update_employee(email: str, first_name: str = None, last_name: str = None, age: int = None, contact_number: str = None, dob: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()

    update_fields = []
    params = []
    if first_name:
        update_fields.append("first_name = %s")
        params.append(first_name)
    if last_name:
        update_fields.append("last_name = %s")
        params.append(last_name)
    if age:
        update_fields.append("age = %s")
        params.append(age)
    if contact_number:
        update_fields.append("contact_number = %s")
        params.append(contact_number)
    if dob:
        update_fields.append("dob = %s")
        params.append(dob)

    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    update_query = f"UPDATE employees SET {', '.join(update_fields)} WHERE email = %s"
    params.append(email)

    cursor.execute(update_query, tuple(params))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    cursor.close()
    conn.close()

    save_db_to_csv() 
    return {"message": "Employee updated successfully"}


@app.delete("/employees/{email}")
def delete_employee(email: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM employees WHERE email = %s", (email,))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    cursor.close()
    conn.close()

    save_db_to_csv() 
    return {"message": "Employee deleted successfully"}
