# Trudy-Lynn O.K. Dube | 202102225
# Keletso Joy Ditlhotlhole | 202002023
# Naomi S. Tumaeletse | 202005404

# CSI428 Assignment 2

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

# Word mappings
terminal_mappings = {
    'v': {"gatang", "bonang", "itseng", "thusang", "bofang", "utlwang", "utlweng", "boneng", "amogelang"},
    'n': {"motho", "mosimane", "moruti", "molaodi", "mothusi", "ngwana", "mopalamente", "morui", "mothudi"},
    'l': {"phakela", "bosigo", "motshegare", "mantseboa", "thata"},
    'c₁': {"ba"},
    'c₂': {"ba"},
    'g': {"sa"},
    'c₃': {"yo"},
    'c₄': {"o"},
    'c₅': {"ya"},
    'n₁': {"bana", "batho"}
}


# Grammar Rules
grammar_rules = {
    1: ("L'", ["c₅", "n₁", "C₁", "C₂", "g", "V", "N", "T", "L"]),
    2: ("C₁", ["c₁"]),
    3: ("C₂", ["c₂"]),
    4: ("V", ["v"]),
    5: ("N", ["n", "T"]),
    6: ("N", []),
    7: ("T", ["c₃", "c₄", "g", "V", "N"]),
    8: ("T", []),
    9: ("L", ["l"]),
    10: ("L", [])
}

# Parsing table (includes shift and reduce operations for terminals for every state)
parsing_table = {
    0: {'c₅': 'S1'},
    1: {'n₁': 'S2'},
    2: {'c₁': 'S4'},
    3: {'c₂': 'S6'},
    4: {'c₂': 'R2'},
    5: {'g': 'S7'},
    6: {'g': 'R3'},
    7: {'v': 'S8'},
    8: {'c₃': 'R4', 'n': 'R4', 'l': 'R4', '$': 'R4'},
    9: {'c₃': 'R6', 'n': 'S14', 'l': 'R6', '$': 'R6'},
    10: {'c₃': 'S16', 'l': 'R8', '$': 'R8'},
    11: {'l': 'S13', '$': 'R10'},
    12: {'$': 'R1'},
    13: {'$': 'R9'},
    14: {'c₃': 'S16', 'c₃': 'R8', 'l': 'R8', '$': 'R8'},
    15: {'c₃': 'R5', 'l': 'R5', '$': 'R5'},
    16: {'c₄': 'S17'},
    17: {'g': 'S18'},
    18: {'v': 'S8'},
    19: {'c₃': 'R6', 'n': 'S14', 'l': 'R6', '$': 'R6'},
    20: {'c₃': 'R7', 'l': 'R7', '$': 'R7'}
}

# Transition table for all non terminals
goto_table = {
    0: {"L'": 'Accept'},
    2: {"C₁": 3},
    3: {"C₂": 5},
    7: {"V": 9},
    9: {"N": 10},
    10: {"T": 11},
    11: {"L": 12},
    14: {"T": 15},
    18: {"V": 19},
    19: {"N": 20}
}

# Function to map words to terminals (tokens)
def map_words_to_terminals(sentence):
    tokens = word_tokenize(sentence.lower())
    terminals = []
    ba_count = 0  # Since 'ba' is mapped to more than one terminal, we need to track how many times it appears

    for token in tokens:
        matched = False
        if token == 'ba':
            if ba_count == 0:
                terminals.append('c₁')
                ba_count += 1
            else:
                terminals.append('c₂')
                ba_count = 0 # Reset 'ba' counter back to 0.
            matched = True
        else:
            for terminal, words in terminal_mappings.items():
                if token in words and terminal not in {'c₁', 'c₂'}:
                    terminals.append(terminal)
                    matched = True
                    break

        if not matched:
            print(f"Unknown word in input: '{token}'")
            return None

    return terminals


def handle_conflict(state, current_token, next_token):
    if (next_token == 'c₄'):
        return 'S16'
    else:
        return 'R8'
    
    return None


def parse_input(tokens):
    tokens.append('$')  # Marks end of input string
    stack = [0]  # Initialise stack to begin with start state 0
    i = 0  # Points to current input symbol (token)

    while True:
        state = stack[-1]  
        
        if i < len(tokens):
          current_token = tokens[i] 
        else: 
          current_token = '$'
        
        action = parsing_table.get(state, {}).get(current_token)

        if(current_token == 'c₃' and (action == 'S16' or 'R8')):
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]
            else:
                next_token = '$'  # End of input

            action = handle_conflict(state, current_token, next_token)

        # Print stack with state-symbol pairs
        stack = stack[:]
        print(f"\nCurrent Stack: {stack}")
        print(f"Current Token: {current_token}")
        print(f"Action: {action}")

        if not action:
            print(f"Error: unexpected symbol '{current_token}' at position {i}")
            return False

        if action == 'Accept':
            print("Sentence is ACCEPTED by the grammar.")
            return True

        if action.startswith('S'):
            next_state = int(action[1:]) # Gets the integer value after the 'S'
            stack.append(current_token) # Add current token to stack
            stack.append(next_state) # Add next state to stack
            i += 1

        elif action.startswith('R'):
            rule_number = int(action[1:]) # Gets the integer value after the 'R'
            lhs, rhs = grammar_rules[rule_number] # Obtain the whole production using the grammar rules (LHS is non terminal, RHS is symbols producing that terminal)

            print(f"Reduction:  {lhs} → {' '.join(rhs) if rhs else 'ε'} (R{rule_number})")

            # Pop the top 2 items in the stack to reduce them to 1 non terminal
            for item in rhs:
                stack.pop()  # pops state
                stack.pop()  # pops symbol

            # Get the current state after popping
            state_after_popping = stack[-1]

            # Get the go to state using the newly reduced non terminal
            goto_state = goto_table.get(state_after_popping, {}).get(lhs)
            if goto_state == 'Accept':
                print("Sentence is ACCEPTED by the grammar.")
                return True
            if goto_state is None:
                print("Error: No GO TO transition after reduction.")
                return False

            stack.append(lhs)
            stack.append(goto_state)
        else:
            print("Invalid action encountered.")
            return False


# Testing Parser
sentence1 = "Ya batho ba ba sa thusang ngwana yo o sa bonang mothusi thata" # c₅ n₁ c₁ c₂ g v n c₃ c₄ g v n l (ACCEPTED)
mapped = map_words_to_terminals(sentence1)

if mapped:
  print("\n--------------- Sentence ---------------")
  print("Sentence:", sentence1)
  print("Mapped terminals:", mapped)
  parse_input(mapped)

sentence2 = "Ya batho ba ba thusang ngwana yo o sa bonang mothusi thata" # c₅ n₁ c₁ c₂ v n c₃ c₄ g v n l (NOT ACCEPTED)
mapped = map_words_to_terminals(sentence2)

if mapped:
  print("\n--------------- Sentence ---------------")
  print("Sentence:", sentence2)
  print("Mapped terminals:", mapped)
  parse_input(mapped)
