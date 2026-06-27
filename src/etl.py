import pyodbc

print("Starting Stage → Final Load")

conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=localhost\SQLEXPRESS;"
    "DATABASE=EmployeeDB;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

# 1. READ from staging table
cursor.execute("SELECT * FROM Employee_Stage")
rows = cursor.fetchall()

print(f"Rows fetched from stage: {len(rows)}")

# 2. CLEAN + LOAD into FINAL table
for row in rows:
    employee_id = row.EmployeeID
    name = row.Name.strip().upper()
    department = row.Department.strip().upper()
    salary = row.Salary

    if salary is None or salary <= 0:
        continue

    cursor.execute("""
        MERGE Employees AS target
        USING (SELECT ? AS EmployeeID, ? AS Name, ? AS Department, ? AS Salary) AS source
        ON target.EmployeeID = source.EmployeeID

        WHEN MATCHED THEN
            UPDATE SET
                Name = source.Name,
                Department = source.Department,
                Salary = source.Salary

        WHEN NOT MATCHED THEN
            INSERT (EmployeeID, Name, Department, Salary)
            VALUES (source.EmployeeID, source.Name, source.Department, source.Salary);
    """,
    employee_id, name, department, salary)

conn.commit()

print("Stage → Final load completed successfully")