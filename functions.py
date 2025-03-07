# go through each transition and look if there is a transition
# that have only one transition per column or if there is 1 entry
def is_deterministic(fa):
    if len(fa.initial) > 1:
        print("The fa has more than 1 entry, then it is not deterministic")
        return False
    for i in range(len(fa.transition_table)):
        if len(fa.transition_table[i]) > 1:
            if i//2 == 0:
                if fa.transition_table[i+1] != '-':
                    print(f"At the state {i//2} there is 2 transitions with the same letter {fa.transition_table[i]}, " 
                          f"{fa.transition_table[i+1]}")
                    return False
            else:
                if fa.transition_table[i-1] != '-':
                    print(f"At the state {i//2} there is 2 transitions with the same letter: {fa.transition_table[i]}, "
                          f"{fa.transition_table[i-1]}")
                    return False
    return True


# check if there is the no transition in a column
def is_complete(fa):
    for i in range(len(fa.transition_table)):
        if fa.transition_table[i] == '-':
            return False
    return True

# check that there is no transition going to the entry (only 1 entry)
def is_standard(fa):
    if is_complete(fa):
        for i in range(len(fa.transition_table)):
            if fa.transition_table[i] == fa.initial[0]:
                return False


def determinization(fa):
    pass


def completing(fa):
    pass


def standardization(fa):
    if not is_standard(fa):
        pass
    return

