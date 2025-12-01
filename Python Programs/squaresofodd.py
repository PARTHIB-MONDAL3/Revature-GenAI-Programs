#Using a for loop, generate a list ofsquares of only the odd numbers from 1 to 20.
def oddsquare():
    for i in range(1,20):
        if i % 2 != 0:
            print(i*i)
oddsquare()            