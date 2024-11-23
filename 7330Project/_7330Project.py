import mysql.connector
from mysql.connector import Error

# Show the main menu
def show_menu():
    print("\nProgram Evaluation System")
    print("1. Enter Degree Information")
    print("2. Enter Course Information")
    print("3. Enter Section Information")
    print("4. Enter Evaluation Information")
    print("5. Query Data")
    print("6. Exit")
    choice = input("Enter choice: ")
    return choice

# Function to collect degree information from the user
def enter_degree():
    name = input("Enter degree name: ")
    level = input("Enter degree level (e.g., BA, BS, MS): ")
    description = input("Enter degree description: ")  # Added description input
    insert_degree(name, level, description)

# Query data menu
def query_data():
    print("\nQuery Options:")
    print("1. List Courses for a Degree")
    print("2. List Sections for a Course")
    print("3. List Sections for an Instructor")
    print("4. List Evaluations for a Semester")
    choice = input("Enter choice: ")
    if choice == '1':
        degree_name = input("Enter degree name: ")
        list_courses_for_degree(degree_name)
    elif choice == '2':
        course_name = input("Enter course name: ")
        list_sections_for_course(course_name)
    else:
        print("Option not implemented yet.")

# Database connection
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='user1',
            password='123',
            database='ProgramEvaluation'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Insert degree information into the database
def insert_degree(name, level, description):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO Degrees (Name, Level, Description) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, level, description))
            connection.commit()
            print("Degree inserted successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# List courses for a degree (placeholder)
def list_courses_for_degree(degree_name):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT name FROM Course WHERE degree_name = %s"
            cursor.execute(query, (degree_name,))
            results = cursor.fetchall()
            if results:
                print(f"Courses for {degree_name}:")
                for course in results:
                    print(f"- {course[0]}")
            else:
                print(f"No courses found for degree: {degree_name}")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Main loop
def main():
    while True:
        choice = show_menu()
        if choice == '1':
            enter_degree()
        elif choice == '2':
            pass  # Add functions for course entry
        elif choice == '3':
            pass  # Add functions for section entry
        elif choice == '4':
            pass  # Add functions for evaluation entry
        elif choice == '5':
            query_data()
        elif choice == '6':
            print("Exiting Program Evaluation System.")
            break
        else:
            print("Invalid choice. Try again.")

# Run the program
if __name__ == "__main__":
    main()