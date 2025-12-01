# Ask how many students
n = int(input("Enter number of students: "))
choice=1
# Collect each student's name and score
students = []
while choice != -1:


    name = input("Enter student name: ")
    score = int(input("Enter student score: "))
    students.append((name, score))
    choice = int(input("Do you want to continue? (-1 to exit, any other number to continue): ")) 

# Find the student with the highest score using lambda
topper = max(students, key=lambda x: x[1])

# Display the result
print("Topper:", topper[0])
print("Score:", topper[1])
