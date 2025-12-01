def primenumber(): # define function
    for a in range(start,end):  # giving range
         if a>1:
            for i in range(2,a): #hecking range from 2-100
                if a%i==0:
                    break
            else: # printing the prime numbers from 2 -100
                print(a ,end=", ")
start=int(input("enter start number"))
end=int(input("enter end number"))
primenumber() #calling the function

                