a = open("customers-100.csv", "r")
count = 0
while True:
    line = a.readline()
    if not line:
        break
    count = count + 1
a.close()
print("Total customers:", count)
