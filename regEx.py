def regEx_separation(expression):
    """
    Recursive function to create a list of state which are based on a regEx expression.
    Format of the expression : 'ab+c*(d+e)'
    :param expression: string
    :return: list of state and its alphabet
    """
    # creation of the first state and a list of all the states
    states = []


    # This variable is here to know the whole alphabet so we can create the automaton later on
    nb_alphabet = 0

    # end of the recursion:
    # We create two states : first one going to the second one with the transition
    # the first one is marked as initial, the second as final
    # it will then be treated when going up in the recursion call
    if len(expression) == 1:
        if get_index(expression[0]) +1 > nb_alphabet:
            nb_alphabet = get_index(expression[0]) +1

        initial_state = State(0)
        initial_state.initial = True
        final_state = State(1)
        final_state.terminal = True
        initial_state.transitions[get_index(expression[0])] = [1]
        states.append(initial_state)
        states.append(final_state)
        return states, nb_alphabet

    # We now make a recursive call to create a list of states which are linked
    # First if we start with a letter we check the character after:
        # A letter or a parenthesis means a followed by
        # A + means it is a or with what is after
        # A * means it repeats itself

    if expression[0] in alphabet:
        #We create a new state which we add to list(states)
        initial_state = State(0)
        final_state =State(1)
        initial_state.initial = True
        final_state.terminal = True
        initial_state.transitions[get_index(expression[0])] = [1]
        states.append(initial_state)
        states.append(final_state)

        # We update the alphabet if needed
        if get_index(expression[0]) +1 > nb_alphabet:
            nb_alphabet = get_index(expression[0]) +1

        if expression[1] in alphabet or expression[1] == '(':
            state, nb_alphabet = followedRegEx((states, nb_alphabet), regEx_separation(expression[1:]))
        else :
            if expression[1] == '*':
                # If it is a *, we need to check if there is something after it or not
                if len(expression) > 2:
                    if expression[2] in alphabet or expression[2] == '(':
                        states, nb_alphabet = followedRegEx(starRegEx((states, nb_alphabet)), regEx_separation(expression[2:]))
                    else:
                        if expression[2] == '+':
                            states, nb_alphabet = orRegEx(starRegEx((states, nb_alphabet)), regEx_separation(expression[3:]))
                else :
                    # in the case where it is only one letter with a star, we only need one state which can loop on itself
                    states = [states[0]]
                    states[0].transitions[get_index(expression[0])] = [0]
                    states[0].terminal = True
                    return states, nb_alphabet

        if expression[1] == '+':
            states, nb_alphabet = orRegEx((states, nb_alphabet), regEx_separation(expression[2:]))

    if expression[0] == "(":
        y = 1
        nb_open = 1
        nb_close = 0
        while nb_open!=nb_close:
            if expression[y] == ')':
                nb_close +=1
            if expression[y] == '(':
                nb_open += 1
            y+=1

        if len(expression) > y:
            if expression[y] in alphabet or expression[y] == '(':
                states, nb_alphabet = followedRegEx(regEx_separation(expression[1:y-1]), regEx_separation(expression[y:]))
            else:
                if expression[y] == '*':
                    if len(expression) >y+1:
                        if expression[y+1] in alphabet or expression[y+1] == '(':
                            states, nb_alphabet = followedRegEx(starRegEx(regEx_separation(expression[1:y-1])), regEx_separation(expression[y+1:]))
                        else:
                            if expression[y+1] == '+':
                                states, nb_alphabet = orRegEx(starRegEx(regEx_separation(expression[1:y - 1])), regEx_separation(expression[y+2:]))
                    else :
                        states, nb_alphabet = starRegEx(regEx_separation(expression[1:y-1]))
                else:
                    if expression[y] == '+':
                        states, nb_alphabet = orRegEx(regEx_separation(expression[1:y-1]), regEx_separation(expression[y+1:]))
        else:
            states, nb_alphabet = regEx_separation(expression[1:y-1])

    return states, nb_alphabet

def orRegEx(statesAlpha1, statesAlpha2):
    """
    Bring two expression together to have an 'or' in regEx.
    The function reunites the transitions of the two initial states into only one initial state.
    :param statesAlpha1: first list of states
    :param statesAlpha2: second list of states
    :return: list of states, int
    """
    nb_alphabet = max(statesAlpha1[1], statesAlpha2[1])
    states = []
    states1 = statesAlpha1[0]
    states2 = statesAlpha2[0]

    initial_state = State(0)
    initial_state.initial = True
    #Here we add the transitions of the initial of states1 to our new initial state
    initial_state.transitions = states1[0].transitions
    if states1[0].terminal:
        initial_state.terminal = True
    states.append(initial_state)
    # Then we add every state of states 1 to our new list states, the name of the states are easy so it is ok
    for i in range(1, len(states1)):
        states.append(states1[i])

    # For the second list, we cannot add it easily because of the names.
    # For example : if the state 1 transit to state 2 in the second list. We need to change the name and the transitions
    # according to the number of state already in the list states

    # We first treat the initial state (state 0)
    # We add all the transitions of the initial state to our new initial state
    for i in range(statesAlpha2[1]):
        for transition in states2[0].transitions[i]:
            states[0].transitions[i].append(transition + len(states1) -1)
    if states2[0].terminal:
        states[0].terminal = True

    # We add now all the other states in states2 taking care to change the names and the transition (+len(states1) -1)
    for i in range(1, len(states2)):
        states2[i].num += len(states1) -1
        for y in range(statesAlpha2[1]):
            for n in range(len(states2[i].transitions[y])):
                states2[i].transitions[y][n] += len(states) -1
        states.append(states2[i])

    return states, nb_alphabet

def followedRegEx(statesAlpha1, statesAlpha2):
    """
    Bring two expression together to have an 'and' in regEx.
    The function transits the final states of te first list to the second states of the second list.
    :param statesAlpha1: first list of states
    :param statesAlpha2: second list of states
    :return: list of states, int
    """
    nb_alphabet = max(statesAlpha1[1], statesAlpha2[1])
    states = statesAlpha1[0]
    states2 = statesAlpha2[0]

    # to create those new transition, we don't forget to change every name of the second list and there transition first
    for i in range(len(states2)):
        states2[i].num += len(states) -1
        for y in range(statesAlpha2[1]):
            for n in range(len(states2[i].transitions[y])):
                states2[i].transitions[y][n] += len(states) -1


    # Now for every terminal of the first list, we add the same transition as the initial state of the second list
    # let us create a variable with the transition of the initial state of the second list for easy reading
    initTransitions = states2[0].transitions
    for state in states:
        if state.terminal:
            state.terminal = states[0].terminal
            for i in range(statesAlpha2[1]):
                for transition in initTransitions[i]:
                    state.transitions[i].append(transition)

    # Now we add the states from the second list into states except for the initial one which is not needed
    for i in range(1, len(states2)):
        states.append(states2[i])

    return states, nb_alphabet


def starRegEx(statesAlpha):
    """
    Change an expression so it loops on itself
    To make it loop on itself : The initial state also becomes terminal and all the terminal states get the transitions
    from the initial state.
    :param statesAlpha : list of states
    :return: list of states, int
    """
    nb_alphabet = statesAlpha[1]
    states = statesAlpha[0]
    states[0].terminal = True

    # Let us create a variable for the transition of the initial state making the code more readable
    transitions = states[0].transitions

    # Now we add those transition to every final state (if they don't exist already)
    for state in states:
        if state.terminal:
            for i in range(nb_alphabet):
                for transition in transitions[i]:
                    if transition not in state.transitions[i]:
                        state.transitions[i].append(transition)

    return states, nb_alphabet