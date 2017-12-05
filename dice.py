from sympy import *
init_printing(use_unicode=True)

### Variable Declarations ###
DIE_SIDES = 20 # The number of sides on each of the two dice to be relabeled
x, y, z = symbols('x y z')


# Admittingly don't understand quite how this function works as of this point
def partition(collection):
    """Function to yield a generator for every possible partition of the elements of `collection`"""
    # Check for full recursion depth
    if len(collection) == 1:
        yield [ collection ]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        # We have 2 possible options: insert the first element into each subset, or create a new subset
        # Case: insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # Case: put `first` in its own subset 
        yield [ [ first ] ] + smaller

def convert_to_factors(die):
    """Converts a sympy factor_list tuple to a list of the factors and returns the list"""
    sub_list = die[1] # Create a list from the tuple
    factor_list = []
    for i in sub_list: # Iterate through the `sub_list` which contains all the factors
        for j in range(i[1]): # Nesting checks the power of each factor and puts it in multiple times
            factor_list.append(i[0]) # The factor is stored in the first element of a tuple in each `sub_list` element

    return factor_list

def check_partition(partition_to_check):
    """A function to check a list of expressions, `partition`, to see if it is a valid die labeling. Returns boolean"""
    # Right now we only care about two dice relabelings, so get rid of anything else
    if (len(partition_to_check)!=2):
        return False
    # `partition` contains two lists, each represent a factor
    sub_list_one = partition_to_check[0]
    sub_list_two = partition_to_check[1]

    factor_one = expand_partition_factor(sub_list_one) # Convert the lists into sympy expressions for the factors
    factor_two = expand_partition_factor(sub_list_two)

    # Check for negative sides
    poly_factor_one = Poly(factor_one, x)
    poly_factor_two = Poly(factor_two, x)
    for coefficient in poly_factor_one.coeffs():
        if coefficient<0:
            return False
    for coefficient in poly_factor_two.coeffs():
        if coefficient<0:
            return False

    # Check for constant terms so that we don't have 0 sides
    if ( (factor_one.evalf(subs={x: 0}) == 1) or (factor_two.evalf(subs={x: 0}) == 1) ):
        return False

    # Check if each factor has `DIE_SIDES` terms by evaluating at 1
    if ( (factor_one.evalf(subs={x: 1}) != DIE_SIDES) or (factor_two.evalf(subs={x: 1}) != DIE_SIDES) ):
        return False

    return True

def expand_partition_factor(sub_list):
    """A function to return a sympy expression based on the mutiplication of elements in `sub_list`"""
    factor = "" # Initialize the factors to something that we can multiply onto
    for i in sub_list:
        factor += "("+str(i)+")" # Wrap in parentheses to avoid parsing multiplication incorrectly
        factor += "*" # Everything in the list is multiplied together
    factor = factor[:-1] # Strip last character for extra multiplication symbol
    return sympify(factor) # Convert to sympy expression before returning

def remove_duplicates(partition_list):
    """A function to remove the duplicates from a list, `partition_list`, and return the resulting list"""
    filtered_list = []
    for i in partition_list:
        swapped = [i[1], i[0]] # TODO improve later, for 2 dice structures we can do this direct swap check though
        if (i not in filtered_list) and (swapped not in filtered_list):
            filtered_list.append(i)
    return filtered_list

def make_distribution(sides):
    """A function to return a sympy expression representing the probability distribution of rolling 2 dice with `sides` sides"""
    str_expression = "(" # Initialize with a parentheses so that we can add squared at the end
    for i in range(sides):
        str_expression += "x**"+str(i+1)+"+" # i+1 is because range is 0 indexed
    str_expression = str_expression[:-1] # Strip last character for extra addition symbol
    str_expression += ")**2" # End the starting parentheses and finished with squared for two dice
    return factor_list(expand(sympify(str_expression))) # Sympify turns string into expression


# Create the initial distribution and convert it to a usable form
dice = make_distribution(DIE_SIDES)
die_factor = convert_to_factors(dice)

# Partition factored terms into subsets 
# and check if they satisfy the dice conditions (2 dice, 4 sided, no zero terms)
possible_partitions = []
for current_partition in partition(die_factor):
    if (check_partition(current_partition)):
        possible_partitions.append(current_partition)

possible_partitions = remove_duplicates(possible_partitions)

# We now have the partitions that will be valid dice
# So we will expand them into sympy expressions
expanded_expressions = []
for i in possible_partitions:
    current_element = []
    current_element.append(Poly(expand(expand_partition_factor(i[0])),x))
    current_element.append(Poly(expand(expand_partition_factor(i[1])),x))
    expanded_expressions.append(current_element)

# Get the coeffcients and exponents from the expressions to construct the dice
poly_terms = []
for i in expanded_expressions:
    current_set = []
    
    first_die = [] # A list containing the sides of the first die
    for monomials in i[0].terms(): # Loop through each of the monomials in the die expression
        for coefficent in range(monomials[1]): # Add the exponent to the list of sides equal to the number of the coefficent
            first_die.append(monomials[0][0])

    # Do the same for the second polynomial
    second_die = [] # A list containing the sides of the second die
    for monomials in i[1].terms():
        for coefficent in range(monomials[1]):
            second_die.append(monomials[0][0])
    
    current_set.append(first_die)
    current_set.append(second_die)
    poly_terms.append(current_set)


# Print the final results
print("")
print("There are ", len(poly_terms), " possible labelings")
print("")
for dice_set in poly_terms:
    print("Die 1: ", dice_set[0])
    print("Die 2: ", dice_set[1])
    print("")