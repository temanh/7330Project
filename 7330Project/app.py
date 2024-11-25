from read import get_all_degrees, get_all_courses, get_degree_by_id, get_course_by_number
from delete import delete_degree, delete_course

def main_menu():
    while True:
        print("\n--- Degree Management System ---")
        print("1. Add a degree")
        print("2. Add a course")
        print("3. Link a degree to a course")
        print("4. View all degrees")
        print("5. View all courses")
        print("6. View a degree by ID")
        print("7. View a course by number")
        print("8. Update course name")
        print("9. Delete a degree")
        print("10. Delete a course")
        print("11. Exit")

        choice = input("Choose an operation (1-11): ").strip()

        if choice == "1":
            break
        elif choice == "2":
            break
        elif choice == "3":
            break
        elif choice == "4":
            get_all_degrees()
        elif choice == "5":
            get_all_courses()
        elif choice == "6":
            get_degree_by_id()
        elif choice == "7":
            get_course_by_number()
        elif choice == "8":
            break
        elif choice == "9":
            delete_degree()
        elif choice == "10":
            delete_course()
        elif choice == "11":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()