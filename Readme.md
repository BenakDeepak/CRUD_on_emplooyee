The **MySQL password** must be updated in the `main.py` file.  

### **Database Setup:**
Create a database named **`employee_db`** by running:  
```sql
CREATE DATABASE employee_db;
```

### **Table Creation:**
Ensure the `employees` table exists by executing the following SQL command:  
```sql
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INT NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    dob DATE NOT NULL
);
```
### **run the requiremnts.txt file:**
Start  with:  
```bash
pip install -r requirements.txt
```
### **Run the API Server:**
Start the FastAPI server with:  
```bash
uvicorn main:app --reload
```

### **API Documentation:**
Access all API endpoints at:  
[http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)
