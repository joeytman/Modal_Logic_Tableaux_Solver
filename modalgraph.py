import networkx as nx
import modalparser
from modalparser import UnaryPred
from modalparser import BinaryPred
from enum import Enum
import copy

class ModalGraph():
	def __init__(self, params=[], data=None, MG=None, next_formulas=None, debug=False):
		if 'r' in params:
			self.reflexive = True
		else:
			self.reflexive = False
		if MG:
			self.nxG = MG.nxG.copy()
			self.true_at_world = copy.deepcopy(MG.true_at_world)
			self.false_at_world = copy.deepcopy(MG.false_at_world)
			self.next_world_number = MG.next_world_number
			self.formulas = copy.deepcopy(next_formulas)
			self.rules_for_children = copy.deepcopy(MG.rules_for_children)
			self.debug = MG.debug
			return
		self.nxG = nx.DiGraph(data)
		self.true_at_world = dict()
		self.false_at_world = dict()
		self.next_world_number = 0
		self.formulas = dict()
		self.rules_for_children = dict()
		self.debug = debug



	""" **attr is arbitrary atributes to add to node through networkx implementation.
		Here, we don't actually have a world name for adding a node, unlike nx default.
		Instead an integer is assigned to each world and the corresponding integer is returned
		upon the function's completion.
		Formula is a parsed prefix form tuple representation of the subformula remaining to be considered in the world
	"""
	def add_node(self, formula, next_formulas=None):
		world_number = self.next_world_number
		self.next_world_number += 1
		self.nxG.add_node(world_number)
		self.true_at_world[world_number] = set()
		self.false_at_world[world_number] = set()
		if next_formulas: 
			next_formulas[world_number] = [formula]
		else: self.formulas[world_number] = [formula]
		self.rules_for_children[world_number] = []
		if self.reflexive:
			self.nxG.add_edge(world_number, world_number)
		return world_number


	""" Sets an atomic proposition to True in the given world
		Returns true so long as the assignment is permissable
		Returns false if this cause a variable to be set to necessarily true and false
	"""
	def set_atom_true(self, world, atom):
		if world not in self.nxG.nodes(): raise KeyError("World " + str(world) + " is not a world")
		if atom in self.false_at_world[world]: return False
		self.true_at_world[world].add(atom)
		return True

	""" Sets an atomic proposition to True in the given world
		Returns true so long as the assignment is permissable
		Returns false if this cause a variable to be set to necessarily true and false
	"""
	def set_atom_false(self, world, atom):
		if world not in self.nodes(): raise KeyError("World " + str(world) + " is not a world")
		if atom in self.true_at_world[world]: return False
		false_at_world[world].add(atom)
		return True

	""" Returns true if all formulas in all worlds have been processed and have had values assigned
	"""
	def is_fully_processed(self):
		return [True for world, formulas in self.formulas.items() if len(formulas) != 0] == []

	def is_consistent(self):
		return [atom not in [self.false_at_world[world] for world in range(self.next_world_number)] for atom in [self.true_at_world[world] for world in range(self.next_world_number)]]


	""" When called, processes all subformulas in all worlds until a new graph (or graphs) must be created
		When new graph(s) are created, the function returns a list of all graphs within its scope that need processing
		If an operation causes this graph to have a contradiction (e.g p ^ ~p) then its returned list will not include itself
		If it did not create any new graphs within this call, that will be an empty list
	"""
	def process_all_worlds(self):
		active_graphs = [self]
		next_formulas = {i:[] for i in range(self.next_world_number)}
		for world, world_formulas in self.formulas.items():
			if self.debug: print("Processing world " + str(world) + " with world formulas " + str(world_formulas))
			for subformula in world_formulas:
				if self.debug: print("Processing subformula " + str(modalparser.readable_natural_form(subformula)))
				if isinstance(subformula, str): 
					# subformula at world is reduced to an atomic proposition that must be set to true
					if self.debug: print("Setting " + subformula + " True")
					graph_still_valid = self.set_atom_true(world, subformula)
					if not graph_still_valid and self in active_graphs:
						if self.debug: print("This invalidated the graph so it has been removed")
						active_graphs.remove(self)
				
				elif isinstance(subformula, tuple): #Operation(s) to process still
					operator = subformula[0]
					if operator == UnaryPred.NOT: action = self.handle_negation(subformula, world)
					elif operator == UnaryPred.BOX: action = self.handle_box(subformula, world)
					elif operator == UnaryPred.DIAM: action = self.handle_diamond(subformula, world)
					elif operator == BinaryPred.AND: action = self.handle_and(subformula, world)
					elif operator == BinaryPred.OR: action = self.handle_or(subformula, world)
					elif operator == BinaryPred.IMPL: action = self.handle_implication(subformula, world)
					else: raise ValueError("Operator " + str(operator) + " is not of a known type")
					action[0](self, world, next_formulas, subformula, active_graphs, action[1])

				else: 
					raise ValueError("Subformula " + str(subformula) + " is not of a known type")
			
			if self not in active_graphs: 
				return active_graphs
		self.formulas = next_formulas
		if self.is_fully_processed(): active_graphs.remove(self)
		return active_graphs


	def handle_negation(self, subformula, world):
		arg = subformula[1]
		if self.debug: print("Handling negation of " + str(arg))
		if isinstance(arg, str):
			#Negating atomic proposition
			graph_still_valid =  self.set_atom_false(world, arg)
			if not graph_still_valid: return (invalidate_graph, None)
			else: return (finished_subformula, None)
		elif isinstance(arg, tuple):
			#Negating subformula
			nextop = arg[0]
			if nextop == BinaryPred.IMPL:
				return (split_subformula_in_world, [arg[1], (UnaryPred.NOT, arg[2])])
			elif nextop == BinaryPred.OR:
				return (split_subformula_in_world, [(UnaryPred.NOT, arg[1]), (UnaryPred.NOT, arg[2])])
			elif nextop == BinaryPred.AND:
				return (split_formula_over_new_graph, [(UnaryPred.NOT, arg[1]), (UnaryPred.NOT, arg[2])])
			elif nextop == UnaryPred.NOT:
				return (replace_current_subformula, [arg[1]])
			elif nextop == UnaryPred.BOX:
				return (add_new_world_with_subformula, [(UnaryPred.NOT, arg[1])])
			elif nextop == UnaryPred.DIAM:
				return (enforce_formula_met_by_children, [(UnaryPred.NOT, arg[1])])

	def handle_box(self, subformula, world):
		if self.debug: print("Handling box of " + str(modalparser.readable_natural_form(subformula[1])))
		return (enforce_formula_met_by_children, [subformula[1]])

	def handle_diamond(self, subformula, world):
		if self.debug: print("Handling diamond of " + str(subformula[1]))
		return (add_new_world_with_subformula, [subformula[1]])

	def handle_and(self, subformula, world):
		if self.debug: print("Handling conjunction of " + str(modalparser.readable_natural_form(subformula[1])) + " and " + str(modalparser.readable_natural_form(subformula[2])))
		phi = subformula[1]
		psi = subformula[2]
		return (split_subformula_in_world, [phi, psi])

	def handle_or(self, subformula, world):
		if self.debug: print("Handling disjunction of " + str(modalparser.readable_natural_form(subformula[1])) + " and " + str(modalparser.readable_natural_form(subformula[2])))
		phi = subformula[1]
		psi = subformula[2]
		return (split_formula_over_new_graph, [phi, psi])

	def handle_implication(self, subformula, world):
		if self.debug: print("Handling implication of " + str(modalparser.readable_natural_form(subformula[1])) + " and " + str(modalparser.readable_natural_form(subformula[2])))
		phi = (UnaryPred.NOT, subformula[1])
		psi = subformula[2]
		return (split_formula_over_new_graph, [phi, psi])

	def __getitem__(self, world):
		return self.nodes[world]

	def visualize(self, plt, node_size=1000):
		nxG = self.nxG
		true_vars = self.true_at_world
		labels = {}
		for node in range(self.next_world_number):
			node_label = ""
			if self.true_at_world[node]:
				node_label = ", ".join(self.true_at_world[node])
			labels[node] = node_label

		
		pos = nx.spring_layout(self.nxG)

		node_coloring = ['#999999'] * len(nxG.nodes()) #Grey
		node_coloring[0] = '#67ff59'

		nx.draw_networkx_labels(nxG, pos, labels)
		nx.draw_networkx_nodes(nxG, pos, node_size=node_size, node_color=node_coloring)
		nx.draw_networkx_edges(nxG, pos, node_size=node_size, edge_color='k', arrowsize=30, arrows=True)
		plt.axis('off')


