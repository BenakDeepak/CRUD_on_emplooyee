password must be changed in the main.py of the Mysql database 

create a database named employee_db;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INT NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    dob DATE NOT NULL
);

run the command below:
uvicorn main:app --reload

in http://127.0.0.1:8000/docs/ we can find the all the api 
