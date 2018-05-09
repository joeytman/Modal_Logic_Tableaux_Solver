import networkx as nx
import modalparser
import modalgraph as mg
import argparse
from enum import Enum
import matplotlib.pyplot as plt



""" Input: parsed formula in tuple prefix form
	Each graph world 
"""
def perform_graph_tableaux(parsed_formula, params=[], debug=False):
	if debug: print("Searching for satisfying model for parsed formula: " + str(parsed_formula))
	MG = mg.ModalGraph(params=params, debug=debug)
	MG.add_node(parsed_formula)
	active_graphs = [MG]
	seen_graphs = [MG]
	while active_graphs != []:
		if debug: print("Processing " + str(len(active_graphs)) + " active graph(s)")
		new_active_graphs = []
		for graph in active_graphs:
			if debug: print("Processing graph: " + str(active_graphs.index(graph)))
			new_active_graphs.extend(graph.process_all_worlds())
			seen_graphs += [new_graph for new_graph in new_active_graphs if new_graph not in seen_graphs]
		active_graphs = new_active_graphs
	valid_solution_graphs = []
	for graph in seen_graphs:
		if graph.is_fully_processed() and graph.is_consistent():
			valid_solution_graphs.append(graph)
	print("Finished processing formula, generated " + str(len(valid_solution_graphs)) + " valid graph(s) and generated " + str(len(seen_graphs) - len(valid_solution_graphs)) + " invalid graph(s)")
	return valid_solution_graphs




if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='parsing arguments')
	parser.add_argument('formula', type=str, help='The formula to determine satisfiability of')
	parser.add_argument('--debug', action='store_true', help='If specified, verbose output will be printed to console throughout processing')
	parser.add_argument('--novis', action='store_true', help='If specified, will  not visualize satisfying graphs discovered')
	parser.add_argument('params', nargs=argparse.REMAINDER, help='Specify any combination of "reflexive", "symmetric", "transitive" to impose them as frame constraints (space separated)')
	args = parser.parse_args()
	formula = args.formula
	parsed_formula = modalparser.parse_formula(formula)
	if args.params: print("Determining satisfiability for '" + formula + "' on frames that are: " + " ".join(args.params))
	else: print("Determining satisfiability for '" + formula + "'")
	valid_solution_graphs = perform_graph_tableaux(parsed_formula, args.params, args.debug)
	if not valid_solution_graphs:
		print("The given formula '" + args.formula + "' is unsatisfiable")
	else:
		for sol_graph in valid_solution_graphs:
			plt.figure(valid_solution_graphs.index(sol_graph))
			sol_graph.visualize(plt)
		if not args.novis: plt.show()	
		else: print("The given formula '" + args.formula + "' is satisfiable")