import mysql.connector

# Database connection function
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your database username
        password="12345678",  # Replace with your database password
        database="7300"
    )

# Add Degree
def add_degree():
    name = input("Enter Degree Name: ")
    level = input("Enter Degree Level (e.g., BA, MS, PhD): ")
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Degrees (name, level) VALUES (%s, %s)", (name, level))
        conn.commit()
        print(f"Degree '{name}' ({level}) added successfully!")
    except Exception as e:
        print(f"Failed to add degree: {e}")
    finally:
        cursor.close()
        conn.close()

# Add Course
def add_course():
    course_number = input("Enter Course Number (e.g., CS101): ")
    name = input("Enter Course Name: ")
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Courses (course_number, name) VALUES (%s, %s)", (course_number, name))
        conn.commit()
        print(f"Course '{course_number} - {name}' added successfully!")
    except Exception as e:
        print(f"Failed to add course: {e}")
    finally:
        cursor.close()
        conn.close()

# Add Instructor
def add_instructor():
    instructor_id = input("Enter Instructor ID (8 digits): ")
    name = input("Enter Instructor Name: ")
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Instructors (instructor_id, name) VALUES (%s, %s)", (instructor_id, name))
        conn.commit()
        print(f"Instructor '{name}' (ID: {instructor_id}) added successfully!")
    except Exception as e:
        print(f"Failed to add instructor: {e}")
    finally:
        cursor.close()
        conn.close()

# Add Section
def add_section():
    course_id = input("Enter Course ID: ")
    semester = input("Enter Semester (Spring, Summer, Fall): ")
    year = input("Enter Year: ")
    section_number = input("Enter Section Number (3 digits): ")
    enrolled_students = input("Enter Number of Enrolled Students: ")
    instructor_id = input("Enter Instructor ID: ")
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Sections (course_id, semester, year, section_number, enrolled_students, instructor_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (course_id, semester, year, section_number, enrolled_students, instructor_id))
        conn.commit()
        print(f"Section '{section_number}' added successfully to Course '{course_id}'!")
    except Exception as e:
        print(f"Failed to add section: {e}")
    finally:
        cursor.close()
        conn.close()

# Add Goal
def add_goal():
    degree_id = input("Enter Degree ID: ")
    code = input("Enter Goal Code (4 characters): ")
    description = input("Enter Goal Description: ")
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Goals (degree_id, code, description) VALUES (%s, %s, %s)", (degree_id, code, description))
        conn.commit()
        print(f"Goal '{code}' added successfully!")
    except Exception as e:
        print(f"Failed to add goal: {e}")
    finally:
        cursor.close()
        conn.close()

# Associate Courses with Goals
def associate_course_with_goal():
    course_id = input("Enter Course ID: ")
    goal_id = input("Enter Goal ID: ")
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Goals SET id = %s WHERE id = %s", (course_id, goal_id))
        conn.commit()
        print(f"Course ID '{course_id}' has been successfully associated with Goal ID '{goal_id}'!")
    except Exception as e:
        print(f"Association failed: {e}")
    finally:
        cursor.close()
        conn.close()

# Add Courses and Sections for a Given Semester
def add_courses_and_sections_for_semester():
    semester = input("Enter Semester (Spring, Summer, Fall): ")
    year = input("Enter Year: ")
    while True:
        course_id = input("Enter Course ID (or type 'exit' to finish): ")
        if course_id.lower() == 'exit':
            break
        section_number = input("Enter Section Number (3 digits): ")
        enrolled_students = input("Enter Number of Enrolled Students: ")
        instructor_id = input("Enter Instructor ID: ")
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Sections (course_id, semester, year, section_number, enrolled_students, instructor_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (course_id, semester, year, section_number, enrolled_students, instructor_id))
            conn.commit()
            print(f"Section '{section_number}' has been successfully added to Course '{course_id}'!")
        except Exception as e:
            print(f"Failed to add section: {e}")
        finally:
            cursor.close()
            conn.close()


