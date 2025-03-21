alphabet = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z".split(",")
digit = "0,1,2,3,4,5,6,7,8,9".split(",")


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
    for state in group:
        print(state.num, end=" ")
    print("]")


def state_in_list(lst, value):
    """
    check if a value is in a list of state
    :param lst: list of state
    :param value: value to check
    :return:
    """
    for state in lst:
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
        if expression[i] == "(":
            new_expression+="("
        if expression[i] == ")":
            new_expression += ")"
        if expression[i] == "+":
            new_expression += ")+("
        else:
            new_expression += expression[i]
        i+= 1
    new_expression += ")"
    return new_expression

def reunites_list_of_string(regEx, value):
    """
    transform the following list of string : ['1a', '1ab'] into '1(a+ab)'
    :param regEx: list of string
    :param value: value we reunite on (string)
    :return: string
    """
    list_for_value = []
    final_list = []
    for s in regEx:
        if s[0] == value:
            list_for_value.append(s[1:])
        else:
            final_list.append(s)
    string_value = value+"("
    for i in range(len(list_for_value) -1):
        if list_for_value[i][0] == '(':
            list_for_value[i] = list_for_value[i][1:-1]
        string_value = string_value + list_for_value[i] + " + "
    if len(list_for_value):
        string_value = string_value + list_for_value[len(list_for_value) -1]+")"
        final_list.append(string_value)
    return final_list

def arden_s_lemma(regEx, value):
    """
    Apply Arden's lemma
    transform the following list ['1(a+b)','2b'] into the following string '2b(a+b)*' if the value is one
    :param regEx: list of string
    :param value: string
    :return: string
    """
    string_to_return = "("
    string_value = ""
    for s in regEx:
        if s[0] != value:
            string_to_return  = string_to_return + s + "+"
        else:
            string_value = s[1:] + "*"
    string_to_return = string_to_return[:-1] + ")" + string_value
    return string_to_return

def develop(s):
    """
    Gets a string and develop it back as a list of little strings
    Example : (2b + a)b* --> ['2bb*' ,'ab*']
    :param s: string
    :return: list of string
    """
    if s[0] != "(":
        return [s]
    new_list = []
    i = 1
    y = i
    while s[i] != ')':
        if s[i] == '+':
            new_list.append(s[y:i])
            y = i+1
        i+= 1
    new_list.append(s[y:i])
    for n in range(len(new_list)):
        new_list[n] += s[i+1:]
    return new_list

def develop_list(l):
    new_list = []
    for s in l:
        developed_list = develop(s)
        for value in developed_list:
            new_list.append(value)
    return new_list

def replace(regEx, value, new_string):
    """
    Function to replace every string containing the value indicated by the new string
    :param regEx: list of string
    :param value: string representing the value to change
    :param value: new_string to change the value by
    :return: list of string
    """
    string_to_add = "("
    for i in range(len(new_string)-1):
        string_to_add = string_to_add + new_string[i] + "+"
    string_to_add = string_to_add + new_string[len(new_string) - 1] + ")"
    for i in range(len(regEx)):
        for y in range(len(regEx[i])):
            if regEx[i][y] == value:
                regEx[i] = regEx[i][:y] + string_to_add + regEx[i][y+1:]
    return regEx

def clean_string(s):
    """
    cleans a string from useless parenthesis or epsilons
    :param s: string
    :return: string
    """
    # Cleaning the epsilon
    s = clean_epsilon(s)

    #Cleaning the parentheses
    s = clean_parentheses(s)
    return s

def clean_epsilon(s):
    new_string = ""
    for i in range(len(s)):
        if s[i] != "ε":
            new_string += s[i]
        else:
            alone = True
            if i != 0:
                if s[i - 1] != '+':
                    alone = False
            if i < len(s) - 1:
                if s[i + 1] != '+':
                    alone = False
            if alone:
                new_string += s[i]
    return new_string

def clean_parentheses(s):
    string_to_return = ""
    y = 0
    while y < len(s):
        if s[y] != '(':
            string_to_return += s[y]
        else:
            needed = False
            i = y
            nb_open = 1
            nb_closed = 0
            while nb_open != nb_closed:
                i += 1
                if s[i] == '(':
                    nb_open += 1
                if s[i] == ')':
                    nb_closed += 1
                if s[i] == '+' and nb_open-nb_closed == 1:
                    needed = True
            if i < len(s)-1:
                if s[i+1] == '*':
                    needed = True
            if not needed:
                new_string = clean_parentheses(s[y+1:i])
            if needed :
                new_string = "("+clean_parentheses(s[y+1: i]) +")"
            string_to_return += new_string
            y=i
        y+= 1
    return string_to_return

