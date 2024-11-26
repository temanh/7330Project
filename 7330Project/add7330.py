import mysql.connector


def add_degree(cursor, name, level):
    try:
        cursor.execute("""
            INSERT INTO Degree(Name, Level)
            VALUES(%s, %s);
        """, (name, level))
    except mysql.connector.Error as err:
        print(f'Degree Input Invalid: {name}, {level}')


# Add a new course
def add_course(cursor, course_id, name):
    try:
        cursor.execute("""
            INSERT INTO Course(CourseID, Name)
            VALUES(%s, %s);
        """, (course_id, name))
    except mysql.connector.Error as err:
        print(f'Course Input Invalid: {course_id}, {name}')


# Add a new instructor
def add_instructor(cursor, instructor_id, name):
    try:
        cursor.execute("""
            INSERT INTO Instructor(InstructorID, Name)
            VALUES(%s, %s);
        """, (instructor_id, name))
    except mysql.connector.Error as err:
        print(f'Instructor Input Invalid: {instructor_id}, {name}')


# Add a new section
def add_section(cursor, offered_course_id, section_number, students_enrolled=0):
    try:
        cursor.execute("""
            INSERT INTO Section(OfferedCourseID, SectionNumber, StudentsEnrolled)
            VALUES(%s, %s, %s);
        """, (offered_course_id, section_number, students_enrolled))
    except mysql.connector.Error as err:
        print(f'Section Input Invalid: {offered_course_id}, {section_number}, {students_enrolled}')


# Add a new goal
def add_goal(cursor, goal_name):
    try:
        cursor.execute("""
            INSERT INTO Goal(GoalName)
            VALUES(%s);
        """, (goal_name,))
    except mysql.connector.Error as err:
        print(f'Goal Input Invalid: {goal_name}')


# Associate a course with a goal
def associate_course_with_goal(cursor, course_id, goal_name):
    try:
        # Find GoalID
        cursor.execute("""
            SELECT GoalID FROM Goal WHERE GoalName = %s;
        """, (goal_name,))
        goal = cursor.fetchone()
        if not goal:
            print(f'Goal Not Found: {goal_name}')
            return
        goal_id = goal[0]

        # Associate course with goal
        cursor.execute("""
            INSERT INTO CourseGoal(CourseID, GoalID)
            VALUES(%s, %s);
        """, (course_id, goal_id))
    except mysql.connector.Error as err:
        print(f'Course-Goal Association Invalid: {course_id}, {goal_name}')


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
    
def update_course_name(cursor, course_id, new_name):
    try:
        # Update the course name
        cursor.execute("""
            UPDATE Course
            SET Name = %s
            WHERE CourseID = %s;
        """, (new_name, course_id))
        if cursor.rowcount == 0:
            print(f'Course Not Found: {course_id}')
        else:
            print(f'Course Updated: {course_id} -> {new_name}')
    except mysql.connector.Error as err:
        print(f'Course Update Failed: {course_id}, {new_name}')
        