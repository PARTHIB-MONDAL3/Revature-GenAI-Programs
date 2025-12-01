# Password program with max 3 attempts
correctpassword = "rishi"
attempts = 0

while attempts < 3:
    a = input("Enter password: ")
    if a == correctpassword:
        print("Login successful")
        break
    else:
        attempts += 1
        if attempts < 3:
            print("Incorrect password. Try again.")
        else:
            print("Number of attempts reached. Access denied.")
