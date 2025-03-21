alphabet = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z".split(",")

def get_index(character):
    # Get the index associated to a letter (used in the transition table)
    # return the index found
    return ord(character) - ord('a')

def compare_two_list_of_states(list1, list2):
    """
    checks if two lists of states are equal
    :param list1: list of states
    :param list2: list of states
    :return: bool
    """
    same = True
    if len(list1) != len(list2):
        return False
    for i in range(len(list1)):
        if list1[i].num != list2[i].num:
            same = False
            break
    return same


def display_group(group):
    """
    display a list of state
    :param group: list of state
    """
    print("[", end="")
    for state in group :
        print(state.num, end=" ")
    print("]")

def state_in_list(l, value):
    """
    check if a value is in a list of state
    :param l: list of state
    :param value: value to check
    :return:
    """
    for state in l:
        if state.num == value:
            return True
    return False

def check_expression(expression):
    """
    Check if the expression is valid.
    An expression is valid if it contains at least one letter, well handled parenthesis and only + and * as other characters.
    :param expression:
    :return: bool
    """
    nb_open_parenthesis = 0
    nb_closed_parenthesis = 0
    one_letter = False
    accepted_characters = ["(", ")", "*", "+"]
    for char in expression:
        if char in alphabet:
            one_letter = True
        if char == "(":
            nb_open_parenthesis += 1
        if char == ")":
            nb_closed_parenthesis += 1
        if char not in accepted_characters and char not in alphabet:
            return False
        if nb_open_parenthesis < nb_closed_parenthesis:
            return False
    if nb_open_parenthesis == nb_closed_parenthesis and one_letter:
        return True

def parenthesis_in_regEx(expression):
    """
    Function which transform ab+c in (ab)+(c). This makes the code easier
    :param expression: string
    :return: string
    """
    new_expression = "("
    i = 0
    while i < len(expression):
        if expression[i] == "+":
            new_expression += ")+("
        else:
            new_expression += expression[i]
        i+= 1
    new_expression += ")"
    return new_expression


