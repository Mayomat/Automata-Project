from usage import *
from queue import *
import re

class State:
    def __init__(self, number):
        self.num = number
        self.transitions = [[] for _ in range(26)]  # An array of 26 array listing all transitions
        self.initial = False
        self.terminal = False

    def compare_to_minimize(self, other):
        """
        Check if two states can be grouped to be then minimized together
        :param other: second state
        :return: bool
        """
        same = True
        if self.terminal != other.terminal:
            same = False

        for i in range(26):
            if self.transitions[i] != other.transitions[i]:
                same = False

        return same


class Automata:
    def __init__(self):
        self.initial = []  # array storing all the initial state
        self.nb_initial = 0
        self.terminal = []  # array storing all the final state
        self.nb_final = 0
        self.states = []  # array storing all states in the automata
        self.nb_states = 0
        self.nb_alphabet = 0
        self.transition_table = []
        self.nb_transition = 0

    def create_automaton_from_file(self, file_path):

        with open(file_path, "r", encoding='utf-8') as file:
            # first line : number of letter used in the alphabet
            self.nb_alphabet = int(file.readline())

            # 2nd line : number of states in the automaton
            self.nb_states = int(file.readline())

            # creation of all the states, we fill them later
            for i in range(self.nb_states):
                new_state = State(i)
                self.states.append(new_state)

            # 3rd line filled with initial states
            init_line = file.readline().split()
            self.nb_initial = int(init_line[0])
            for i in range(1, self.nb_initial + 1):
                self.initial.append(int(init_line[i]))

            # Putting all entry states in the list "initial" as initial
            for i in range(self.nb_initial):
                self.states[self.initial[i]].initial = True

            # 4th line filled with final states
            term_line = file.readline().split()
            self.nb_final = int(term_line[0])
            for i in range(1, self.nb_final + 1):
                self.terminal.append(int(term_line[i]))

            # Putting all final states in the list "final" as terminal
            for i in range(self.nb_final):
                self.states[self.terminal[i]].terminal = True

            # 5th line gives the number of transition so line after this one in the txt
            self.nb_transition = int(file.readline())
            for i in range(self.nb_transition):
                line = file.readline()
                before_state, transition, after_state = re.match(r"(\d+)([a-zA-Z])(\d+)", line).groups()
                self.states[int(before_state)].transitions[get_index(transition)].append(int(after_state))

    def max_transitions(self, index):
        maxi = 0
        nb_elem = 0
        for state in self.states:
            length = sum(len(str(nxtState)) for nxtState in state.transitions[index])
            if length > maxi:
                maxi = length
                nb_elem = len(state.transitions[index])
        return [maxi, nb_elem]

    """
    ----------------------------------------------
    | Initial | State |   a   |  b  | Terminal |
    ----------------------------------------------
    |  ---->  |   0   | 0,1,3 | 1,2 |  ---->   |
    ----------------------------------------------
    |         |   1   | 2     |     |          |
    ----------------------------------------------
    |  ---->  |   2   | 0     |     |  ---->   |
    ----------------------------------------------
    """

    def display_table(self):
        nb_trans_lst = [self.max_transitions(i) for i in
                        range(self.nb_alphabet)]  # Get the max transition for each letter

        # Modify the list into space taken for each column
        i = 0
        size_lst = []
        for length, nb_elem in nb_trans_lst:
            elem = length + nb_elem - 1
            if elem == 1:
                elem = 5
            elif elem == 2:
                elem = 6
            else:
                elem += 2
            size_lst.append(elem)
            i += 1

        size_state = 6 + len(str(self.nb_states))  # Size of the column State

        delimiter = "A" + "═════════" + "B" + "═"*size_state + "B"
        for nb in size_lst:
            delimiter += "═" * nb + "B"
        delimiter += "══════════" + "C"

        print(delimiter.replace("A", "╔").replace("B", "╦").replace("C", "╗"))  # Line 1 : Header

        # Line 2 : Column title
        print("║ Initial ║", end="")
        print("State".center(size_state, " ")+"║", end="")
        for i in range(self.nb_alphabet):  # Every transitions
            print(alphabet[i].center(size_lst[i], " "), end="║")
        print(" Terminal ║")

        print(delimiter.replace("A", "╠").replace("B", "╬").replace("C", "╣"))  # Line 3 : Delimiter

        for state in self.states:  # Display each lines
            # Display the initial column
            if state.initial:
                print("║  ---->  ", end="")  # If initial, print the arrow
            else:
                print("║         ", end="")

            # Display the state number
            print("║" + str(state.num).center(size_state, " ") + "║", end="")

            # Display the state transitions
            for i in range(self.nb_alphabet):
                print((",".join(str(s) for s in state.transitions[i])).center(size_lst[i], " "), end="║")

            # Display the terminal column
            if state.terminal:
                print("  ----->  ║")  # If terminal, print the arrow
            else:
                print("          ║")

        print(delimiter.replace("A", "╚").replace("B", "╩").replace("C", "╝"))  # Final line

    def is_complete(self):
        """
        function to detect if the automaton is complete or not
        :return: bool
        """
        for state in self.states:
            for i in range(self.nb_alphabet):
                if len(state.transitions[i]) == 0:
                    # error message when not complete
                    print(f"The state '{state.num}' has a no transition for '{alphabet[i]}' so it's not complete.")
                    print("We can stop here and don't have to check for other missing transitions")
                    return False
        return True

    def complete(self):
        """
        function completing an automaton
        """
        if not self.is_complete():
            garbage = State(self.nb_states)
            self.nb_states += 1
            self.states.append(garbage)
            for state in self.states:
                for i in range(self.nb_alphabet):
                    if len(state.transitions[i]) == 0:
                        state.transitions[i].append(garbage.num)

    def is_deterministic(self):
        """
        function to detect if the automaton is deterministic or not
        It is deterministic if :
        - there is 1 initial state
        -there is no ambiguity
        :return: bool
        """
        if self.nb_initial > 1:
            # error message when more than 1 initial state
            print(f"The automaton is not deterministic because there is {self.nb_initial} initial states")
            return False
        for state in self.states:
            for i in range(self.nb_alphabet):
                if len(state.transitions[i]) > 1:
                    # error message when ambiguity
                    print(f" The automaton is not deterministic because the state {state.num} is ambiguous with the letter {i}")
                    return False
        print("The automaton is deterministic")
        return True

    def determine(self):
        """
        Function to determine the automaton if it is not deterministic yet
        :return: Automata
        """
        if not self.is_deterministic():
            deter_automaton = Automata()
            deter_automaton.nb_alphabet = self.nb_alphabet
            # creation of a dict to understand the link between old states and new states :
            # For example if the new state 3 represent the state 5, 7, and 9 of the non-deterministic automaton,
            # we'll have :
            # { 3 : [5, 7, 9] }
            dict_links = {}

            # creation of the only initial state of the deterministic automaton
            initial_state = State(0)
            initial_state.initial = True
            deter_automaton.states.append(initial_state)
            deter_automaton.nb_states += 1
            deter_automaton.nb_initial += 1
            deter_automaton.initial.append(0)

            # adding it to the dictionary link to all the states it represents
            dict_links[0] = set()
            for state in self.initial:
                dict_links[0].add(state)

            # creation of a queue to control the creation and treatment of all the states :
            # if we create a new states for the automaton, we add it to the queue, it will then be treated later
            determinization_queue = Queue()
            determinization_queue.enqueue(initial_state)
            # we create a while loop to treat every state until there are none
            while not determinization_queue.isEmpty():
                state_to_treat = determinization_queue.dequeue()
                for i in range(self.nb_alphabet):
                    exist_already = False
                    if len(dict_links[state_to_treat.num]) != 0:
                        deter_automaton.nb_transition += 1

                        # we create a set to get all the transition for this state
                        transition_equivalence = set()
                        for state_number in dict_links[state_to_treat.num]:
                            for transition in self.states[state_number].transitions[i]:
                                transition_equivalence.add(transition)

                        # we check we didn't already create this state
                        for key in dict_links.keys():
                            if dict_links[key] == transition_equivalence:
                                state_to_treat.transitions[i].append(key)
                                exist_already = True
                                break

                        # we create a new state if we don't have it yet
                        if not exist_already:
                            new_state = State(deter_automaton.nb_states)
                            # We check if it is a terminal state
                            for name_state in transition_equivalence:
                                if self.states[name_state].terminal:
                                    new_state.terminal = True
                            if new_state.terminal and (new_state.num not in deter_automaton.terminal):
                                deter_automaton.terminal.append(new_state.num)

                            deter_automaton.states.append(new_state)

                            # We add it as the only transition for the state in treatment
                            state_to_treat.transitions[i].append(new_state.num)
                            # We precise in the dict we created this new state and which state it represent
                            dict_links[deter_automaton.nb_states] = transition_equivalence
                            deter_automaton.nb_states += 1
                            # We then enqueue it to treat it after
                            determinization_queue.enqueue(new_state)
            return deter_automaton
        print("The automaton is already determined")
        return self

    def is_standardized(self):
        # check if standardized :
        # 1 initial state
        # no transition toward it
        # return a boolean
        if self.nb_initial != 1:
            print(f"The automaton is not standardized because there is {self.nb_initial} initial states")
            return False
        for state in self.states:  # For every state in the automaton
            for i in range(self.nb_alphabet):  # Go through all transition of the state
                if self.initial[0] in state.transitions[i]:  # Check if the initial state is in any transition
                    print(f"The automaton is not standardized because the state {i} has an transition toward the initial state with '{alphabet[i]}'")
                    return False
        print(f"The automaton is standardized")
        return True

    def find_non_accessible_states(self):

        """
        From the initial states go to every state using transitions and save the visited states
        If a state is not part of the accessible ones, then it is non-accessible
        """

        non_accessible_states = []
        accessible_states = self.initial  # List updating itself with accessible states
        for state in accessible_states:
            for i in range(self.nb_alphabet):  # For every possible transition
                # If a transition exists to a non accessed state then the state is accessible
                for next_state in self.states[state].transitions[i]:
                    if next_state not in accessible_states:  # If we did not visit it, add it to accessible states
                        accessible_states.append(self.states[next_state].num)

        # Save the non-accessible states
        for state in self.states:
            if state.num not in accessible_states:
                non_accessible_states.append(state.num)

        return non_accessible_states

    def standardize(self):
        """
        An automaton is standardized if it has only one initial state,
        and no transition goes to the initial state
        """
        # Combine every initial states transitions into a new initial state
        if self.is_standardized():
            print("The automaton is already standardized")
            return
        init_state = State(self.nb_states)  # New initial state
        init_state.initial = True
        self.nb_states += 1
        self.nb_initial = 1
        # For each transition in each initial state
        for state in self.initial:

            self.states[state].initial = False  # Remove the initial attribute from the state
            for i in range(self.nb_alphabet):
                for transition in self.states[state].transitions[i]:
                    if transition not in init_state.transitions[i]:
                        init_state.transitions[i].append(transition)  # We add to the new initial state each transition
                        self.nb_transition += 1
        self.states.append(init_state)  # Add the new states into the automaton's state list
        self.initial = [init_state.num]  # Change the automaton's initial state list to our new initial state

    def complementary(self):    # Changes the Automaton to its complementary
        self.complete()
        self.terminal = []
        for state in self.states:
            state.terminal = not state.terminal
            if state.terminal:
                self.terminal.append(state)
        self.nb_final = len(self.terminal)

    def minimize(self):
        """
        To minimize : determine, complete, check there are no non-accessible states
        :return: automata
        """
        automaton = self.determine()  # we determine --> there are no non-accessible state

        automaton.complete()

        # At first, we only have 2 groups : terminal and non-terminal
        groups = [[], []]
        for state in automaton.states:
            if state.terminal:
                groups[0].append(state)
            else:
                groups[1].append(state)

        # Display the partition of Terminal States and Non-Terminal States
        print("Partition 1:")
        print("Group 1: Terminal States")
        for state in groups[0]:
            print(f" - State {state.num} (Terminal)")
        print("\nGroup 2: Non-Terminal States")
        for state in groups[1]:
            print(f" - State {state.num} (Non-Terminal)")


        # this boolean is put to true when after a step we still have the same groups
        stop = False
        # variables to count the number of partition
        partition = 1
        # loop running until every group is in list(reunited)
        while not stop:
            # We create a new list group which we'll compare to the old list groups
            new_groups = []
            # We create a list with the same states but with transitions link to the old groups (at first it is 1 or 0)
            new_states = []

            # We add new states with the new transitions
            for state in automaton.states:
                state_new_transition = State(state.num)
                if state.terminal:
                    state_new_transition.terminal = True
                if state.initial:
                    state_new_transition.initial = True

                for i in range(self.nb_alphabet):
                    transition = state.transitions[i][0]
                    for y in range(len(groups)):
                        if state_in_list(groups[y], transition):
                            state_new_transition.transitions[i].append(y)
                            break
                new_states.append(state_new_transition)

            # regroup the different state into groups
            for state in new_states:
                found = False
                for group in new_groups:
                    # check if the state can be in this group
                    if group[0].compare_to_minimize(state):
                        group.append(state)
                        found = True
                        break
                # if the state can not be grouped, we create a new group
                if not found:
                    new_groups.append([state])
            print(f"\nPartition {partition}:", end="")
            for i in range(len(new_groups)):
                print(f"\nGroup {i}:\n - State", end="")
                for state in new_groups[i]:
                    print(f" {state.num}", end="")
            print("")
            partition += 1

            # compare new_groups with groups to see if it changed
            stop = True
            for new_group in new_groups:
                found = False
                for group in groups:
                    if compare_two_list_of_states(new_group, group):
                        found = True
                        break
                if not found:
                    stop = False
                    break

            groups = new_groups

        # creation of the new automaton
        minimized_automaton = Automata()
        minimized_automaton.nb_initial = 1
        minimized_automaton.nb_states = len(groups)
        minimized_automaton.nb_alphabet = self.nb_alphabet
        for i in range(minimized_automaton.nb_states):
            minimized_automaton.states.append(groups[i][0])
            minimized_automaton.states[i].num = i

        for i in range(len(groups)):
            for state in groups[i]:
                if state.initial:
                    minimized_automaton.states[i].initial = True
                    minimized_automaton.initial.append(state.num)
                if state.terminal:
                    minimized_automaton.states[i].terminal = True

        for state in minimized_automaton.states:
            if state.terminal:
                minimized_automaton.nb_final += 1
                minimized_automaton.terminal.append(state.num)

        minimized_automaton.nb_transition = minimized_automaton.nb_states * minimized_automaton.nb_alphabet
        return minimized_automaton

    def recognize_word(self, word):
        """
        Check if the word take in parameter is accepted by the automaton
        return True or False
        """
        print("We first check if our automaton is determined, else we determine it")
        determine_aut = self.determine()
        print("we do the same to complete it")
        determine_aut.complete()
        current_state = determine_aut.states[determine_aut.initial[0]]
        if word == " ":  # Check if the word is the empty word
            if len(determine_aut.initial) == 0 or len(determine_aut.terminal) == 0:  # It can't accept the empty word if there are no final or initial state
                return False

            if len(determine_aut.initial) != 0 and len(determine_aut.terminal) != 0:
                if determine_aut.initial[0] == determine_aut.terminal[0]:  # The initial state is a terminal state
                    return True
        for letter in word:
            index_letter = get_index(letter)
            if index_letter > determine_aut.nb_alphabet:  # Check that the letter is accepted by the automaton
                print("One letter is not taken by automaton ")
                return False
            else:
                current_state = determine_aut.states[current_state.transitions[index_letter][0]]  # Next state to check
        return current_state.terminal

    def word_recognition(self):
        print(f"The world is composed of the letters : ")
        for i in range(self.nb_alphabet):
            print(alphabet[i], end=" ")  # Display the alphabet of the automaton
        print()
        word = input("Enter a word according to the letters accepted by the automaton (Put 'end' to stop):")
        print()
        while word != "end":  # While the word 'end' is not enter, it continues to wait for a word
            if self.recognize_word(word):
                print(f"The word {word} is recognized by the automaton ")
            else:
                print(f"The word {word} is NOT recognized by the automaton ")
            word = input("Enter a word according to the letters accepted by the automaton (Put 'end' to stop):")
            print()

    def create_automaton_from_regEx(self, expression):
        """
        Create an automaton giving a regular expression.
        example : ab+c
        :param expression:
        :return:
        """
        expression = parenthesis_in_regEx(expression)
        # The following lines are the most important, they call the recursive function creating the states and transitions
        if check_expression(expression):
            self.states, self.nb_alphabet = regEx_separation(expression)
        for state in self.states:
            if state.initial:
                self.initial.append(state.num)
                self.nb_initial += 1
            if state.terminal:
                self.terminal.append(state.num)
                self.nb_final += 1
            self.nb_states += 1

    def getRegExExpression(self):
        dict_expressions = {}
        for state in self.states:
            dict_expressions[state.num] = []
            if state.initial:
                dict_expressions[state.num].append("ε")

        for state in self.states:
            for i in range(self.nb_alphabet):
                for transition in state.transitions[i]:
                    dict_expressions[transition].append(str(state.num) + alphabet[i])


        for i in range(len(self.states)):
            dict_expressions[i] = reunites_list_of_string(dict_expressions[i], str(i))
            for y in range(len(dict_expressions[i])):
                dict_expressions[i][y] = clean_string(dict_expressions[i][y])

            dict_expressions[i] = arden_s_lemma(dict_expressions[i], str(i))

            dict_expressions[i] = develop(dict_expressions[i])
            for y in range(i+1, len(self.states)):
                dict_expressions[y] = replace(dict_expressions[y], str(i), dict_expressions[i])
                dict_expressions[y] = develop_list(dict_expressions[y])


        #check there are no number left
        i = len(self.states) -1
        while i>-1:
            for y in range(i):
                dict_expressions[y] = replace(dict_expressions[y], str(i), dict_expressions[i])
                dict_expressions[y] = develop_list(dict_expressions[y])
            dict_expressions[i][0] = clean_string(dict_expressions[i][0])


            i-=1

        last_string = ""
        for i in range(len(self.states)):
            if self.states[i].terminal:
                for text in dict_expressions[i]:
                    last_string = last_string + text +"+"
        last_string = last_string[:-1]
        return last_string



