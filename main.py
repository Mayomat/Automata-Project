from Automata import *

# create and display the automata from "eg.txt"

"""
eg = Automata()
eg.create_automaton_from_file('eg.txt')
eg.create_table()
eg.fill_transition_table()
eg.display_transition_table()
eg.is_deterministic()
print(eg.is_standardized())
print(eg.find_non_accessible_states())
"""


ex = Automata()
ex.create_automaton_from_file('eg.txt')
ex.create_table()
ex.display_transition_table()
ex.fill_transition_table()
ex.display_transition_table()
ex.standardize()
ex.create_table()
ex.fill_transition_table()
ex.display_transition_table()
print(ex.max_transitions(1))
ex.display_table()


"""
print("[")
for i in range(len(ex.initial[0].transitions)):
    print("[", end="")
    for j in range(len(ex.initial[0].transitions[i])):
        print(eg.transition_table[i][j], end="")
    print("]", end="")
"""