import json


class Employee:
    def __init__(self, name, emp_id, title, department):
        self._name = name
        self._emp_id = emp_id
        self._title = title
        self._department = department

    def display_details(self):
        print(f"Name: {self._name}")
        print(f"ID: {self._emp_id}")
        print(f"Title: {self._title}")
        print(f"Department: {self._department}")

    def __str__(self):
        return f"{self._name} - ID: {self._emp_id}"


class Department:
    def __init__(self, name):
        self._name = name
        self._employees = []

    @property
    def name(self):
        return self._name

    def add_employee(self, employee):
        self._employees.append(employee)

    def remove_employee(self, emp_id):
        for employee in self._employees:
            if employee._emp_id == emp_id:
                self._employees.remove(employee)
                return True
        return False

    def list_employees(self):
        for employee in self._employees:
            print(employee)


class Company:
    def __init__(self):
        self._departments = {}

    def add_department(self, department):
        self._departments[department.name] = department

    def remove_department(self, department_name):
        if department_name in self._departments:
            del self._departments[department_name]
            return True
        return False

    def display_departments(self):
        for department in self._departments.values():
            print(f"Department: {department.name}")
            department.list_employees()
            print()


def print_menu():
    print("Employee Management System Menu:")
    print("1. Add Employee")
    print("2. Remove Employee")
    print("3. Add Department")
    print("4. Remove Department")
    print("5. Display Departments")
    print("6. Exit")


def save_company_data(company):
    with open('company_data.json', 'w') as f:
        json.dump(company._departments, f, default=lambda o: o.__dict__, indent=4)


def load_company_data():
    try:
        with open('company_data.json', 'r') as f:
            data = json.load(f)
            company = Company()
            for department_name, department_data in data.items():
                department = Department(department_name)
                for emp_data in department_data['_employees']:
                    employee = Employee(emp_data['_name'], emp_data['_emp_id'], emp_data['_title'],
                                        emp_data['_department'])
                    department.add_employee(employee)
                company.add_department(department)
            return company
    except FileNotFoundError:
        return Company()


def main():
    company = load_company_data()

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter employee name: ")
            emp_id = input("Enter employee ID: ")
            title = input("Enter employee title: ")
            department = input("Enter department name: ")

            if department in company._departments:
                employee = Employee(name, emp_id, title, department)
                company._departments[department].add_employee(employee)
                print("Employee added successfully.")
            else:
                print("Department does not exist.")

        elif choice == '2':
            emp_id = input("Enter employee ID to remove: ")
            for department in company._departments.values():
                if department.remove_employee(emp_id):
                    print("Employee removed successfully.")
                    break
            else:
                print("Employee not found.")

        elif choice == '3':
            department_name = input("Enter department name: ")
            department = Department(department_name)
            company.add_department(department)
            print("Department added successfully.")

        elif choice == '4':
            department_name = input("Enter department name to remove: ")
            if company.remove_department(department_name):
                print("Department removed successfully.")
            else:
                print("Department not found.")

        elif choice == '5':
            company.display_departments()

        elif choice == '6':
            save_company_data(company)
            print("Data saved to company_data.json.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
