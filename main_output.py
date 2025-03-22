from Automata import *
from contextlib import redirect_stdout
import sys

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
          "║ 8: Recognize the word of the Automaton             ║\n"
          "║ 9: Check if the Automaton recognize your input     ║\n"
          "║ 10: Output the max Transitions from State 1        ║\n"
          "║ 11: Give the complementary of the Automaton        ║\n"
          "║ 12: Give the regular expression of the Automaton   ║\n"
          "║ 13: Get automaton from regular expression          ║\n"
          "╚════════════════════════════════════════════════════╝\n")


class DualOutput:
    """
    A custom class to write to both the console and a file.
    """
    def __init__(self, file):
        self.file = file
        self.console = sys.__stdout__  # Use the original stdout for console output

    def write(self, message):
        # Write to the console using the original stdout
        self.console.write(message)
        # Write to the file
        self.file.write(message)

    def flush(self):
        # Flush both the console and the file
        self.console.flush()
        self.file.flush()


def input_with_log(prompt, file):
    """
    A custom input function that writes the prompt and user input to the file.
    :param prompt: The input prompt to display.
    :param file: The file object to write to.
    :return: The user's input.
    """
    # Write the prompt to the file
    print(prompt, file=file, end="")
    # Display the prompt in the console
    print(prompt, end="")
    # Get user input
    user_input = input()
    # Write the user input to the file
    print(user_input, file=file)
    return user_input


def automate_actions(automaton, file):
    """
    Automate the actions for a given automaton.
    :param automaton: The automaton to test.
    :param file: The file object to write to.
    """
    # List of actions to perform in order
    actions = [6, 7, 2, 3, 4, 10, 11, 12]

    for action in actions:
        if action == 6:  # Test if complete
            print("Testing if automaton is complete...", file=file)
            automaton.is_complete()
        elif action == 7:  # Test if standardized
            print("Testing if automaton is standardized...", file=file)
            automaton.is_standardized()
        elif action == 2:  # Determine the Automaton
            print("Determining the automaton...", file=file)
            automaton = automaton.determine()
            automaton.display_automaton()
        elif action == 3:  # Standardize Automaton
            print("Standardizing the automaton...", file=file)
            automaton.standardize()
            automaton.display_automaton()
        elif action == 4:  # Minimize the Automaton
            print("Minimizing the automaton...", file=file)
            automaton = automaton.minimize()
            automaton.display_automaton()
        elif action == 10:  # Output the max Transitions from State 1
            print("Outputting the max transitions from State 1...", file=file)
            print(f"Result: {automaton.max_transitions(1)}", file=file)
        elif action == 11:  # Give complementary of the Automaton
            print("Giving the complementary of the automaton...", file=file)
            automaton.complementary()
            automaton.display_automaton()

        # Add a separator between actions
        print("\n" + "=" * 50 + "\n", file=file)


def main():
    # Open a file for writing with UTF-8 encoding
    with open("output.txt", "w", encoding="utf-8") as f:
        # Create a DualOutput object
        dual_output = DualOutput(f)

        # Redirect stdout to the DualOutput object
        with redirect_stdout(dual_output):
            # Loop through each automaton (1 to 44)
            for automaton_number in range(1, 45):
                print(f"Testing Automaton {automaton_number}\n", file=f)
                print("=" * 50 + "\n", file=f)

                # Create the automaton
                ex = Automata()
                path = f"Finite_Automata_files/{automaton_number}.txt"
                ex.create_automaton_from_file(path)

                # Automate the actions for this automaton
                automate_actions(ex, f)

                # Print a separator between automata
                print("\n" + "=" * 50 + "\n", file=f)
                print(f"Finished testing Automaton {automaton_number}\n", file=f)

            print("All automata have been tested.", file=f)


if __name__ == "__main__":
    main()