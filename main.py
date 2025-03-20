from Automata import *

def print_menu():
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║                AUTOMATON CONSOLE MENU              ║")
    print("╠════════════════════════════════════════════════════╣")
    print("║ 0: Build the Automaton                             ║")
    print("║ 1: Determine the Automaton                         ║")
    print("║ 2: Standardize Automaton                           ║")
    print("║ 3: Minimaze the Automaton                          ║")
    print("║ 4: Recognize the word of the Automaton             ║")
    print("║ 5: Search if the Automaton recognize the inputed   ║")
    print("║ 6: Output the max Transitions from State 1         ║")
    print("║ 7: Return to the automaton selection               ║")
    print("╚════════════════════════════════════════════════════╝")

def main():
    ex = Automata()

    while True:

        # Here we create variables and not use is_deterministic or else to check the automata otherwise it will create error checking
        # something that is not build
        Build = False
        Determined = False

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
                ex.create_table()
                ex.fill_transition_table()
                ex.display_table()
                Build = True
            elif choice == 1:
                if not Build:
                    print("Please first Build the Automata")
                else:
                    ex.determine()
                    ex.fill_transition_table()
                    ex.display_table()
                    Determined = True
            elif choice == 2:
                if not Determined:
                    print("Please first Determine the Automata")
                else:
                    ex.standardize()
                    ex.display_table()
            elif choice == 3 and Determined:
                if not Determined:
                    print("Please first Determine the Automata")
                else:
                    ex.minimize()
                    ex.display_table()
            elif choice == 4:
                if not Build or not Determined:
                    print("Please first build or determine the automata")
                else :
                    word = input("What word do you want to be tested in the automata : ")
                    if ex.recognize_word(word):
                        print("Yes the Automata recognized the word " + word)
                    else:
                        print("No the Automata does not recognized the word" + word)
            elif choice == 5:
                if not Build or not Determined:
                    print("Please first build or determine the automata")
                else :
                    ex.word_recognition()
            elif choice == 6:
                if not Build or not Determined:
                    print("Please first build or determine the automata")
                else :
                    print(f"Result: {ex.max_transitions(1)}")
            elif choice == 7:
                break
            else:
                print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()