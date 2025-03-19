from Automata import *

def print_menu():
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║                AUTOMATON CONSOLE MENU              ║")
    print("╠════════════════════════════════════════════════════╣")
    print("║ 0: Initialize Automaton from File                  ║")
    print("║ 1: Create Transition Table                         ║")
    print("║ 2: Display Transition Table                        ║")
    print("║ 3: Fill Transition Table                           ║")
    print("║ 4: Standardize Automaton                           ║")
    print("║ 5: Max Transitions from State 1                    ║")
    print("║ 6: Display Full Table                              ║")
    print("║ 7: Return to the automaton selection               ║")
    print("╚════════════════════════════════════════════════════╝")

def main():
    ex = Automata()

    while True:
        print("╔════════════════════════════════════════════════════╗")
        print("║                AUTOMATON CONSOLE MENU              ║")
        print("╠════════════════════════════════════════════════════╣")
        print("║ Enter the number of the automaton that you want,   ║")
        print("║ From 1 to 44 and O to exit                         ║")
        print("╚════════════════════════════════════════════════════╝")
        choice = int(input("Enter your choice: "))
        if choice > 0 and choice < 45:
            path = "Finite_Automata_files/"+str(choice)+".txt"
        elif choice == 0:
            print("╔════════════════════════════════════════════════════╗")
            print("║                     ByeBye                         ║")
            print("╚════════════════════════════════════════════════════╝")
            break
        else:
            print("Invalid input. Please enter a number.")
        while True:
            print_menu()
            choice = int(input("Enter your choice: "))


            if choice == 0:
                ex.create_automaton_from_file(path)
            elif choice == 1:
                ex.create_table()
            elif choice == 2:
                ex.display_transition_table()
            elif choice == 3:
                ex.fill_transition_table()
            elif choice == 4:
                ex.standardize()
            elif choice == 5:
                print(f"Result: {ex.max_transitions(1)}")
            elif choice == 6:
                ex.display_table()
            elif choice == 7:
                break
            else:
                print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()