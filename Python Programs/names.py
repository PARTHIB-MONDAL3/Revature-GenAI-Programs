def names():
    a=input("enter 5 names ").split()
    b=['a','e','i','o','u']
    for name in a:
        if name[0] in b:
            print(name)
names()        