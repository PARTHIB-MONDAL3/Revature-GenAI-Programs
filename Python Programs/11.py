'''Create a program that counts how many
lines, words, and characters exist in a text file.'''

a=open("prog.txt",'r')
b=a.read()
lines=b.split('\n')
words=b.split()
char=len(b)
print("lines",len(lines))
print("words",len(words))
print(char)
