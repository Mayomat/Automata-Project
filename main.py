from Automata import *

# create and display the automata from "eg.txt"


ex = Automata()
ex.create_automaton_from_file('eg.txt')
ex.display_table()
ex.word_recognition()