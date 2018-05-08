import networkx as nx
import modalparser

class ModalGraph(nx.DiGraph):
	def __init__(self, data=None):
		nx.DiGraph.__init__(self, data)
		self.true_at_world = {}
		self.false_at_world = {}
		self.nextworldnumber = 0

	"""
		**attr is arbitrary atributes to add to node through networkx implementation.
		Here, we don't actually have a world name for adding a node, unlike nx default.
		Instead an integer is assigned to each world and the corresponding integer is returned
		upon the function's completion.
	"""
	def add_node(self, **attr):
		super().add_node(nextworldnumber, attr)
		self.true_at_world[node_for_adding] = {}
		self.false_at_world[node_for_adding] = {}
		nextworldnumber+= 1
		return nextworldnumber - 1

	"""
		Sets an atomic proposition to True in the given world
		Returns true so long as the assignment is permissable
		Returns false if this cause a variable to be set to necessarily true and false
	"""
	def set_atom_true(self, world, atom):
		if world not in self.nodes(): raise KeyError("World " + str(world) + " is not a world")
		if atom in self.false_at_world[world]: return False
		true_at_world[world].add(atom)
		return True

	"""
		Sets an atomic proposition to True in the given world
		Returns true so long as the assignment is permissable
		Returns false if this cause a variable to be set to necessarily true and false
	"""
	def set_atom_false(self, world, atom):
		if world not in self.nodes(): raise KeyError("World " + str(world) + " is not a world")
		if atom in self.true_at_world[world]: return False
		false_at_world[world].add(atom)
		return True

	def __getitem__(self, world):
		return self.nodes[world]
