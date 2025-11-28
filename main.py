import csv

def athletes():
    with open("athletes.csv", 'r') as file:
        csvreader = csv.reader(file)
        
        for row in csvreader:
            print(row)

