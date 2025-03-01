

class Automata:

    def alphabet(self, nb_alphabet):
        self.alphabet = []
        for i in range(nb_alphabet):
            self.alphabet.append(chr(97 + i))

    def get_index(self, character):
        return ord(character) - ord('a')

    def create_table(self, nb_row, nb_column):
        self.transition_table = []

        for row in range(nb_row):
            self.transition_table.append(["-"] * nb_column)


    def fill_transition_table(self, line):
        if self.transition_table[int(line[0])][self.get_index(line[1])] == "-": 
            self.transition_table[int(line[0])][self.get_index(line[1])] = line[2]
        else : 
            self.transition_table[int(line[0])][self.get_index(line[1])] = self.transition_table[int(line[0])][self.get_index(line[1])]+"," + line[2]

    def create_table(self, nb_row, nb_column):
        self.transition_table = []

        for row in range(nb_row):
            self.transition_table.append(["-"] * nb_column)

    # This shit don't work
    def string_spaced(nb_space, elem):
        if len(elem) == nb_space: return elem
        string = " "
        for i in range(nb_space - len(elem) - 1):
            string += " "
        string += elem
        return elem
        

    def display_transition_table(self, nb_row, nb_col):

        print("     ", end=" ")
        for col in range(nb_col):
            print(f"{chr(col + ord('a')):5}", end=" ")
        print()


        for row in range(nb_row):
            for col in range(nb_col):
                if col == 0:
                    print(f"{row: 5}", end=" ")
                print(f"{str(self.transition_table[row][col]):5}", end=" ")
            print()



    def __init__(self, file_path):
        self.name = file_path
        self.initial = []
        self.final = []

        
        with open(file_path, "r",  encoding='utf-8') as file:
            lines = file.readlines()

            for index_line,line in enumerate(lines):

                if index_line == 0: 
                    self.nb_alphabet = int(line)

                elif index_line == 1: 
                    self.nb_state = int(line)

                elif index_line == 2:
                    for index_character, character in enumerate(line):
                        if index_character == 0: self.nb_initial = character

                        self.initial.append(character)

                elif index_line == 3:
                    for index_character, character in enumerate(line):
                        if index_character == 0: self.nb_final = character

                        self.final.append(character)

                elif index_line == 4: 
                    self.nb_transition = int(line)
                    self.create_table( self.nb_transition, self.nb_alphabet)
                
                else:
                    self.fill_transition_table(line)



eg = Automata('eg.txt')
eg.display_transition_table(eg.nb_state, eg.nb_alphabet)
        
            