def invalidate_graph(MG, world, next_formulas, subformula, active_graphs, args):
	if MG.debug: print("Invalidating graph due to contradiction")
	if MG in active_graphs:
		active_graphs.remove(MG)

def finished_subformula(MG, world, next_formulas, subformula, active_graphs, args):
	if MG.debug: print("Finished processing subformula " + modalparser.readable_natural_form(subformula))
	

def split_subformula_in_world(MG, world, next_formulas, subformula, active_graphs, args):
	if MG.debug: print("Splitting subformula within world from " + modalparser.readable_natural_form(subformula) + " to " + modalparser.readable_natural_form(args[0]) + " and " + modalparser.readable_natural_form(args[1]))
	next_formulas[world].append(args[0])
	next_formulas[world].append(args[1])

def split_formula_over_new_graph(MG, world, next_formulas, subformula, active_graphs, args):
	if MG.debug: print("Splitting subformula over new graph from " + modalparser.readable_natural_form(subformula) + " to " + modalparser.readable_natural_form(args[0]) + " and " + modalparser.readable_natural_form(args[1]))
	newMG = ModalGraph(MG=MG, next_formulas=next_formulas)
	next_formulas[world].append(args[0])
	newMG.formulas[world].append(args[1])
	active_graphs.append(newMG)
	if MG.debug: print("After split, original graph kept formula " + modalparser.readable_natural_form(next_formulas[world][-1]) + " and new graph handles formula " + modalparser.readable_natural_form(newMG.formulas[world][-1]))

def replace_current_subformula(MG, world, next_formulas, subformula, active_graphs, args):
	if MG.debug: print("Replacing current subformula " + modalparser.readable_natural_form(subformula) + " in world with " + str(args[0]))
	next_formulas[world].append(args[0])

def add_new_world_with_subformula(MG, world, next_formulas, subformula, active_graphs, args):
	if MG.debug: print("Adding a new world with formula " + str(args[0]))
	newworld = MG.add_node(args[0], next_formulas)
	next_formulas[newworld].extend(MG.rules_for_children[world])
	MG.nxG.add_edge(world, newworld)

def enforce_formula_met_by_children(MG, world, next_formulas, subformula, active_graphs, args):
	if MG.debug: print("Adding a new enforcement rule " + str(args[0]) + " to world " + str(world))
	MG.rules_for_children[world].append(args[0])
	for child in [edge[1] for edge in MG.nxG.out_edges(world)]:
		if MG.debug: print("Applied new enforcement rule to child " + str(child))
		next_formulas[child].append(args[0])


