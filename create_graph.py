import csv
import matplotlib.pyplot as plt


class CreateGraph:

  def __init__(self):
    print("Initializing CreateGraph object...")

  def generate_population_dictionary(self, file_name='data.csv'):
    population_per_continent = {
    }  #init empty dictionary to populate with data read from csv
    file_name = 'data.csv'

    with open(file_name, mode='r') as file:
      csvFile = csv.DictReader(file)
      for lines in csvFile:

        continent = lines['continent']
        year = int(lines['year'])
        population = int(lines['population'])

        if continent not in population_per_continent:
          population_per_continent[continent] = {'population': [], 'years': []}

        population_per_continent[continent]['population'].append(population)
        population_per_continent[continent]['years'].append(year)
    return population_per_continent

  def display_graph(self, population_per_continent):
    for continent in population_per_continent:
      population = population_per_continent[continent][
          'population']  # loops through main_dict[continent key]['population' key]
      years = population_per_continent[continent][
          'years']  #loops through main_dict[continent key]['years' key]

      plt.plot(years, population, label=continent, marker=".", alpha=0.5)

    plt.title("Internet Population (per continent)")
    plt.xlabel("Year")
    plt.ylabel("Internet users (in millions)")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()
