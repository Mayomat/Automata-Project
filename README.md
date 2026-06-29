# ⚙️ Automata-Project - Finite Automata Operations Engine

![Algorithms](https://img.shields.io/badge/Category-Algorithms%20%26%20Data%20Structures-blue)
![Language](https://img.shields.io/badge/Language-C%20%2F%20C%2B%2B%20%2F%20Python%20%2F%20Java-green)
![Academic](https://img.shields.io/badge/Coursework-EFREI%20Project-red)

> **Source Code Repository:** [github.com/msirier/Automata-Project](https://github.com/msirier/Automata-Project)

## 📖 Project Overview
This project is an advanced **Finite Automata (FA) Processing Engine** designed to read, analyze, transform, and evaluate formal languages using structural finite state machines. 

The application implements core computer science concepts including state machine validation, standardization, determinization, completion, partition-based minimization, and string token recognition. It features an interactive command-line loop that allows users to process multiple automata seamlessly without restarting the application.

---

## 🎯 Features & Project Milestones

### 🧱 Core Functionality 
- [x] **File Parsing & Storage:** Dynamic loading of finite automata from formatted `.txt` files into tailored in-memory data structures.
- [x] **Aligned Matrix Display:** Outputs clean, beautifully aligned transition tables explicitly identifying initial (`→`) and terminal (`←`) states.
- [x] **Automata Analysis:** Auto-detects and reports whether a loaded FA is:
  * Deterministic
  * Complete
  * Standard
- [x] **Standardization:** Transforms non-standard automata into standard equivalents on demand.
- [x] **Determinization & Completion:** Converts Non-Deterministic Finite Automata (NFA) into Complete Deterministic Finite Automata (CDFA) using textbook subset construction algorithms.

### 🚀 Advanced Features
- [x] **Minimization (MCDFA):** Optimizes CDFAs into Minimal CDFAs using sequential partition groups, showing step-by-step group updates.
- [x] **Word Recognition Testing:** Simulates input string validation loops over the generated state machines to check for language acceptance.
- [x] **Complementary Language Engine:** Constructs an automaton that recognizes the exact complement of the primary language.

---

## 📄 Automaton File Syntax (`.txt`)
The engine reads state machines from plain text files adhering to a strict index convention (alphabet characters `a-z`, states numbered sequentially starting from `0`).

### File Template Structure
```text
Line 1: Number of symbols in the alphabet (e.g., 2 implies {a, b})
Line 2: Total number of states
Line 3: Number of initial states, followed by their numeric labels
Line 4: Number of final states, followed by their numeric labels
Line 5: Total number of transition rules
Lines 6+: Transition definitions formatted as <source_state><symbol><target_state>

```

### Practical Example (`animate.txt`)

For an alphabet of 2 symbols (`a, b`), 5 states, 1 initial state (`0`), 1 final state (`4`), and 6 distinct transitions:

```text
2
5
1 0
1 4
6
0a0
0b0
0a1
1b2
2a3
3a4

```

---

## 🧠 Core Algorithmic Details

### State Tracking & Subsets

When converting an NFA to a CDFA, macro-states are dynamically labeled to transparently show their origin composition (e.g., sub-states `{1, 2, 3}` collapse into a clear compound state string `1.2.3`).

### Minimization Traces

The minimization module outputs successive partitions explicitly, mapping the newly structured minimal state names back to their original macro-state origins via a clean lookup layout.

> ⚠️ **Algorithmic Guardrails:** In strict compliance with operational limits, the engine guards against redundancy. For instance, launching a determinization process on an already deterministic state machine will actively throw an explanatory notice rather than executing out-of-context routines.

---

## 💻 How to Run the Program

### Running Interactively

1. Clone the project:
```bash
git clone [https://github.com/msirier/Automata-Project.git](https://github.com/msirier/Automata-Project.git)
cd Automata-Project

```


2. Compile and execute the main controller file using your respective language environment framework.
3. Use the runtime interface to load automated text matrices by typing their target test numbers (e.g., inputting `8` maps straight to loading `test_fa_8.txt`).

### String Testing Loop

When evaluating word strings on the loaded machine, type input combinations sequentially. To exit the tracking evaluation layer and return to the main configuration setup, type:

```text
end

```

---

## 📂 Project Structure

```text
📦 Automata-Project
├── 📂 test_automata/     # Collection of target text files (.txt) mapping state machines
├── 📂 documentation/     # PDF slides and system layout charts 
├── 📂 execution_traces/  # Generated .txt logs mirroring standard out console runs
│
├── ⚙️ Core Engines
│   ├── parser_loader     # Handles data input validation and matrix generation
│   ├── properties_chk    # Scans for complete, deterministic, and standard statuses
│   ├── transformation    # Code processing standardization and CDFA conversion
│   ├── minimization      # State partition consolidation and lookup mapping
│   └── recognizer        # Full string processing sequence evaluation loop
│
└── 📄 main               # Main application hub loop

```

---


