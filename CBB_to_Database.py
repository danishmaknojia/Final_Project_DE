import pandas as pd
import sqlite3

# Load the CSV file into a Pandas DataFrame
cbb = pd.read_csv("../Final_Project_DE/archive/cbb.csv")

# Connect to SQLite database (or create one if it doesn't exist)
conn = sqlite3.connect("cbb_data.db")

# Write the DataFrame to a SQL table
table_name = "cbb_data_complete"
cbb.to_sql(table_name, conn, if_exists="replace", index=False)

# Confirm the operation
print(f"Data successfully written to the SQLite database in table: {table_name}")

# Close the connection
conn.close()