# Functions used in 'create_automaton_from_regEx'
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

    # end of the recursion: only one letter so 2 states -> state1 letter state2
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

        # If the letter is followed by another letter or a open parenthesis, we call the function followedRegEx which
        # will merge the two lists of states making them follow each other
        if expression[1] in alphabet or expression[1] == '(':
            state, nb_alphabet = followedRegEx((states, nb_alphabet), regEx_separation(expression[1:]))
        else :
            if expression[1] == '*':
                # If it is a *, we need to check if there is something after it or not
                if len(expression) > 2:
                    # If the '*' is followed by a letter or a '(', we make the followed by call but adding the starCall
                    # inside the function. The star call will create a list of states which repeat itself
                    if expression[2] in alphabet or expression[2] == '(':
                        states, nb_alphabet = followedRegEx(starRegEx((states, nb_alphabet)), regEx_separation(expression[2:]))
                    else:
                        # If it is a '+', we do the same but with the orRegEx function
                        if expression[2] == '+':
                            states, nb_alphabet = orRegEx(starRegEx((states, nb_alphabet)), regEx_separation(expression[3:]))
                else :
                    # in the case where it is only one letter with a star, we only need one state which can loop on itself
                    states = [states[0]]
                    states[0].transitions[get_index(expression[0])] = [0]
                    states[0].terminal = True
                    return states, nb_alphabet

        if expression[1] == '+':
            # if we get a simple '+', we make the or call between our letter and what follows the +
            # For example, a+ab will create the states for a then call those inside the function with the recursive
            # call of ab. In the recursive call, ab is treated as a 'a followed by b' by the function followedRegEx
            states, nb_alphabet = orRegEx((states, nb_alphabet), regEx_separation(expression[2:]))

    # If we get a parenthesis, we get the end of the parenthesis and call the function on what's inside.
    # For this we again check what is after to make the recursive call inside the function followRegEx or orRegEx
    # It is the same logic as with only one letter
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
            state.terminal = states2[0].terminal
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