import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'toor',
)

cr = db.cursor()

cr.execute("Create Database if not exists crm_db")

print("All Done!")
