from create_graph import CreateGraph

new_graph = CreateGraph()

data_filename = 'data.csv'

new_graph_data = new_graph.generate_population_dictionary(data_filename)

new_graph.display_graph(new_graph_data)
