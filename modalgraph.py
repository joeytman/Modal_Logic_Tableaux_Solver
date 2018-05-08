import networkx as nx
import modalparser
from modalparser import UnaryPred
from modalparser import BinaryPred
from enum import Enum

class ModalGraph():
	def __init__(self, data=None, MG=None):
		if MG:
			self.nxG = MG.copy()
			self.true_at_world = MG.set(true_at_world)
			self.false_at_world = MG.set(false_at_world)
			self.next_world_number = MG.next_world_number
			self.formulas = dict(MG.formulas)
			self.rules_for_children = dict(MG.rules_for_children)
			return self
		self.nxG = nx.DiGraph(data)
		self.true_at_world = {}
		self.false_at_world = {}
		self.next_world_number = 0
		self.formulas = dict()
		self.rules_for_children = dict()
		return self



	""" **attr is arbitrary atributes to add to node through networkx implementation.
		Here, we don't actually have a world name for adding a node, unlike nx default.
		Instead an integer is assigned to each world and the corresponding integer is returned
		upon the function's completion.
		Formula is a parsed prefix form tuple representation of the subformula remaining to be considered in the world
	"""
	def add_node(self, formula):
		world_number = self.next_world_number
		self.next_world_number += 1
		self.nxG.add_node(world_number)
		self.true_at_world[world_number] = {}
		self.false_at_world[world_number] = {}
		self.formulas[world_number] = [formula]
		self.rules_for_children[world_number] = []
		return world_number


	""" Sets an atomic proposition to True in the given world
		Returns true so long as the assignment is permissable
		Returns false if this cause a variable to be set to necessarily true and false
	"""
	def set_atom_true(self, world, atom):
		if world not in self.nodes(): raise KeyError("World " + str(world) + " is not a world")
		if atom in self.false_at_world[world]: return False
		true_at_world[world].add(atom)
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


	""" When called, processes all subformulas in all worlds until a new graph (or graphs) must be created
		When new graph(s) are created, the function returns a list of all graphs within its scope that need processing
		If an operation causes this graph to have a contradiction (e.g p ^ ~p) then its returned list will not include itself
		If it did not create any new graphs within this call, that will be an empty list
	"""
	def process_all_worlds(self):
		valid_graphs = [self]
		for world, world_formulas in self.formulas:
			for subformula in world_formulas:
				if isinstance(subformula, str): 
					# subformula at world is reduced to an atomic proposition that must be set to true
					graph_still_valid = self.set_atom_true(world, subformula)
					world_formulas.remove(subformula)
					if not graph_still_valid and self in valid_graphs:
						valid_graphs.remove(self)
				
				elif isinstance(subformula, tuple): #Operation(s) to process still
					operator = subformula[0]
					if operator == UnaryPred.NOT:
						action = self.handle_negation(subformula, world, world_formulas)
						action[0](self, world, world_formulas, subformula, valid_graphs, action[1])
					elif operator == UnaryPred.BOX:
						action = 

					elif operator == UnaryPred.DIAM:

					elif operator == BinaryPred.AND:

					elif operator == BinaryPred.OR:

					elif operator == BinaryPred.IMPL:

					else: raise ValueError("Operator " + str(operator) + " is not of a known type")
		return valid_graphs


	def handle_negation(self, subformula, world):
		arg = subformula[1]
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
				return (set_current_subformula, [arg[1]])
			elif nextop == UnaryPred.BOX:
				return (add_new_world_with_subformula, [(UnaryPred.NOT, arg[1])])
			elif nextop == UnaryPred.DIAM:
				return (enforce_formula_met_by_children, [(UnaryPred.NOT, arg[1])])

	def handle_box(self, subformula, world):
		return (enforce_formula_met_by_children, [subformula[1]])

	def __getitem__(self, world):
		return self.nodes[world]


def invalidate_graph(MG, world, world_formulas, subformula, valid_graphs, args):
	if MG in valid_graphs:
		valid_graphs.remove(MG)

def finished_subformula(MG, world, world_formulas, subformula, valid_graphs, args):
	world_formulas.remove(subformula)

def split_subformula_in_world(MG, world, world_formulas, subformula, valid_graphs, args):
	world_formulas.remove(subformula)
	world_formulas.add(args[0])
	world_formulas.add(args[1])

def split_formula_over_new_graph(MG, world, world_formulas, subformula, valid_graphs, args):
	world_formulas.remove(subformula)
	newMG = ModalGraph(MG=MG)
	world_formulas.add(args[0])
	newMG.formulas[world].add(args[1])

def set_current_subformula(MG, world, world_formulas, subformula, valid_graphs, args):
	world_formulas.remove(subformula)
	world_formulas.add(args[0])

def add_new_world_with_subformula(MG, world, world_formulas, subformula, valid_graphs, args):
	newworld = MG.add_node(args[0])
	MG.formulas[newworld].extend(MG.rules_for_children[world])
	MG.nxG.add_edge(world, newworld)


def enforce_formula_met_by_children(MG, world, world_formulas, subformula, valid_graphs, args):
	MG.rules_for_children[world].add(args[0])
	for child in [edge[1] for edge in MG.out_edges_iter(world)]:
		MG.formulas[child].add(args[0])