def manage_evaluation():
    semester = input("Enter Semester (Spring, Summer, Fall): ")
    year = input("Enter Year: ")
    instructor_id = input("Enter Instructor ID: ")

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    try:
        # Check if the instructor exists
        cursor.execute("SELECT id, name FROM Instructors WHERE id = %s", (instructor_id,))
        instructor = cursor.fetchone()
        if not instructor:
            print(f"Error: Instructor ID {instructor_id} does not exist.")
            return

        # Get sections taught by the instructor in the given semester and year
        cursor.execute("""
            SELECT s.id AS section_id, c.course_number, s.section_number, s.enrolled_students
            FROM Sections s
            JOIN Courses c ON s.course_id = c.id
            WHERE s.instructor_id = %s AND s.semester = %s AND s.year = %s
        """, (instructor_id, semester, year))
        sections = cursor.fetchall()

        if not sections:
            print(f"No sections found for Instructor ID {instructor_id} in {semester} {year}.")
            return

        # Display sections and their evaluation status
        print(f"\nSections taught by {instructor['name']} ({instructor_id}) in {semester} {year}:")
        for section in sections:
            cursor.execute("""
                SELECT e.id, e.goal_id, e.evaluation_method, e.grade_a, e.grade_b, e.grade_c, e.grade_f
                FROM Evaluations e
                WHERE e.section_id = %s
            """, (section['section_id'],))
            evaluations = cursor.fetchall()

            print(f"\nSection: {section['course_number']} - {section['section_number']}")
            print(f"Enrolled Students: {section['enrolled_students']}")
            if evaluations:
                print("Existing Evaluations:")
                for eval in evaluations:
                    print(f"  Goal ID: {eval['goal_id']}, Method: {eval['evaluation_method']}, "
                          f"Grades - A: {eval['grade_a']}, B: {eval['grade_b']}, "
                          f"C: {eval['grade_c']}, F: {eval['grade_f']}")
            else:
                print("No evaluation data available.")

            # Prompt user to manage evaluations
            while True:
                action = input("Choose an action: (1) Enter New, (2) Modify Existing, (3) Skip: ")
                if action == "1":
                    add_evaluation_for_section(section['section_id'])
                    break
                elif action == "2":
                    modify_evaluation_for_section(section['section_id'])
                    break
                elif action == "3":
                    print("Skipping this section.")
                    break
                else:
                    print("Invalid choice. Please choose 1, 2, or 3.")

        # Handle duplication to other degrees
        duplicate = input("\nDo you want to duplicate evaluations for courses associated with multiple degrees? (yes/no): ")
        if duplicate.lower() == "yes":
            duplicate_evaluations_to_other_degrees(cursor)

    except Exception as e:
        print(f"Error managing evaluations: {e}")
    finally:
        cursor.close()
        conn.close()


# Add evaluation for a specific section
def add_evaluation_for_section(section_id):
    goal_id = input("Enter Goal ID: ")
    evaluation_method = input("Enter Evaluation Method (e.g., Homework, Quiz, Project): ")
    grade_a = input("Enter Number of Students with Grade A: ")
    grade_b = input("Enter Number of Students with Grade B: ")
    grade_c = input("Enter Number of Students with Grade C: ")
    grade_f = input("Enter Number of Students with Grade F: ")
    improvement_suggestion = input("Enter Improvement Suggestion (optional, press Enter to skip): ")

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Evaluations 
            (section_id, goal_id, evaluation_method, grade_a, grade_b, grade_c, grade_f, improvement_suggestion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (section_id, goal_id, evaluation_method, grade_a, grade_b, grade_c, grade_f, improvement_suggestion))
        conn.commit()
        print(f"Evaluation added successfully for Section ID {section_id}.")
    except Exception as e:
        print(f"Failed to add evaluation: {e}")
    finally:
        cursor.close()
        conn.close()


