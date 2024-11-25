from db_connection import connect_to_database

def execute_query(query, data=None, fetch=False):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        if fetch:
            return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Get all degrees
def get_all_degrees():
    query = "SELECT * FROM Degrees"
    results = execute_query(query, fetch=True)
    print("Degrees:")
    for row in results:
        print(row)

# Get all courses
def get_all_courses():
    query = "SELECT * FROM Courses"
    results = execute_query(query, fetch=True)
    print("Courses:")
    for row in results:
        print(row)

# Get a single degree by DegreeID
def get_degree_by_id():
    degree_id = int(input("Enter the Degree ID to query: "))
    query = "SELECT * FROM Degrees WHERE DegreeID = %s"
    results = execute_query(query, (degree_id,), fetch=True)
    if results:
        print("Degree Details:")
        for row in results:
            print(row)
    else:
        print("No degree found with the given ID.")

# Get a single course by CourseNumber
def get_course_by_number():
    course_number = input("Enter the Course Number to query: ")
    query = "SELECT * FROM Courses WHERE CourseNumber = %s"
    results = execute_query(query, (course_number,), fetch=True)
    if results:
        print("Course Details:")
        for row in results:
            print(row)
    else:
        print("No course found with the given number.")