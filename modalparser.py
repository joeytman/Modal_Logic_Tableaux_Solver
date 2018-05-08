from enum import Enum
from string import ascii_lowercase

class UnaryPred(Enum):
	NOT = '~'
	BOX = 'B'
	DIAM = 'D'

class BinaryPred(Enum):
	AND = '&'
	OR = '|'
	IMPL = '>'

class Language:
	def __init__(self):
		self.atoms = {ascii_lowercase[char] for char in range(26)} # characters 'a' through 'z'
		self.unaryPreds = {item.value for item in UnaryPred} # Unary predicates NOT, BOX, and DIAMOND
		self.binaryPreds = {item.value for item in BinaryPred} # Binary predicates AND, OR, and IMPLIES
		self.brackets = {('(', ')'), ('[',']'), ('{','}')} # Accepted brackets for scoping

	def __getitem__(self, symbol):
		if symbol in self.unaryPreds:
			return UnaryPred(symbol)
		elif symbol in self.binaryPreds:
			return BinaryPred(symbol)
		elif symbol in self.atoms \
		or symbol in {pair[0] for pair in self.brackets} \
		or symbol in {pair[1] for pair in self.brackets}:
			return symbol
		return None

def parse_formula(formula, debug=False):
	formula = convert_for_aliases(formula)
	return list_to_tuple(parse_into_list(formula, debug))

def parse_into_list(formula, debug=False):
	if debug: print("Parsing " + formula)
	# Remove whitespace
	formula = ''.join(formula.split())
	parsed_formula = []

	# if formula is atomic return it
	if len(formula) == 1:
		syntax_check(need_one_to_pass=[formula in L.atoms])
		if debug: print("Reached atomic symbol " + formula)
		return L[formula]

	# Deal with formula by splitting it and generating subformulas.
	partition = [[]]
	bracket_list = []
	i = 0 #Index of current subformula.
	for part in formula:
		if debug: print("Considering '" + part + "'")
		partition[i].append(part) #Adds the current symbol to the current partition
		if part in {pair[0] for pair in L.brackets}: #If it's an open bracket, track it
			bracket_list.append(part)
		elif part in {pair[1] for pair in L.brackets}: #If it's a closed bracket
			#Ensure that this is validly losing an open bracket
			syntax_check(need_one_to_pass=[(bracket_list[-1], part) in L.brackets], show_with_error='Brackets are formed incorrectly')
			bracket_list.pop() #Get rid of the tracked open bracket that was just closed
			if bracket_list == []: #If this was the last bracket to close then this partition is done
				i = i + 1
				partition.append([]) #New partition
		elif bracket_list == []: #If there are no brackets being tracked, 
			#Then if the symbol is a proposition or a binary predicate, partition after this symbol
			if part in L.atoms or \
			   part in L.binaryPreds:
				i = i + 1
				partition.append([])
	
	partition = partition[:-1] #The above loop always adds an extra list for another proposition at the end
	if debug: print("After first loop, partitioned " + formula + " into " + str(partition))
	if len(partition) == 1: #The formula's scope is only over a single subformula
		first_symbol = partition[0][0]
		#If there is only one partition, then the first symbol has to be either a bracket or a unary pred
		syntax_check(need_one_to_pass=[(first_symbol, partition[0][-1]) in L.brackets, first_symbol in L.unaryPreds])
		if (first_symbol, partition[0][-1]) in L.brackets:
			#Recursively parse the formula without the brackets
			parsed_formula = parse_into_list(formula[1:-1], debug)
		else: 
			#This must be a unary predicate
			parsed_formula = [L[first_symbol], parse_into_list(formula[1:], debug)]
	else: #There are multiple subformulas partitioned here
		for sub in partition: 
			if (len(sub) == 1 and
				sub[0] in L.binaryPreds):
				parsed_formula = \
				[L[sub[0]]] + [parse_into_list(''.join(form), debug) for form in partition if form[0] is not sub[0]]
			#From the structure of this parser, any two-place predicates will create three partitions
			#For instance, Bp ^ Dq will make [[B, p], [^], [D, q]]
			#Hence, we want to parse this by moving the operator to the beginning and then 
	return parsed_formula

def list_to_tuple(format):
	formtype = type(format)
	if formtype == list:
		return tuple(list_to_tuple(sub) for sub in format)
	syntax_check(need_one_to_pass=[formtype == str, formtype == tuple, formtype == UnaryPred, formtype == BinaryPred], 
		show_with_error='Wrong type for ' + str(format))
	return format

def syntax_check(show_with_error='', need_all_to_pass=None, need_one_to_pass=None):
	if need_one_to_pass:
		for item in need_one_to_pass:
			if item:
				return True
		raise SyntaxError("Given formula is incorrectly formatted: " + show_with_error)
	if need_all_to_pass:
		for item in need_all_to_pass:
			if not item:
				raise SyntaxError("Given formula is incorrectly formatted: " + show_with_error)

def convert_for_aliases(format):
	for ind in range(len(format)):
		if format[ind] == '^':
			return convert_for_aliases(format[:ind] + '&' + format[ind + 1:])
		if ind != len(format) - 1 and format[ind] == '[' and format[ind + 1] == ']':
			return convert_for_aliases(format[:ind] + 'B' + format[ind + 2:])
		if ind != len(format) - 1 and format[ind] == '<' and format[ind + 1] == '>':
			return convert_for_aliases(format[:ind] + 'D' + format[ind + 2:])
	return format

#Prints a parsed formula in prefix form with all strings 
#e.g. (BinaryPred.AND: '&', 'p', 'q') --> (&, p, q)
def readable_prefix_form(formula, debug=False):
	syntax_check(need_one_to_pass=[type(formula) == tuple], show_with_error="Attempting to print tuple that isn't a tuple")
	if formula == (): return
	first = formula[0]
	rest = readable_prefix_form(formula[1:], debug)
	if type(first) == str:
		return (first, rest) if rest != None else first
	elif isinstance(first, Enum):
		return (first.value, rest) if rest != None else first.value
	elif isinstance(first, tuple):
		readablefirst = readable_prefix_form(first, debug)
		return (readablefirst, rest) if rest != None else readablefirst

#Prints a parsed formula in natural form, as in the way it would be input to the program
def readable_natural_form(formula, debug=False):
	syntax_check(need_one_to_pass=[type(formula) == tuple, type(formula) == str, type(formula) == Enum], show_with_error="Attempting to print tuple that isn't a tuple")
	first = formula[0]
	if debug: print("Parsing " + str(formula) + "\nFirst=" + str(first))
	if first in L.atoms:
		return first
	if isinstance(first, UnaryPred): #Operator on single variable
		first_symbol = first.value
		if first.value == "B": first_symbol = '[]'
		if first.value == "D": first_symbol = '<>'
		return first_symbol + readable_natural_form(formula[1], debug)
	if isinstance(first, BinaryPred):
		return "(" + readable_natural_form(formula[1], debug) + " " + first.value + " " + readable_natural_form(formula[2], debug) + ")"

L = Language()
