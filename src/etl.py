import pandas as pd
import pyodbc

print("Starting ETL")

# 1. Extract
df = pd.read_csv("data/employees.csv")

# 2. Transform
df = df.drop_duplicates()
df["Name"] = df["Name"].str.upper()

# 3. Connect to SQL Server (THIS is the missing link)
conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=localhost;"
    "DATABASE=EmployeeDB;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

# 4. Load into SQL (THIS is the real connection)
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO Employee_Stage (EmployeeID, Name, Department, Salary)
        VALUES (?, ?, ?, ?)
    """, row.EmployeeID, row.Name, row.Department, row.Salary)

conn.commit()

print("Data successfully loaded into SQL Server")