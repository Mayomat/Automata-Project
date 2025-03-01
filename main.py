

class Automata:

    def get_index(self, character):
        # Get the index associated to a letter (used in the transition table)
        # return the index found
        return ord(character) - ord('a')

    def create_table(self, nb_row, nb_column):
        # create the table for the transition table
        # nb_row = nb_transition
        # nb_column = nb_alphabet

        self.transition_table = []

        for row in range(nb_row):
            self.transition_table.append(["-"] * nb_column)


    def fill_transition_table(self, line):
        # fill the transition table with the values from the txt
        # handle when there is no value : "-"  or 1/several values in the format :value,value
        # line contain a single line form the txt of the form : State Alphabet NextState (without space), eg : 0a1

        # if the line is empty (no transition in it so == "-", change it by the transition
        if self.transition_table[int(line[0])][self.get_index(line[1])] == "-": 
            self.transition_table[int(line[0])][self.get_index(line[1])] = line[2]

        # if there is already a transition in the table, add it in the format : transition1,transition2
        else : 
            self.transition_table[int(line[0])][self.get_index(line[1])] = self.transition_table[int(line[0])][self.get_index(line[1])]+"," + line[2]

    def create_table(self, nb_row, nb_column):
        # Create the table of the size nb_row, nb_column where all values are "-"
        # nb_row = nb_transition
        # nb_column = nb_alphabet

        self.transition_table = []

        for row in range(nb_row):
            self.transition_table.append(["-"] * nb_column)

    def string_spaced(nb_space, elem):
        # This shit don't work
        # Want to create a function that compute the space for each values in the table to be beautiful based on the number of trnasition

        if len(elem) == nb_space: return elem
        string = " "
        for i in range(nb_space - len(elem) - 1):
            string += " "
        string += elem
        return elem
        

    def display_transition_table(self, nb_row, nb_col):
        # display the table of transition
        # problem, if the number of character (eg: 1,2,4,6) for transition > 5 then all the table shift
        # nb_row = nb_transition
        # nb_column = nb_alphabet

        # there is a problem we don't show the initial and final state

        # print the abscisse of the table
        print("     ", end=" ")
        for col in range(nb_col):
            print(f"{chr(col + ord('a')):5}", end=" ")
        print()


        for row in range(nb_row):
            for col in range(nb_col):
                if col == 0: print(f"{row: 5}", end=" ")       # print the ordonnée so the transition
                print(f"{str(self.transition_table[row][col]):5}", end=" ")
            print()



    def __init__(self, file_path):
        self.name = file_path # path of the file from the directory
        self.initial = []     # array storing all the initial state
        self.final = []       # array storing all the final state

        
        with open(file_path, "r",  encoding='utf-8') as file:
            # get a list of all lines from the txt
            lines = file.readlines()

            for index_line,line in enumerate(lines):

                # in the first line symbolising the number of letter used in the alphabet
                if index_line == 0:
                    self.nb_alphabet = int(line)

                #in the 2nd line symbolising the
                elif index_line == 1: 
                    self.nb_state = int(line)

                # in the 3rd line, first elem the number of Initial state and the other are the Initial states
                # 1 value for the nb of initial state, 1 array to keep all the initial state
                elif index_line == 2:
                    for index_character, character in enumerate(line):
                        if index_character == 0: self.nb_initial = character

                        self.initial.append(character)

                # in the 4th line, first elem the number of final state and the other are the final states
                # 1 value for the nb of final state, 1 array to keep all the final state
                elif index_line == 3:
                    for index_character, character in enumerate(line):
                        if index_character == 0: self.nb_final = character

                        self.final.append(character)

                # 5th line, give the number of transition so line after this one in the txt
                # create the table to fill it after based on the size : nb_row = nb_transition, nb_column = nb_alphabet
                elif index_line == 4: 
                    self.nb_transition = int(line)
                    self.create_table( self.nb_transition, self.nb_alphabet)

                # all the other lines are the transition in the form : State Alphabet NextState (without space), eg : 0a1
                # we fill the transition table
                else:
                    self.fill_transition_table(line)


# create and display the automata from "eg.txt"
eg = Automata('eg.txt')
eg.display_transition_table(eg.nb_state, eg.nb_alphabet)
        
            