# Modify existing evaluation for a specific section
def modify_evaluation_for_section(section_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id, goal_id, evaluation_method, grade_a, grade_b, grade_c, grade_f
            FROM Evaluations
            WHERE section_id = %s
        """, (section_id,))
        evaluations = cursor.fetchall()

        if not evaluations:
            print("No existing evaluations to modify.")
            return

        print("Existing Evaluations:")
        for eval in evaluations:
            print(f"ID: {eval['id']}, Goal ID: {eval['goal_id']}, Method: {eval['evaluation_method']}, "
                  f"Grades - A: {eval['grade_a']}, B: {eval['grade_b']}, C: {eval['grade_c']}, F: {eval['grade_f']}")

        eval_id = input("Enter the Evaluation ID to modify: ")
        new_method = input("Enter New Evaluation Method (or press Enter to keep current): ")
        new_grade_a = input("Enter New Number of Grade A (or press Enter to keep current): ")
        new_grade_b = input("Enter New Number of Grade B (or press Enter to keep current): ")
        new_grade_c = input("Enter New Number of Grade C (or press Enter to keep current): ")
        new_grade_f = input("Enter New Number of Grade F (or press Enter to keep current): ")

        cursor.execute("""
            UPDATE Evaluations
            SET evaluation_method = IF(%s = '', evaluation_method, %s),
                grade_a = IF(%s = '', grade_a, %s),
                grade_b = IF(%s = '', grade_b, %s),
                grade_c = IF(%s = '', grade_c, %s),
                grade_f = IF(%s = '', grade_f, %s)
            WHERE id = %s
        """, (new_method, new_method, new_grade_a, new_grade_a, new_grade_b, new_grade_b,
              new_grade_c, new_grade_c, new_grade_f, new_grade_f, eval_id))
        conn.commit()
        print(f"Evaluation ID {eval_id} updated successfully.")
    except Exception as e:
        print(f"Failed to modify evaluation: {e}")
    finally:
        cursor.close()
        conn.close()


# Duplicate evaluations to other degrees
def duplicate_evaluations_to_other_degrees(cursor):
    print("Duplicating evaluations to other degrees...")
    # Implementation for duplicating evaluations based on degrees
    # Example: Copy evaluation data for courses shared by multiple degrees
    print("Feature under development.")

def add_evaluation():
    section_id = input("Enter Section ID: ")
    goal_id = input("Enter Goal ID: ")
    evaluation_method = input("Enter Evaluation Method (e.g., Homework, Quiz, Project): ")
    grade_a = input("Enter Number of Students with Grade A: ")
    grade_b = input("Enter Number of Students with Grade B: ")
    grade_c = input("Enter Number of Students with Grade C: ")
    grade_f = input("Enter Number of Students with Grade F: ")
    improvement_suggestion = input("Enter Improvement Suggestion (optional, press Enter to skip): ")

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if the Section ID exists
        cursor.execute("SELECT id FROM Sections WHERE id = %s", (section_id,))
        section_exists = cursor.fetchone()

        # Check if the Goal ID exists
        cursor.execute("SELECT id FROM Goals WHERE id = %s", (goal_id,))
        goal_exists = cursor.fetchone()

        if not section_exists:
            print(f"Error: Section ID {section_id} does not exist. Please add the section first.")
            return
        if not goal_exists:
            print(f"Error: Goal ID {goal_id} does not exist. Please add the goal first.")
            return

        # Insert evaluation data
        cursor.execute("""
            INSERT INTO Evaluations 
            (section_id, goal_id, evaluation_method, grade_a, grade_b, grade_c, grade_f, improvement_suggestion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (section_id, goal_id, evaluation_method, grade_a, grade_b, grade_c, grade_f, improvement_suggestion))
        conn.commit()
        print(f"Evaluation for Section ID '{section_id}' and Goal ID '{goal_id}' added successfully!")
    except Exception as e:
        print(f"Failed to add evaluation: {e}")
    finally:
        cursor.close()
        conn.close()
def query_by_degree():
    degree_id = input("Enter Degree ID: ")
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # Query courses associated with the degree
        print("\nCourses associated with the degree:")
        cursor.execute("""
            SELECT c.course_number, c.name, dc.is_core
            FROM DegreeCourses dc
            JOIN Courses c ON dc.course_id = c.id
            WHERE dc.degree_id = %s
        """, (degree_id,))
        courses = cursor.fetchall()
        for course in courses:
            core_status = "Core" if course['is_core'] else "Elective"
            print(f"  {course['course_number']} - {course['name']} ({core_status})")

        # Query goals and associated courses
        print("\nGoals and associated courses:")
        cursor.execute("""
            SELECT g.code AS goal_code, g.description AS goal_description, 
                   IFNULL(c.course_number, 'N/A') AS course_number, 
                   IFNULL(c.name, 'N/A') AS course_name
            FROM Goals g
            LEFT JOIN Courses c ON g.id = c.id
            WHERE g.degree_id = %s
        """, (degree_id,))
        goals = cursor.fetchall()
        for goal in goals:
            print(f"  Goal: {goal['goal_code']} - {goal['goal_description']}")
            if goal['course_number'] != 'N/A':
                print(f"    Associated Course: {goal['course_number']} - {goal['course_name']}")
            else:
                print(f"    No course associated with this goal.")

        # Query sections offered for courses in this degree
        print("\nSections offered for this degree:")
        cursor.execute("""
            SELECT s.section_number, s.semester, s.year, c.course_number, i.name AS instructor_name
            FROM Sections s
            JOIN Courses c ON s.course_id = c.id
            JOIN DegreeCourses dc ON c.id = dc.course_id
            JOIN Instructors i ON s.instructor_id = i.id
            WHERE dc.degree_id = %s
            ORDER BY s.year, 
                     CASE s.semester
                        WHEN 'Spring' THEN 1
                        WHEN 'Summer' THEN 2
                        WHEN 'Fall' THEN 3
                     END
        """, (degree_id,))
        sections = cursor.fetchall()
        if sections:
            for section in sections:
                print(f"  {section['course_number']} - Section {section['section_number']}, "
                      f"{section['semester']} {section['year']}, Instructor: {section['instructor_name']}")
        else:
            print("  No sections found for this degree.")

        # Query sections within a user-defined time range
        print("\nQuery sections by time range:")
        start_year = input("Enter the start year (YYYY): ")
        end_year = input("Enter the end year (YYYY): ")
        cursor.execute("""
            SELECT c.course_number, s.section_number, s.semester, s.year, i.name AS instructor_name
            FROM Sections s
            JOIN Courses c ON s.course_id = c.id
            JOIN DegreeCourses dc ON c.id = dc.course_id
            JOIN Instructors i ON s.instructor_id = i.id
            WHERE dc.degree_id = %s AND s.year BETWEEN %s AND %s
            ORDER BY s.year, 
                     CASE s.semester
                        WHEN 'Spring' THEN 1
                        WHEN 'Summer' THEN 2
                        WHEN 'Fall' THEN 3
                     END
        """, (degree_id, start_year, end_year))
        time_range_sections = cursor.fetchall()
        if time_range_sections:
            print(f"\nSections offered between {start_year} and {end_year}:")
            for section in time_range_sections:
                print(f"  {section['course_number']} - Section {section['section_number']}, "
                      f"{section['semester']} {section['year']}, Instructor: {section['instructor_name']}")
        else:
            print(f"No sections found between {start_year} and {end_year} for this degree.")

    except Exception as e:
        print(f"Error querying by degree: {e}")
    finally:
        cursor.close()
        conn.close()


def query_by_course():
    course_id = input("Enter Course ID: ")
    semester = input("Enter Semester (Spring, Summer, Fall): ")
    year = input("Enter Year: ")
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT s.section_number, s.enrolled_students, i.name AS instructor_name
            FROM Sections s
            JOIN Instructors i ON s.instructor_id = i.id
            WHERE s.course_id = %s AND s.semester = %s AND s.year = %s
        """, (course_id, semester, year))
        sections = cursor.fetchall()
        if sections:
            print(f"\nSections for Course ID {course_id} in {semester} {year}:")
            for section in sections:
                print(f"  Section {section['section_number']}: Enrolled Students: {section['enrolled_students']}, Instructor: {section['instructor_name']}")
        else:
            print(f"No sections found for Course ID {course_id} in {semester} {year}.")
    except Exception as e:
        print(f"Error querying by course: {e}")
    finally:
        cursor.close()
        conn.close()


def query_by_instructor():
    instructor_id = input("Enter Instructor ID: ")
    semester = input("Enter Semester (Spring, Summer, Fall): ")
    year = input("Enter Year: ")
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT s.section_number, c.course_number, s.enrolled_students
            FROM Sections s
            JOIN Courses c ON s.course_id = c.id
            WHERE s.instructor_id = %s AND s.semester = %s AND s.year = %s
        """, (instructor_id, semester, year))
        sections = cursor.fetchall()
        if sections:
            print(f"\nSections taught by Instructor ID {instructor_id} in {semester} {year}:")
            for section in sections:
                print(f"  Course {section['course_number']}, Section {section['section_number']}: Enrolled Students: {section['enrolled_students']}")
        else:
            print(f"No sections found for Instructor ID {instructor_id} in {semester} {year}.")
    except Exception as e:
        print(f"Error querying by instructor: {e}")
    finally:
        cursor.close()
        conn.close()


