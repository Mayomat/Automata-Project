from Automata import *


# create and display the automata from "eg.txt"
eg = Automata()
eg.create_automaton_from_file('eg.txt')
eg.create_table()
eg.fill_transition_table()
eg.display_transition_table()
eg.is_deterministic()
eg.standardize()

"""
print("- - - - - - -")

ex = Automata()
ex.create_automaton_from_file('eg.txt')
#ex.display_transition_table()
ex.standardize()
eg.create_table()
ex.fill_transition_table()

print("[")
for i in range(len(ex.initial[0].transitions)):
    print("[",end="")
    for j in range(len(ex.initial[0].transitions[i])):
        print(eg.transition_table[i][j],end="")
    print("]",end="")

"""