from usage import *
from queue import *

class State:
    def __init__(self, number):
        self.num = number
        self.transitions = [[] for x in range(26)] # An array of 26 array listing all transitions
        self.initial = False
        self.terminal = False



class Automata:
    def __init__(self):
        self.initial = []     # array storing all the initial state
        self.nb_initial = 0
        self.terminal = []       # array storing all the final state
        self.nb_final = 0
        self.states = []      # array storing all states in the automata
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
                before_state = int(line[0])
                transition = line[1]
                after_state = int(line[2])
                self.states[before_state].transitions[get_index(transition)].append(after_state)

    def max_transitions(self, index):
        maxi = 0
        for state in self.states:
            length = len(state.transitions[index])
            if length > maxi:
                maxi = length
        return maxi

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
        nb_trans_lst = [self.max_transitions(i) for i in range(self.nb_alphabet)] #Get the max transition for each letter

        # Modify the list into space taken for each column
        for i in range(len(nb_trans_lst)):
            if nb_trans_lst[i] == 1:
                nb_trans_lst[i] = 5
            else:
                nb_trans_lst[i] = 1+2*nb_trans_lst[i]

        delimiter = "-" * (30 + sum(nb_trans_lst)+self.nb_alphabet) #30 for the fixed columns,init,state,term, computation for the transition

        print(delimiter) # Line 1 : Header

        # Line 2 : Column title
        print("| Initial | State |", end="")
        for i in range(self.nb_alphabet): # Every transitions
            print(alphabet[i].center(nb_trans_lst[i], " "), end="|")
        print(" Terminal |")

        print(delimiter) # Line 3 : Delimiter

        for state in self.states: # Display each lines
            # Display the initial column
            if state.initial:
                print("|  ---->  ", end="") # If initial, print the arrow
            else:
                print("|         ", end="")

            #Display the state number
            print("|   "+str(state.num)+"   |", end="")

            #Display the state transitions
            for i in range(self.nb_alphabet):
                print((",".join(str(s) for s in state.transitions[i])).center(nb_trans_lst[i], " "), end="|")

            # Display the initial column
            if state.terminal:
                print("  <-----  |") # If terminal, print the arrow
            else:
                print("          |")

        print(delimiter) # Final line

    def create_table(self):
        # create the table for the transition table
        # nb_column = nb_alphabet
        self.transition_table = []
        for row in range(self.nb_transition):
            self.transition_table.append(["-"] * self.nb_alphabet)

    def fill_transition_table(self):
        for state_index in range(len(self.states)):
            for index_letter in range(len(self.states[state_index].transitions)):
                for i in range(len(self.states[state_index].transitions[index_letter])):
                    if self.transition_table[state_index][index_letter] == "-":
                        self.transition_table[state_index][index_letter] = str(self.states[state_index].transitions[index_letter][i])
                    else:
                        self.transition_table[state_index][index_letter] += "," + str(self.states[state_index].transitions[index_letter][i])



    def display_transition_table(self):
        # display the table of transition
        # problem, if the number of character (eg: 1,2,4,6) for transition > 5 then all the table shift
        # nb_row = nb_transition
        # nb_column = nb_alphabet

        # there is a problem we don't show the initial and final state

        # print the abscisse of the table
        print("     ", end=" ")
        for col in range(self.nb_alphabet):
            print(f"{chr(col + ord('a')):5}", end=" ")
        print()


        for row in range(self.nb_states):
            for col in range(self.nb_alphabet):
                if col == 0: print(f"{row: 5}", end=" ")       # print the ordonnée so the transition
                print(f"{str(self.transition_table[row][col]):5}", end=" ")
            print()

    def string_spaced(self, nb_space, elem):
        # This shit don't work
        # Want to create a function that compute the space for each values in the table to be beautiful based on the number of transition

        if len(elem) == nb_space: return elem
        string = " "
        for i in range(nb_space - len(elem) - 1):
            string += " "
        string += elem
        return elem

    def is_complete(self):
        """
        function to detect if the automaton is complete or not
        :return: bool
        """
        for state in self.states:
            for i in range(self.nb_alphabet):
                if len(state.transitions[i]) == 0:
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



    # def is_deterministic(self):
    #     # Check the automaton to see if
    #     # there is 1 initial state
    #     # there is no ambiguity
    #     # return a boolean
    #     #Remi
    #     if self.nb_initial != 1: return False
    #     for row in range(self.nb_transition):
    #         for col in range(self.nb_alphabet):
    #             # check to see if it can be decomposed because go to several places marked by ,
    #             for character in self.transition_table[row][col]:
    #                 if character == ",": return False
    #     #Paul
    #     for row in range(self.nb_transition):
    #         for col in range(self.nb_alphabet):
    #             if len(self.transition_table[row][col]) > 1:
    #                 if col//2 == 0:
    #                     if self.transition_table[row][col+1] != '-':
    #                         print(f"At the state {row//2} there is 2 transitions with the same letter {self.transition_table[row][col]}, "
    #                               f"{self.transition_table[row][col+1]}")
    #                         return False
    #                 else:
    #                     if self.transition_table[row][col-1] != '-':
    #                         print(f"At the state {row//2} there is 2 transitions with the same letter: {self.transition_table[row][col]}, "
    #                               f"{self.transition_table[row][col-1]}")
    #                         return False
    #     return True


    def is_deterministic(self):
        """
        function to detect if the automaton is deterministic or not
        It is deterministic if :
        - there is 1 initial state
        -there is no ambiguity
        :return: bool
        """
        if self.nb_final > 1:
            return False
        for state in self.states:
            for i in range(self.nb_alphabet):
                if len(state.transitions[i]) >1:
                    return False
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

            # adding it to the dictionary link to all the states it represent
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
                                    state_to_treat.terminal = True
                            if state_to_treat.terminal and (state_to_treat.num not in deter_automaton.terminal):
                                deter_automaton.terminal.append(state_to_treat.num)

                            deter_automaton.states.append(new_state)

                            # We add it as the only transition for the state in treatment
                            state_to_treat.transitions[i].append(new_state.num)
                            # We precise in the dict we created this new state and which state it represent
                            dict_links[deter_automaton.nb_states] = transition_equivalence
                            deter_automaton.nb_states += 1
                            # We then enqueue it to treat it after
                            determinization_queue.enqueue(new_state)
            return deter_automaton
        return self

    def is_standardized(self):
        # check if standardized if
        # 1 initial state
        # no transition toward it
        # return a boolean
        if self.nb_initial != 1:
            return False
        for state in self.states: # For every state in the automaton
            for i in range(self.nb_alphabet): # Go through all transition of the state
                if self.initial[0] in state.transitions[i]: # Check if the initial state is in any transition
                    return False
        return True

    def find_non_accessible_states(self):

        """
        From the initial states go to every state using transitions and save the visited states
        If a state is not part of the accessible ones, then it is non-accessible
        """

        non_accessible_states = []
        accessible_states = self.initial # List updating itself with accessible states, first accessible states are initial ones
        for state in accessible_states:
            for i in range(self.nb_alphabet): # For every possible transition
                for next_state in self.states[state].transitions[i]: # If a transition exists to a non accessed state then the state is accessible
                    if next_state not in accessible_states: # If we did not already visit it, add it to accessible states
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
            return
        init_state = State(self.nb_states) #New initial state
        init_state.initial = True
        self.nb_states += 1
        self.nb_initial = 1
        #For each transition in each initial state
        for state in self.initial:
            self.states[state].initial = False  # Remove the initial attribute from the state
            for i in range(self.nb_alphabet):
                for transition in self.states[state].transitions[i]:
                    if transition not in init_state.transitions[i]:
                        init_state.transitions[i].append(transition) #We add to the new initial state each transition
                        self.nb_transition += 1
        self.states.append(init_state)# Add the new states into the automaton's state list
        self.initial = [init_state.num] # Change the automaton's initial state list to our new initial state