import pandas as pd
import pyodbc

print("Starting ETL with SQL")

# Read CSV
df = pd.read_csv("data/employees.csv")

# Clean data
df = df.drop_duplicates()
df = df.dropna()
df["Name"] = df["Name"].str.upper()

# Connect to SQL Server
conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=localhost;"
    "DATABASE=EmployeeDB;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

# Load into SQL (Employee_Stage)
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO Employee_Stage (EmployeeID, Name, Department, Salary)
        VALUES (?, ?, ?, ?)
    """, row.EmployeeID, row.Name, row.Department, row.Salary)

conn.commit()

print("Data loaded into SQL successfully")