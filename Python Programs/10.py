file = open("hello.txt", "r")

for line in file:
    if "python" in line.lower():
        print(line.strip())

file.close()
