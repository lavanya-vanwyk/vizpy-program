import csv
import matplotlib.pyplot as plt

population_per_continent = {}

with open('data.csv', mode='r') as file:
  csvFile = csv.DictReader(file)
  for lines in csvFile:

    continent = lines['continent']
    year = lines['year']
    population = lines['population']

    if continent not in population_per_continent:
      population_per_continent[continent] = {'population': [], 'years': []}

    population_per_continent[continent]['population'].append(population)
    population_per_continent[continent]['years'].append(year)

print(population_per_continent)