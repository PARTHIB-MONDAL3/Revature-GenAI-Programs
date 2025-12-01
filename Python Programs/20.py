f = open("numbers1.txt", "w")
even = 0
odd = 0

while True:
    n = input("Enter a number (type STOP to end): ")
    if n == "STOP":
        break
    n = int(n)
    f.write(str(n) + "\n")
    if n % 2 == 0:
        even += 1
    else:
        odd += 1

f.close()

print("Even numbers:", even)
print("Odd numbers:", odd)
