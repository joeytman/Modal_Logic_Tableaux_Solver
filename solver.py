import networkx as nx
import modalparser
import argparse

if __name == '__main__':
	parser = argparse.ArgumentParser(description='parsing arguments')
	parser.add_argument('formula', type=str, help='The formula to determine satisfiability of')
	args = parser.parse_args()
	formula = args.formula
	parsed_formula = modalparser.parse_formula()

#Input: parsed formula in tuple form
def perform_graph_tableaux(parsed_formula):
	