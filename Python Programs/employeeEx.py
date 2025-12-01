class Employee:
    def __init__(self, name, emp_id, salary):
        self.name = name
        self.emp_id = emp_id
        self.salary = salary

    def show(self):
        print("Name:", self.name, "| ID:", self.emp_id, "| Salary:", self.salary)

class Manager(Employee):
    def __init__(self, name, emp_id, salary, dept):
        super().__init__(name, emp_id, salary)
        self.dept = dept

    def show(self):
        print("Manager:", self.name, "| ID:", self.emp_id, "| Dept:", self.dept, "| Salary:", self.salary)

class HR:
    def __init__(self):
        self.list = []

    def add(self, emp):
        self.list.append(emp)
        print("Employee added!")

    def show_all(self):
        print("\n Employee List ")
        for e in self.list:
            e.show()

# main
hr = HR()

while True:
    print("\n1. Add Employee")
    print("2. Add Manager")
    print("3. Show All")
    print("4. Exit")

    ch = input("Enter choice: ")

    if ch == "1":
        n = input("Name: ")
        i = input("ID: ")
        s = input("Salary: ")
        e = Employee(n, i, s)
        hr.add(e)

    elif ch == "2":
        n = input("Name: ")
        i = input("ID: ")
        s = input("Salary: ")
        d = input("Dept: ")
        m = Manager(n, i, s, d)
        hr.add(m)

    elif ch == "3":
        hr.show_all()

    elif ch == "4":
        print("Exit done")
        break

    else:
        print("Invalid choice")
       


