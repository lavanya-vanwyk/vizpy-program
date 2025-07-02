import csv

with open('data.csv', mode='r') as file:
  csvFile = csv.DictReader(file)
  for lines in csvFile:

    continent = lines['continent']
    year = lines['year']
    population = lines['population']

    print(f'The population in {continent} in the year {year}, was {population} people!')