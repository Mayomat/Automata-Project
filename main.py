from Automata import *

def fauxmain():
    for i in range(43):
        path = 0
        ex = Automata()


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

        print(f"Enter your choice: {i}")
        choice = i
        if True:
            choice = int(choice)
            if 0 < choice < 45:
                path = "Finite_Automata_files/" + str(choice) + ".txt"
            elif choice == 0:
                print("╔════════════════════════════════════════════════════╗\n"
                      "║                       ByeBye                       ║\n"
                      "╚════════════════════════════════════════════════════╝\n")

            else:
                print("Invalid input, please put a valid number")

        else:
            print("Invalid input, please put a valid number")

        for j in range(12):
            if j != 7:
                while j != 12:
                    print_menu()
                    print(f"Enter your choice: {j}")
                    choice = j
                    if True: # verify that it's an int
                        choice = int(choice)
                        if choice == 0:  # Returns to the automaton selection
                            ex = Automata()  # mandatory, or else the memory keeps the previous automata in memory
                            break

                        elif choice == 1:  # Build the Automaton
                            if not build:
                                ex.create_automaton_from_file(path)
                                ex.display_automaton()
                                build = True # this boolean is mandatory or else you can build it infinitely
                                # the states will then be superposed


                            else:
                                print("Your automaton is already built, try another function")

                        elif choice == 2:  # Determine the Automaton
                            if not build:
                                print("Please first build the Automata")
                            else:
                                print("In order to determine the automaton, and for technical purposes, we changed the name\n"
                                      "of the states, the new automaton states and old one are not linked by their names")
                                ex = ex.determine()
                                ex.display_automaton()
                                determined = True

                        elif choice == 3:  # Standardize Automaton
                            if not build:
                                print("Please first build the Automaton")
                            else:
                                ex.standardize()
                                ex.display_automaton()

                        elif choice == 4:  # Minimize the Automaton
                            if not build:
                                print("Please first build the Automaton")
                            else:
                                ex = ex.minimize()
                                ex.display_automaton()
                                determined = True # same as built, else it superposed itself

                        elif choice == 5:   # Test if deterministic
                            if not build:
                                print("Please first build the Automaton")
                            else:
                                ex.is_deterministic()

                        elif choice == 6:   # Test if complete
                            if not build:
                                print("Please first build the Automaton")
                            else:
                                ex.is_complete()

                        elif choice == 7:   # Test if standardized
                            if not build:
                                print("Please first build the")
                            else:
                                ex.is_standardized()

                        elif choice == 8:  # Check if the Automaton recognise your input
                            if not build:
                                print("Please first build or determine the automaton")
                            else:
                                ex.word_recognition()

                        elif choice == 9:   # Output the max Transitions from State 1
                            if not build or not determined:
                                print("Please first build or determine the automaton")
                            else:
                                print(f"Result: {ex.max_transitions(1)}")

                        elif choice == 10:   # Give complementary of the Automaton
                            if not build:
                                print("Please first build the automaton")
                            else:
                                ex.complementary()
                                ex.display_automaton()

                        elif choice == 11:
                            if not build:
                                print("Please first build the automaton")
                            else:
                                print("Automaton regEx : "+ex.getRegExExpression())

                        elif choice == 12:
                            ex = Automata()
                            ex.create_automaton_from_regEx(input("Enter the desired regular expression :\n"))
                            ex.display_automaton()
                            build = True

                        else:
                            print("Invalid input, please put a valid number")
                        #print("Press Enter to continue")
                        #input()
                    else:
                        print("Invalid input, please put a valid number")


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
          "║ 5: Test if deterministic                           ║\n"
          "║ 6: Test if complete                                ║\n"
          "║ 7: Test if standardized                            ║\n"
          "║ 8: Check if the Automaton recognise your input     ║\n"
          "║ 9: Output the max Transitions from State 1         ║\n"
          "║ 10: Give the complementary of the Automaton        ║\n"
          "║ 11: Give the regular expression of the Automaton   ║\n"
          "║ 12: Get automaton from regular expression          ║\n"
          "╚════════════════════════════════════════════════════╝\n")



if __name__ == "__main__":
    fauxmain()