def query_evaluation_status():
    semester = input("Enter Semester (Spring, Summer, Fall): ")
    year = input("Enter Year: ")
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT s.id AS section_id, c.course_number, s.section_number, 
                   COUNT(e.id) AS evaluation_count
            FROM Sections s
            LEFT JOIN Evaluations e ON s.id = e.section_id
            JOIN Courses c ON s.course_id = c.id
            WHERE s.semester = %s AND s.year = %s
            GROUP BY s.id
        """, (semester, year))
        sections = cursor.fetchall()
        print(f"\nEvaluation status for sections in {semester} {year}:")
        for section in sections:
            status = "Complete" if section['evaluation_count'] > 0 else "Incomplete"
            print(f"  Course {section['course_number']}, Section {section['section_number']}: {status}")
    except Exception as e:
        print(f"Error querying evaluation status: {e}")
    finally:
        cursor.close()
        conn.close()


def query_by_grade_percentage():
    semester = input("Enter Semester (Spring, Summer, Fall): ")
    year = input("Enter Year: ")
    percentage = int(input("Enter Minimum Percentage of Students Not Receiving F: "))
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT s.id AS section_id, c.course_number, s.section_number, 
                   e.grade_a, e.grade_b, e.grade_c, e.grade_f,
                   (e.grade_a + e.grade_b + e.grade_c) * 100.0 / 
                   (e.grade_a + e.grade_b + e.grade_c + e.grade_f) AS pass_percentage
            FROM Sections s
            JOIN Evaluations e ON s.id = e.section_id
            JOIN Courses c ON s.course_id = c.id
            WHERE s.semester = %s AND s.year = %s
            HAVING pass_percentage >= %s
        """, (semester, year, percentage))
        sections = cursor.fetchall()
        if sections:
            print(f"\nSections in {semester} {year} with pass percentage >= {percentage}%:")
            for section in sections:
                print(f"  Course {section['course_number']}, Section {section['section_number']}: {section['pass_percentage']:.2f}% pass rate")
        else:
            print(f"No sections found with pass percentage >= {percentage}% in {semester} {year}.")
    except Exception as e:
        print(f"Error querying by grade percentage: {e}")
    finally:
        cursor.close()
        conn.close()


