from Automata import *


# create and display the automata from "eg.txt"
eg = Automata()
eg.create_automaton_from_file('eg.txt')
eg.create_table()
eg.fill_transition_table()
eg.display_transition_table()
eg.is_deterministic()
print(eg.find_non_accessible_states())
            
