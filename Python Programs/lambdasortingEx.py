employees=[
    {"name":"alice","salary":50000},{"name":"rishi","salary":60000},{"name":"charlie","salary":40000}]
sortedemployees=sorted(employees,key=lambda x:(x["salary"],x["name"]))
print(sortedemployees)