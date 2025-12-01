class Opn:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def details(self):
        return f"Name: {self.name}, Age: {self.age}"


class Ug(Opn):
    def __init__(self, name, age, course):
        super().__init__(name, age)   # Call parent constructor
        self.course = course

    def coursedetails(self):
        return f"{self.details()}, Course: {self.course}"


# ---- Main Code ----
name = input("Enter name: ")
age = int(input("Enter age: "))
course = input("Enter your course: ")

student = Ug(name, age, course)  # Create UG object
print(student.coursedetails())

