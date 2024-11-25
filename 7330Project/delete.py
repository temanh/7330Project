from db_connection import connect_to_database

def execute_query(query, data=None):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Operation successful!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def delete_degree():
    degree_id = int(input("Enter the degree ID to delete: "))
    query = """
        DELETE FROM Degrees
        WHERE DegreeID = %s
    """
    execute_query(query, (degree_id,))

def delete_course():
    course_number = input("Enter the course number to delete: ")
    query = """
        DELETE FROM Courses
        WHERE CourseNumber = %s
    """
    execute_query(query, (course_number,))