def data_entry_menu():
    while True:
        print("\n=== Data Entry Menu ===")
        print("1. Add Degree")
        print("2. Add Course")
        print("3. Add Instructor")
        print("4. Add Section")
        print("5. Add Goal")
        print("6. Associate Courses with Goals")
        print("7. Add Courses and Sections for a Semester")
        print("8. Add Evaluation")
        print("9. Manage Evaluations for an Instructor")
        print("10. Query by Degree")
        print("11. Query by Course")
        print("12. Query by Instructor")
        print("13. Query Evaluation Status")
        print("14. Query Sections by Grade Percentage")
        print("15. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_degree()
        elif choice == "2":
            add_course()
        elif choice == "3":
            add_instructor()
        elif choice == "4":
            add_section()
        elif choice == "5":
            add_goal()
        elif choice == "6":
            associate_course_with_goal()
        elif choice == "7":
            add_courses_and_sections_for_semester()
        elif choice == "8":
            add_evaluation()
        elif choice == "9":
            manage_evaluation() 
        elif choice == "10":
            query_by_degree()
        elif choice == "11":
            query_by_course()
        elif choice == "12":
            query_by_instructor()
        elif choice == "13":
            query_evaluation_status()
        elif choice == "14":
            query_by_grade_percentage()
        elif choice == "15":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")

# Main entry point
if __name__ == "__main__":
    data_entry_menu()