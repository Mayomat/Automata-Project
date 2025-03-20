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
