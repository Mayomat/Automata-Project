from usage import *

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



    def create_table(self):
        # create the table for the transition table
        # nb_column = nb_alphabet

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


        for row in range(self.nb_transition):
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
        # function to detect if the automata is complete or not, check the transition table to see if there is no transition = "-"
        # return a boolean
        for row in range(self.nb_transition):
            for col in range(self.nb_alphabet):
                if self.transition_table[row][col] == "-": return False
        return True

    def is_deterministic(self):
        # Check the automaton to see if
        # there is 1 initial state
        # there is no ambiguity
        # return a boolean
        if self.nb_initial != 1: return False
        for row in range(self.nb_transition):
            for col in range(self.nb_alphabet):
                # check to see if can be decomposed because go to several places marked by ,
                for character in self.transition_table[row][col]:
                    if character == ",": return False
        return True

    def is_standardized(self):
        # check if standardized if
        # 1 initial state
        # no transition toward it
        # return a boolean
        if self.nb_initial != 1: return False
        initial = self.initial[0]
        for row in range(self.nb_transition):
            for col in range(self.nb_alphabet):
                for character in self.transition_table[row][col]:
                    if character == initial: return False
        return True

    def standardize(self, nb_row, nb_col, ):
        pass