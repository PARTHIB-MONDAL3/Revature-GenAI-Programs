f = open("data.txt", "r")
nums = f.read().split()
f.close()

sum = 0
for n in nums:
    if int(n) % 2 == 0:
        sum = sum + int(n)

print("Sum of even numbers:", sum)
