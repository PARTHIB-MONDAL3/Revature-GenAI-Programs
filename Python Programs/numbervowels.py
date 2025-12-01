def vowels():
    a=input("enter a string :")
    b=['a','e','i','o','u']
    count=0
    for char in a:
        if char in b:
            count+= 1
    print(count)
vowels()        


