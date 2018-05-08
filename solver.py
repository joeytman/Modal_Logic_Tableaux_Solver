import networkx as nx
import modalparser
import modalgraph
import argparse
from enum import Enum



if __name == '__main__':
	parser = argparse.ArgumentParser(description='parsing arguments')
	parser.add_argument('formula', type=str, help='The formula to determine satisfiability of')
	args = parser.parse_args()
	formula = args.formula
	parsed_formula = modalparser.parse_formula()
	valid_solution_graphs = perform_graph_tableaux(parsed_formula)

""" Input: parsed formula in tuple prefix form
	Each graph world 
"""
def perform_graph_tableaux(parsed_formula):
	MG = ModalGraph()
	MG.add_node(parsed_formula)
	active_graphs = [MG]
	seen_graphs = [MG]
	while active_graphs:
		new_active_graphs = []
		new_active_graphs.extend(MG.process_all_worlds())
		seen_graphs += [new_graph for new_graph in new_active_graphs if new_graph not in seen_graphs]
		active_graphs = new_active_graphs
	valid_solution_graphs = []
	for graph in seen_graphs:
		if graph.is_fully_processed() and graph.is_consistent():
			valid_solution_graphs.add(graph)
	return valid_solution_graphs

