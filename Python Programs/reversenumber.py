def reversenumber():
    a = int(input("Enter a number: "))
    b = 0  # this will store the reversed number
    temp = a  # temporary variable to manipulate

    while temp > 0:
        digit = temp % 10
        b = b * 10 + digit
        temp = temp // 10

    print("Reversed number:", b)

reversenumber()
