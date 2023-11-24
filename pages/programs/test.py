import csv

route = "C:\\Users\\ST\\Documents\\CHAPINGO\\PYTHON TAREAS\\esalgo.csv"
#route = fr"{route}"
#print(route)

data = []

with open(route, "r", newline="", encoding="utf-8") as file:
    table = csv.reader(file)
    
    for row in table:
        new_row = [str(x) for x in row]
        data.append(new_row)
        
print(data)