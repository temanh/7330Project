import mysql.connector
from mysql.connector import Error
from datetime import datetime 






##### CONNECT TO DB 
def connect_to_db():
    """Establish a connection to the database."""
    try:
        connection = mysql.connector.connect(
            host="",
            user="",
            password="",
            database="ProgramEvaluation"
        )
        return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None





##### ADD METHODS

# Add Degree Method
def add_degree(name, level, description):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO Degrees (Name, Level, Description) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, level, description))
            connection.commit()
            print("Degree created successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()



# Add a new course
def add_course(course_Id, courseName):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO Courses (CourseID, CourseName) VALUES (%s, %s)"
            cursor.execute(query, (course_Id, courseName))
            connection.commit()
            print(f"Course '{courseName}' with ID '{course_Id}' created successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Add a new instructor
def add_instructor(instructor_id, name):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO Instructors (InstructorID, Name) VALUES (%s, %s)"
            cursor.execute(query, (instructor_id, name))
            connection.commit()
            print(f"Instructor '{name}' with ID '{instructor_id}' created successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()


# Add a new section
def add_section(course_id, year, semester, section_id, enrolled_students=0, instructor_id=""):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO Sections (CourseID, Year, Semester, SectionId, EnrolledStudents, InstructorId) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (course_id, year, semester, section_id, enrolled_students, instructor_id))
            connection.commit()
            print(f"Section '{section_id}' for Course ID '{course_id}' created successfully with {enrolled_students} students enrolled!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Add a new goal
def add_goal(goal_id, degree_id, code, description):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO Goals (GoalID, DegreeID, Code, Description)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(query, (goal_id, degree_id, code, description))
            connection.commit()
            print(f"Goal with ID '{goal_id}' added successfully under Degree ID '{degree_id}'.")
        except Error as e:
            print(f"Error while adding goal: {e}")
        finally:
            cursor.close()
            connection.close()

# Link/Associate a course with a goal
def link_course_with_goal(course_id, goal_id):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO CourseGoal(CourseID, GoalID)
                VALUES(%s, %s);
            """, (course_id, goal_id))

            connection.commit()
            print(f'Successfully associated CourseID {course_id} with GoalID {goal_id}.')
        except mysql.connector.Error as err:
            print(f'Course-Goal Association Invalid: {course_id}, GoalID: {goal_id}. Error: {err}')
        finally:
            cursor.close()  
            connection.close()


# Add a course for a given semester
def add_offered_course(cursor, course_id, semester_name, year):
    try:
        # Find SemesterID
        cursor.execute("""
            SELECT SemesterID FROM Semester WHERE Name = %s AND Year = %s;
        """, (semester_name, year))
        semester = cursor.fetchone()
        if not semester:
            print(f'Semester Not Found: {semester_name} {year}')
            return
        semester_id = semester[0]

        # Add offered course
        cursor.execute("""
            INSERT INTO OfferedCourse(CourseID, SemesterID)
            VALUES(%s, %s);
        """, (course_id, semester_id))
    except mysql.connector.Error as err:
        print(f'Offered Course Input Invalid: {course_id}, {semester_name}, {year}')
    
def update_course_name(course_id, new_name):
    """
    Update the name of a course in the database based on its CourseID.
    """
    connection = connect_to_db()
    
    if connection:
        try:
            cursor = connection.cursor()

            # Update the course name
            cursor.execute("""
                UPDATE Courses
                SET CourseName = %s
                WHERE CourseID = %s;
            """, (new_name, course_id))

            if cursor.rowcount == 0:
                print(f"Course Not Found: {course_id}")
            else:
                connection.commit()  # Commit the transaction
                print(f"Course Updated: {course_id} -> {new_name}")
        except Error as err:
            print(f"Course Update Failed: {course_id}, {new_name}. Error: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Unable to connect to the database.")
        




##### END ADD METHODS











#### DELETE METHODS 
def execute_query(query, data=None):
    connection = connect_to_db()
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


#### END DELETE METHODS 











#### READ METHODS 
def execute_query(query, data=None, fetch=False):
    connection = connect_to_db()
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
    query = "SELECT DegreeID, Name, Level, Description FROM Degrees;"
    results = execute_query(query, fetch=True)
    if results:
        print("\nAvailable Degrees:")
        degree_choices = []
        for row in results:
            degree_id, name, level, description = row
            print(f"Degree ID: {degree_id}, Name: {name}, Level: {level}, Description: {description}")
            degree_choices.append(degree_id)
        return degree_choices
    else:
        print("No degrees found.")
        return None

        
# Get all courses
def get_all_courses():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT CourseID, CourseName FROM Courses;")
            return cursor.fetchall() 
        except mysql.connector.Error as e:
            print(f"Error retrieving courses: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    return []

# Get courses by degree id 
def list_courses_by_degree(degree_id):
    query = """
        SELECT c.CourseID, c.CourseName, dc.IsCore
        FROM Courses c
        JOIN Degree_Courses dc ON c.CourseID = dc.CourseID
        WHERE dc.DegreeID = %s;
    """
    # Pass parameters directly as a tuple if `params` is not a valid keyword
    results = execute_query(query, (degree_id,), fetch=True)
    if results:
        print(f"\nCourses for Degree ID {degree_id}:")
        for row in results:
            course_id, course_name, is_core = row
            core_status = "Core" if is_core else "Elective"
            print(f"Course ID: {course_id}, Name: {course_name}, Type: {core_status}")
    else:
        print(f"No courses found for Degree ID {degree_id}.")

    
# Get all goals
def get_all_goals():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT GoalID, DegreeID, Description FROM Goals;")
            results = cursor.fetchall()

            # Check if results are not empty
            if results:
                print("\nAvailable Goals:")
                for goal_id, degree_id, description in results:
                    print(f"Goal ID: {goal_id}, Degree ID: {degree_id}, Description: {description}")
            else:
                print("No goals found.")
                
        except mysql.connector.Error as e:
            print(f"Error retrieving goals: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Connection to the database failed.")

# Get all instructors
def get_all_instructors():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT InstructorID, Name FROM Instructors;") 
            return cursor.fetchall()  
        except mysql.connector.Error as e:
            print(f"Error retrieving instructors: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    return []

def view_all_courses():
    """
    Fetch and return all courses with their CourseID and CourseName.
    """
    connection = connect_to_db()
    courses = []  # Initialize list to store course records

    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT CourseID, CourseName FROM Courses"  # Query to fetch all courses
            cursor.execute(query)
            courses = cursor.fetchall()  # Fetch all rows
        except Error as e:
            print(f"Error retrieving courses: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Unable to connect to the database.")

    return courses  # Return the list of courses



# Get a single course by CourseNumber
def get_course_id(course_name):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT CourseID FROM Courses WHERE CourseName = %s;", (course_name,))
            course = cursor.fetchone()
            return course[0] if course else None  # Return CourseID or None if not found
        except mysql.connector.Error as e:
            print(f"Error retrieving Course ID for {course_name}: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    return None

#### END READ METHODS 


#### SPECIAL METHODS 
def enter_course_section_for_semester(course_id, semester, year):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()

            # Insert into Sections
            try:
                cursor.execute(""" 
                    INSERT INTO Sections (CourseID, Semester, Year)
                    VALUES (%s, %s, %s);
                """, (course_id, semester, year))
                connection.commit()
                print(f"Successfully added section for Course ID {course_id} in {semester} {year}.")
            except mysql.connector.Error as err:
                print(f"Error inserting section: {err}")
        except mysql.connector.Error as e:
            print(f"Database operation failed: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Database connection failed.")
        



def list_sections_by_year_range(start_year, end_year):
    """
    List all sections offered in the specified year range (inclusive).
    """
    query = """
        SELECT SectionID, CourseID, Year, Semester
        FROM Sections
        WHERE Year BETWEEN {start_year} AND {end_year}
        ORDER BY Year ASC, Semester ASC;
    """.format(start_year=start_year, end_year=end_year)

    results = execute_query(query, fetch=True)  # No params argument needed now
    if results:
        print(f"\nSections offered between {start_year} and {end_year}:")
        for row in results:
            section_id, course_id, year, semester = row
            print(f"Section ID: {section_id}, Course ID: {course_id}, Year: {year}, Semester: {semester}")
    else:
        print(f"No sections found between {start_year} and {end_year}.")
        

def enter_evaluations(semester, instructor_id):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()

            # List sections taught by the instructor for the given semester
            cursor.execute(""" 
                SELECT SectionID, CourseID, Year 
                FROM Sections 
                WHERE InstructorID = %s AND Semester = %s;
            """, (instructor_id, semester))
            sections = cursor.fetchall()

            if not sections:
                print("No sections found for this instructor in the given semester.")
                return
            
            print("\nSections taught by the instructor:")
            for section in sections:
                print(f"Section ID: {section[0]}, Course ID: {section[1]}, Year: {section[2]}")

            # Fetch and display available Goal IDs and their descriptions
            cursor.execute("SELECT GoalID, Description FROM Goals;")
            goals = cursor.fetchall()

            print("\nAvailable Goals:")
            for goal in goals:
                print(f"Goal ID: {goal[0]}, Description: {goal[1]}")

            # Check existing evaluations
            evaluations = []
            for section in sections:
                cursor.execute(""" 
                    SELECT CourseID, EvaluationMethod, GoalID 
                    FROM Evaluations 
                    WHERE SectionID = %s;
                """, (section[0],))
                evals = cursor.fetchall()
                evaluations.extend(evals)

            # Display existing evaluations
            if evaluations:
                print("\nExisting Evaluations:")
                for eval in evaluations:
                    print(f"Course ID: {eval[0]}, Evaluation Method: {eval[1]}, Goal ID: {eval[2]}")
            else:
                print("No evaluations found for these sections.")

            # Option to enter new data or change existing data
            action = input("\nWould you like to (A)dd new evaluations, (C)hange existing evaluations, or (N)o changes? ").strip().lower()
            if action == 'a':
                # Add new evaluations logic
                for section in sections:
                    goal_id = input(f"Enter Goal ID for Section ID {section[0]}: ").strip()
                    evaluation_method = input("Enter Evaluation Method: ").strip()
                    grade_a = input("Enter Grade A (default 0): ").strip() or 0
                    grade_b = input("Enter Grade B (default 0): ").strip() or 0
                    grade_c = input("Enter Grade C (default 0): ").strip() or 0
                    grade_f = input("Enter Grade F (default 0): ").strip() or 0
                    improvement_notes = input("Enter Improvement Notes: ").strip()

                    # Insert new evaluation
                    cursor.execute(""" 
                        INSERT INTO Evaluations (CourseID, Year, Semester, SectionID, GoalID, EvaluationMethod, GradeA, GradeB, GradeC, GradeF, ImprovementNotes) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, (section[1], section[2], semester, section[0], goal_id, evaluation_method, grade_a, grade_b, grade_c, grade_f, improvement_notes))
                    print(f"Evaluation added for Section ID {section[0]}.")
                
                connection.commit()  # Commit the transaction after all inserts
            elif action == 'c':
                # Change existing evaluations logic
                for eval in evaluations:
                    new_data = input(f"Enter new evaluation data for Evaluation ID {eval[0]} (current: {eval[1]}): ").strip()
                    cursor.execute("""
                        UPDATE Evaluations 
                        SET EvaluationMethod = %s 
                        WHERE EvaluationID = %s;
                    """, (new_data, eval[0]))
                    print(f"Evaluation ID {eval[0]} updated.")
                connection.commit()
            elif action == 'n':
                print("No changes made.")
            else:
                print("Invalid action. Please select A, C, or N.")

            # Duplicate evaluation option
            duplicate = input("\nWould you like to duplicate an evaluation to another degree? (Y/N): ").strip().lower()
            if duplicate == 'y':
                # Logic for duplicating evaluations to other degrees
                degree_id = input("Enter the degree ID to duplicate evaluations to: ").strip()
                for eval in evaluations:
                    cursor.execute("""
                        INSERT INTO Evaluations (SectionID, EvaluationMethod, GoalID, DegreeID) 
                        VALUES (%s, %s, %s, %s);
                    """, (eval[0], eval[1], eval[2], degree_id))
                    print(f"Evaluation duplicated for Degree ID {degree_id}.")

                connection.commit()

        except mysql.connector.Error as e:
            print(f"Database operation failed: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Database connection failed.")
        


def link_degree_with_course(course_id, course_name):
    """
    Link a course to a degree in the database based on course ID and course name.
    """
    connection = connect_to_db()
    
    if connection:
        try:
            cursor = connection.cursor()

            # Check if the course exists
            check_query = "SELECT CourseID FROM Courses WHERE CourseID = %s AND CourseName = %s"
            cursor.execute(check_query, (course_id, course_name))
            course_exists = cursor.fetchone()

            if course_exists:
                # Link the course to a degree 
                link_query = """
                INSERT INTO degree_courses (DegreeID, CourseID, IsCore)
                VALUES (%s, %s, 1)
                """
                degree_id = input("Enter degree ID to link with this course: ").strip()
                cursor.execute(link_query, (degree_id, course_id))
                connection.commit()  # Commit the transaction
                print(f"Successfully linked course {course_name} (ID: {course_id}) to degree ID {degree_id}.")
            else:
                print("The specified course does not exist. Please check the Course ID and Course Name.")
        
        except Error as e:
            print(f"Error linking course with degree: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Unable to connect to the database.")
        


#### SPECIAL METHODS END











# Main loop
def main_menu():
    while True:
        print("\n--- Degree Management System ---")

        # Group: Degree Operations
        print("\n--- Degree Operations ---")
        print("1.  Add a degree")
        print("2.  Link degree with course")
        print("3.  View all degrees")
        print("4.  View a degree by ID")
        print("5.  Delete a degree")

        # Group: Course Operations
        print("\n--- Course Operations ---")
        print("6.  Add a course")
        print("7.  Link course with goal")
        print("8.  View all courses")
        print("9.  List courses by degree")
        print("10. Update course name")
        print("11. Delete a course")
        print("12. Enter course/section for a given semester")  

        # Group: Instructor and Section Operations
        print("\n--- Instructor and Section Operations ---")
        print("13. Add an instructor")
        print("14. Add a section")
        print("15. List sections")

        # Group: Goals
        print("\n--- Goal Operations ---")
        print("16. Add a goal")
        print("17. List goals")
       
        # Group: Evaluations
        print("\n--- Enter Evaluations ---")
        print("18. Enter evaluations")  

        # Exit
        print("\n")
        print("19. Exit")
        choice = input("Choose an operation (1-19): ").strip()

        if choice == "1":
            name = input("Enter the name of the degree: ").strip()
            level = input("Enter the level of the degree: ").strip()
            description = input("Enter a description for the degree: ").strip()
            if name and level and description:
                add_degree(name, level, description)
            else:
                print("All fields are required.")
        elif choice == "2":
              # Preview all courses
            courses = view_all_courses()  # Fetch all courses
    
            if courses:
                print("Available Courses:")
                print(f"{'CourseID':<10} {'CourseName':<20}")  # Header
                print("-" * 30)
                for course_id, course_name in courses:
                    print(f"{course_id:<10} {course_name:<20}")
                print("-" * 30)

                # Prompt user for CourseID and CourseName
                course_id = input("Enter course ID: ").strip()
                course_name = input("Enter course name: ").strip()

                if course_id and course_name:
                    link_degree_with_course(course_id, course_name)
                else:
                    print("All fields are required.")
            else:
                print("No courses available to link.")
        elif choice == "3":
              valid_degrees = get_valid_degrees() 
              print("Available Degrees:")

              if valid_degrees:
                    for degree_id, name in valid_degrees:
                        print(f"ID: {degree_id}, Name: {name}")
              else:
                    print("No degrees found or unable to retrieve data.")
        elif choice == "4":
            degree_id = input("Enter degree ID: ").strip()
            result = view_degree_by_id(degree_id) 

            if result:
                print(f"Degree Details:\nID: {result[0]}, Name: {result[1]}")
            else:
                print("No degree found with the given ID.")
        elif choice == "5":
            delete_degree()
        elif choice == "6":
            course_name = input("Enter the name of the course: ").strip()
            level = input("Enter the level of the course: ").strip()
            description = input("Enter a description for the course: ").strip()
            if course_name and level and description:
                add_course(course_name, level)
            else:
                print("All fields are required.")
        elif choice == "7":
            course_id = input("Enter the CourseID to associate with a goal: ").strip()
            link_course_with_goal(course_id)
        elif choice == "8":
            courses = view_all_courses()  # Call the function and store the results

            if courses:
                print("All Courses:")
                print(f"{'CourseID':<10} {'CourseName':<20}")  # Header with column names
                print("-" * 30)  # Divider line
                for course_id, course_name in courses:
                    print(f"{course_id:<10} {course_name:<20}")  # Display each course
            else:
                print("No courses found or unable to retrieve data.")
        elif choice == "9":
            degree_choices = get_all_degrees()
            if degree_choices:
                while True:
                    try:
                        degree_id = input("\nEnter Degree ID to list courses: ").strip()
                        if int(degree_id) in degree_choices:
                            list_courses_by_degree(degree_id)
                            break
                        else:
                            print("Invalid Degree ID. Please select from the available options.")
                    except ValueError:
                        print("Please enter a valid numeric Degree ID.")
        elif choice == "10":
             # Preview all courses
            courses = view_all_courses()  # Fetch all courses
    
            if courses:
                print("Available Courses:")
                print(f"{'CourseID':<10} {'CourseName':<20}")  # Header
                print("-" * 30)
                for course_id, course_name in courses:
                    print(f"{course_id:<10} {course_name:<20}")
                print("-" * 30)

                # Ask user for the CourseID and new CourseName
                course_id = input("Enter the CourseID to update: ").strip()
                new_course_name = input("Enter the new name for the course: ").strip()
        
                if course_id and new_course_name:
                    update_course_name(course_id, new_course_name)
                else:
                    print("Both Course ID and new Course Name are required.")
            else:
                print("No courses available to update.")
        elif choice == "11":
            course_id = input("Enter the CourseID to delete: ").strip()
            delete_course(course_id)
        elif choice == "12":
            courses = get_all_courses()
            if not courses:
                print("No courses available to assign to a section.")
                continue  # Go back to menu

            print("Available Courses:")
            for course in courses:
                print(f"Course ID: {course[0]}, Course Name: {course[1]}")

            # Input for Course ID
            course_id = input("Enter the Course ID to associate with a section: ").strip()

            # Input for Semester
            semester = input("Enter the Semester (e.g., Fall, Spring, Summer): ").strip()

            # Input for Year
            while True:
                year_input = input("Enter the Year (e.g., 2024): ").strip()
                if len(year_input) == 4 and year_input.isdigit():  # Check if it is 4 digits and numeric
                    year = int(year_input)
                    break
                else:
                    print("Invalid input. Please enter a valid four-digit year.")
            enter_course_section_for_semester(course_id, semester, year)
            
        elif choice == "13":
            instructor_id = input("Enter instructor ID: ").strip()
            instructor_name = input("Enter instructor name: ").strip()
            add_instructor(instructor_id, instructor_name)
        elif choice == "14":
            courses = get_all_courses()
            if not courses:
                print("No courses available to select.")
            else:
                print("Available Courses:")
                for course in courses:
                    print(f"Course ID: {course[0]}, Course Name: {course[1]}")

                # Prompt user for input parameters
                course_id = input("Enter the Course ID from the above list: ").strip()

                # Ensure that the course ID is valid
                valid_course_ids = [course[0] for course in courses]
                while course_id not in valid_course_ids:
                    print("Invalid Course ID. Please select a valid Course ID from the list.")
                    course_id = input("Enter the Course ID from the above list: ").strip()

                year = input("Enter the Year (e.g., 2024): ").strip()

                # Ensure the year is a four-digit number
                while not (year.isdigit() and len(year) == 4):
                    print("Invalid input. Please enter a valid four-digit year.")
                    year = input("Enter the Year (e.g., 2024): ").strip()

                semester = input("Enter the Semester (e.g., Fall, Spring, Summer): ").strip()
                section_id = input("Enter the Section ID: ").strip()

                # Prompt for the number of enrolled students (default is 0)
                enrolled_students_input = input("Enter the number of enrolled students (default is 0): ").strip()
                enrolled_students = int(enrolled_students_input) if enrolled_students_input else 0

                # Get all instructors and display them
                instructors = get_all_instructors()

                if not instructors:
                    print("No instructors available to select.")
                    instructor_id = None  # No instructor option
                else:
                    print("Available Instructors:")
                    for instructor in instructors:
                        print(f"Instructor ID: {instructor[0]}, Instructor Name: {instructor[1]}")

                    instructor_id = input("Enter the Instructor ID from the above list (leave blank if no instructor): ").strip() or None
            
                    # Ensure that the instructor ID is valid
                    if instructor_id and instructor_id not in [str(instructor[0]) for instructor in instructors]:
                        print("Invalid Instructor ID. Setting instructor to None.")
                        instructor_id = None

                # Call the add_section method with the gathered parameters
                add_section(course_id, year, semester, section_id, enrolled_students, instructor_id)
                
        elif choice == "15":
            print("\nSpecify the year range:")
            try:
                start_year = int(input("Enter the start year: ").strip())
                end_year = int(input("Enter the end year: ").strip())

                if start_year > end_year:
                    print("Start year must not be greater than the end year.")
                else:
                    list_sections_by_year_range(start_year, end_year)
            except ValueError:
                print("Invalid year entered. Please enter numeric values for the year range.")
        elif choice == "16":
            goal_id = input("Enter the goal ID: ").strip()
            degree_id = input("Enter the degree ID: ").strip()
            code = input("Enter code: ").strip()
            description = input("Enter description: ").strip()
            add_goal(goal_id, degree_id, code, description)
        elif choice == "17":
            get_all_goals()
        elif choice == "18":
              semester = input("Enter the Semester (e.g., Fall, Spring, Summer): ").strip()
              # Get all instructors and display them
              instructors = get_all_instructors()
              if not instructors:
                    print("No instructors available to select.")
                    instructor_id = None  # No instructor option
              else:
                    print("Available Instructors:")
                    for instructor in instructors:
                        print(f"Instructor ID: {instructor[0]}, Instructor Name: {instructor[1]}")
              instructor_id = input("Enter the Instructor ID: ").strip()
              enter_evaluations(semester, instructor_id)  # Pass the parameters
        elif choice == "19":
            print("Exiting the system.")
        else:
            print("Invalid choice, please try again.")
            
        # Prompt to go back to the main menu
        input("\nPress Enter to return to the main menu...")

# END Main loop


### VALIDATION METHODS 
def degree_exists(degree_id):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT 1 FROM Degrees WHERE DegreeID = %s"
            cursor.execute(query, (degree_id,))
            result = cursor.fetchone()
            return result is not None  # Returns True if a degree exists, False otherwise
        except Error as e:
            print(f"Error checking degree existence: {e}")
            return False
        finally:
            cursor.close()
            connection.close()


### USED IN CHOICE #5
def get_valid_degrees():
    connection = connect_to_db()
    degrees = []
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT DegreeID, Name FROM Degrees"
            cursor.execute(query)
            degrees = cursor.fetchall()  # Fetch all DegreeID and Name pairs
        except Error as e:
            print(f"Error retrieving valid degrees: {e}")
        finally:
            cursor.close()
            connection.close()
    return degrees


def view_degree_by_id(degree_id):
    connection = connect_to_db()
    degree_details = None 

    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT DegreeID, Name FROM Degrees WHERE DegreeID = %s"
            cursor.execute(query, (degree_id,)) 
            degree_details = cursor.fetchone() 
        except Error as e:
            print(f"Error retrieving degree: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Unable to connect to the database.")

    return degree_details  # Return the fetched result or None



### END VALIDATION METHODS 



# Calling the main menu
if __name__ == "__main__":
    main_menu()
