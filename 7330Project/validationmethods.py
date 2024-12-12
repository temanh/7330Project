# Validators
def validate_degree_input(name, level, description):
    if not name or not level or not description:
        raise ValueError("All fields (name, level, description) are required.")
    if len(name) > 100 or len(level) > 50 or len(description) > 500:
        raise ValueError("Input exceeds allowed length.")
    return True

def validate_course_input(course_id, course_name):
    if not course_id or not course_name:
        raise ValueError("CourseID and CourseName are required.")
    if len(course_id) > 20 or len(course_name) > 100:
        raise ValueError("Input exceeds allowed length.")
    return True

def validate_instructor_input(instructor_id, name):
    if not instructor_id or not name:
        raise ValueError("InstructorID and Name are required.")
    if len(instructor_id) > 20 or len(name) > 100:
        raise ValueError("Input exceeds allowed length.")
    return True

def validate_section_input(course_id, year, semester, section_id, enrolled_students, instructor_id):
    if not course_id or not year or not semester or not section_id:
        raise ValueError("CourseID, Year, Semester, and SectionID are required.")
    if not isinstance(enrolled_students, int) or enrolled_students < 0:
        raise ValueError("EnrolledStudents must be a non-negative integer.")
    if instructor_id and len(instructor_id) > 20:
        raise ValueError("InstructorID exceeds allowed length.")
    return True

def validate_goal_input(goal_id, degree_id, code, description):
    if not goal_id or not degree_id or not code or not description:
        raise ValueError("GoalID, DegreeID, Code, and Description are required.")
    if len(goal_id) > 20 or len(code) > 50 or len(description) > 500:
        raise ValueError("Input exceeds allowed length.")
    return True

# Methods with validation
def add_degree(name, level, description):
    try:
        validate_degree_input(name, level, description)
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
    except ValueError as ve:
        print(f"Validation Error: {ve}")

def add_course(course_id, course_name):
    try:
        validate_course_input(course_id, course_name)
        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO Courses (CourseID, CourseName) VALUES (%s, %s)"
                cursor.execute(query, (course_id, course_name))
                connection.commit()
                print(f"Course '{course_name}' with ID '{course_id}' created successfully!")
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
    except ValueError as ve:
        print(f"Validation Error: {ve}")

def add_instructor(instructor_id, name):
    try:
        validate_instructor_input(instructor_id, name)
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
    except ValueError as ve:
        print(f"Validation Error: {ve}")

def add_section(course_id, year, semester, section_id, enrolled_students=0, instructor_id=""):
    try:
        validate_section_input(course_id, year, semester, section_id, enrolled_students, instructor_id)
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
    except ValueError as ve:
        print(f"Validation Error: {ve}")

def add_goal(goal_id, degree_id, code, description):
    try:
        validate_goal_input(goal_id, degree_id, code, description)
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
    except ValueError as ve:
        print(f"Validation Error: {ve}")

def link_course_with_goal(course_id, goal_id):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()

            # Check if CourseID exists
            cursor.execute("SELECT 1 FROM Courses WHERE CourseID = %s", (course_id,))
            if cursor.fetchone() is None:
                print(f"Invalid CourseID: {course_id}")
                return

            # Check if GoalID exists
            cursor.execute("SELECT 1 FROM Goals WHERE GoalID = %s", (goal_id,))
            if cursor.fetchone() is None:
                print(f"Invalid GoalID: {goal_id}")
                return

            # If valid, insert into CourseGoal table
            cursor.execute("""
                INSERT INTO CourseGoal(CourseID, GoalID)
                VALUES(%s, %s);
            """, (course_id, goal_id))
            connection.commit()
            print(f'Successfully associated CourseID {course_id} with GoalID {goal_id}.')
        except Error as e:
            print(f'Course-Goal Association Invalid: {course_id}, GoalID: {goal_id}. Error: {e}')
        finally:
            cursor.close()
            connection.close()

            