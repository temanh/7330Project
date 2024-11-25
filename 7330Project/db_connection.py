import mysql.connector

# Database connection setup
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",  
        user="root",       
        password="12345678",  
        database="school"  
    )
