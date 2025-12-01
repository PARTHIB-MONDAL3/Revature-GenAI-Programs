class Animals:
    def eat(self):
        print("animals eat")
class Birds:
    def fly(self):
        print("birds fly")
class A(Animals,Birds):
    def talk(self):
        print("both animals and birds talk")
a=A()
a.eat()
a.fly()
a.talk()    

                  

        