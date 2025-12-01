# Correct version
marks = input("Enter marks separated by space: ").split()  # split input into list of strings
marks = [int(mark) for mark in marks]  # convert each string to integer

pass_all = True

for mark in marks:
    if mark <= 40:
        pass_all = False
        break

if pass_all:
    print("Pass")
else:
    print("Fail")
