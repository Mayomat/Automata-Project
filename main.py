from Automata import *

def print_menu():
    print("\n")
    print("╔════════════════════════════════════════════════════╗\n"
          "║               AUTOMATON CONSOLE MENU               ║\n"
          "╠════════════════════════════════════════════════════╣\n"
          "║ 0: Return to the automaton selection               ║\n"
          "║ 1: Build the Automaton                             ║\n"
          "║ 2: Determine the Automaton                         ║\n"
          "║ 3: Standardize Automaton                           ║\n"
          "║ 4: Minimize the Automaton                          ║\n"
          "║ 5: Recognize the word of the Automaton             ║\n"
          "║ 6: Check if the Automaton recognise your input     ║\n"
          "║ 7: Output the max Transitions from State 1         ║\n"
          "║ 8: Give the complementary of the Automaton         ║\n"
          "║ 9: Give the regular expression of the Automaton    ║\n"
          "║ 10: Get automaton from regular expression          ║\n"
          "╚════════════════════════════════════════════════════╝\n")


def main():
    ex = Automata()

    while True:

        # Here we create variables and not use is_deterministic or else to check the automata
        # otherwise it will create error checking
        # something that is not build
        build = False
        determined = False

        print("╔════════════════════════════════════════════════════╗\n"
              "║               AUTOMATON CONSOLE MENU               ║\n"
              "╠════════════════════════════════════════════════════╣\n"
              "║ Enter the number of the automaton that you want,   ║\n"
              "║ From 1 to 44 and O to exit                         ║\n"
              "╚════════════════════════════════════════════════════╝\n")

        choice = input("Enter your choice: ")
        if choice.isdigit():
            choice = int(choice)
            if 0 < choice < 45:
                path = "Finite_Automata_files/" + str(choice) + ".txt"
            elif choice == 0:
                print("╔════════════════════════════════════════════════════╗\n"
                      "║                       ByeBye                       ║\n"
                      "╚════════════════════════════════════════════════════╝\n")
                break
            else:
                print("Invalid input, please put a valid number")
                continue
        else:
            print("Invalid input, please put a valid number")
            continue

        while True:
            print_menu()
            choice = input("Enter your choice: ")
            if choice.isdigit():
                choice = int(choice)
                if choice == 0:  # Returns to the automaton selection
                    ex = Automata()  # mandatory, or else the memory keeps the previous automata in memory
                    break

                elif choice == 1:  # Build the Automaton
                    if not build:
                        ex.create_automaton_from_file(path)
                        ex.display_table()
                        build = True


                    else:
                        print("Your automaton is already built, try another function")

                elif choice == 2:  # Determine the Automaton
                    if not build:
                        print("Please first build the Automata")
                    else:
                        print("In order to determine the automaton, and for technical purposes, we changed the name\n"
                              "of the states, the new automaton states and old one are not linked by their names")
                        ex = ex.determine()
                        ex.display_table()
                        determined = True
                        #print()

                elif choice == 3:  # Standardize Automaton
                    if not build:
                        print("Please first build the Automaton")
                    else:
                        ex.standardize()
                        ex.display_table()

                elif choice == 4:  # Minimize the Automaton
                    if not build:
                        print("Please first build the Automaton")
                    else:
                        ex = ex.minimize()
                        ex.display_table()
                        determined = True

                elif choice == 5:  # Recognize the word of the Automaton
                    if not build:
                        print("Please first build the automaton")
                    else:
                        word = input("What word do you want to be tested in the automaton : ")
                        if ex.recognize_word(word):
                            print("Yes the Automaton recognized the word " + word)
                        else:
                            print("No the Automaton does not recognized the word" + word)

                elif choice == 6:  # Check if the Automaton recognise your input
                    if not build:
                        print("Please first build or determine the automaton")
                    else:
                        ex.word_recognition()

                elif choice == 7:   # Output the max Transitions from State 1
                    if not build or not determined:
                        print("Please first build or determine the automaton")
                    else:
                        print(f"Result: {ex.max_transitions(1)}")

                elif choice == 8:   # Give complementary of the Automaton
                    if not build:
                        print("Please first build the automaton")
                    else:
                        ex.complementary()
                        ex.display_table()

                elif choice == 9:
                    if not build:
                        print("Please first build the automaton")
                    else:
                        print("Automaton regEx : "+ex.getRegExExpression())

                elif choice == 10:
                    ex = Automata()
                    ex.create_automaton_from_regEx(input("Enter the desired regular expression :\n"))
                    ex.display_table()
                    build = True

                else:
                    print("Invalid input, please put a valid number")
                print("Press Enter to continue")
                input()
            else:
                print("Invalid input, please put a valid number")


if __name__ == "__main__":
    main()
