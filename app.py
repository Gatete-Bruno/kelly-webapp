import pymysql

def task_management_app(name):
    # Function to authenticate user credentials
    def authenticate():
        while True:
            username = input("Enter your username: ")
            pword = input('Enter your password: ')
            try:
                connection = pymysql.connect(host='localhost',
                                             user=username,
                                             password=pword,
                                             database=name,
                                             cursorclass=pymysql.cursors.DictCursor,
                                             autocommit=True)
                return connection
            except pymysql.Error as e:
                code, msg = e.args
                print("Cannot connect to the database", code, msg)

    # Function to display main menu options
    def display_menu():
        print("Main Menu:")
        print("1. Create Task")
        print("2. View Task")
        print("3. Update Task")
        print("4. Add Comment")
        print("5. View Comments")
        print("6. Delete Task")
        print("7. Exit")

    # Function to create a task
    def create_task(connection):
        print("Create Task:")
        task_name = input("Enter task name: ")
        task_description = input("Enter task description: ")
        task_due_date = input("Enter task due date (YYYY-MM-DD): ")

        # Display category options
        print("Available Categories: School, Work, Personal, Health and Fitness")
        category = input("Enter category: ")

        # Display priority options
        print("Available Priorities: High, Medium, Low")
        priority = input("Enter priority: ")

        # Display status options
        print("Available Status: Not started, In progress, Completed")
        status = input("Enter status: ")

        try:
            with connection.cursor() as cursor:
                cursor.callproc('CreateTask', (task_name, task_description, task_due_date, category, priority, status))
                print("Task created successfully!")
        except pymysql.Error as e:
            print("Error creating task:", e)

    # Function to view tasks by task name
    def view_task_by_name(connection):
        print("View Task by Name:")
        task_name = input("Enter task name: ")

        try:
            with connection.cursor() as cursor:
                cursor.callproc('GetTaskByName', (task_name,))
                result_set = cursor.fetchall()
                for row in result_set:
                    print(row)
        except pymysql.Error as e:
            print("Error fetching tasks by name:", e)

    # Function to view tasks by priority
    def view_task_by_priority(connection):
        print("View Task by Priority:")
        priority_name = input("Enter priority name: ")

        try:
            with connection.cursor() as cursor:
                cursor.callproc('GetTaskByPriority', (priority_name,))
                result_set = cursor.fetchall()
                for row in result_set:
                    print(row)
        except pymysql.Error as e:
            print("Error fetching tasks by priority:", e)

    # Function to update task status
    def update_task_status(connection):
        print("Update Task Status:")
        task_name = input("Enter task name to update: ")
        new_status = input("Enter new status: ")

        try:
            with connection.cursor() as cursor:
                cursor.callproc('UpdateTaskStatus', (task_name, new_status))
                print("Task status updated successfully!")
        except pymysql.Error as e:
            print("Error updating task status:", e)

    # Function to update task due date
    def update_task_due_date(connection):
        print("Update Task Due Date:")
        task_name = input("Enter task name to update: ")
        new_due_date = input("Enter new due date (YYYY-MM-DD): ")

        try:
            with connection.cursor() as cursor:
                cursor.callproc('UpdateTaskDueDate', (task_name, new_due_date))
                print("Task due date updated successfully!")
        except pymysql.Error as e:
            print("Error updating task due date:", e)

    # Function to add comment to task
    def add_comment(connection):
        print("Add Comment:")
        task_name = input("Enter task name: ")
        comment_text = input("Enter comment: ")

        try:
            with connection.cursor() as cursor:
                cursor.callproc('CreateTaskComment', (task_name, comment_text))
                print("Comment added successfully!")
        except pymysql.Error as e:
            print("Error adding comment:", e)

    # Function to view comments for task
    def view_comments(connection):
        print("View Comments:")
        task_name = input("Enter task name: ")

        try:
            with connection.cursor() as cursor:
                cursor.callproc('GetTaskComments', (task_name,))
                result_set = cursor.fetchall()
                for row in result_set:
                    print(row)
        except pymysql.Error as e:
            print("Error fetching comments:", e)

    # Function to delete task
    def delete_task(connection):
        print("Delete Task:")
        task_name = input("Enter task name to delete: ")

        try:
            with connection.cursor() as cursor:
                cursor.callproc('DeleteTask', (task_name,))
                print("Task deleted successfully!")
        except pymysql.Error as e:
            print("Error deleting task:", e)

    # Main application flow
    connection = authenticate()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            create_task(connection)
        elif choice == "2":
            print("View Task:")
            print("1. By Task Name")
            print("2. By Priority")
            view_choice = input("Enter your choice: ")
            if view_choice == "1":
                view_task_by_name(connection)
            elif view_choice == "2":
                view_task_by_priority(connection)
            else:
                print("Invalid choice. Please try again.")
        elif choice == "3":
            print("Update Task:")
            print("1. Update Task Status")
            print("2. Update Task Due Date")
            update_choice = input("Enter your choice: ")
            if update_choice == "1":
                update_task_status(connection)
            elif update_choice == "2":
                update_task_due_date(connection)
            else:
                print("Invalid choice. Please try again.")
        elif choice == "4":
            add_comment(connection)
        elif choice == "5":
            view_comments(connection)
        elif choice == "6":
            delete_task(connection)
        elif choice == "7":
            print("Exiting...")
            connection.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    task_management_app('task_management_db')