# Print numbers between 1 and 100 divisible by 3 or 5 but not both
for i in range(1, 100):
    if (i % 3 == 0) != (i % 5 == 0):  # XOR logic
        print(i, end=", ")
