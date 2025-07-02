import csv
import matplotlib.pyplot as plt


population_per_continent = {
}  #init empty dictionary to populate with data read from csv

with open('data.csv', mode='r') as file:
  csvFile = csv.DictReader(file)
  for lines in csvFile:

    continent = lines['continent']
    year = int(lines['year'])
    population = int(lines['population'])

    if continent not in population_per_continent:
      population_per_continent[continent] = {
          'population': [],
          'years': []
      }  #creates dictionary with key-values pairs containing lists

    population_per_continent[continent]['population'].append(
        population)  #adds population data into the 'population' value list
    population_per_continent[continent]['years'].append(
        year)  #adds year data into the 'years' value list

  for continent in population_per_continent:
    population = population_per_continent[continent][
        'population']  # loops through main_dict[continent key]['population' key]
    years = population_per_continent[continent][
        'years']  #loops through main_dict[continent key]['years' key]
    plt.plot(years, population, label=continent, marker=".", alpha=0.5)

plt.title("Internet Population per continent")
plt.xlabel("Year")
plt.ylabel("Internet users (in millions)")
plt.grid(True)
plt.show()
