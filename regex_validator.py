# regex_validator.py

import re

# Define your regex pattern with capture groups
pattern = r'\d\d\.\d\d\.\d\d\d\d \d\d\:\d\d\; ((Nachalarmierung), )?(.*?)?, in (.*?),( (.*?),)? (.*)'

# Define the examples and expected group values
examples = [
    ('15.01.2023 16:08; BMA, in Seon, Oberdorfstrasse 33, Stiftung ABC, Hauptgebäude,', ['BMA', 'Seon', 'Oberdorfstrasse 33', 'Stiftung ABC, Hauptgebäude,']),
    ('06.02.2021 14:21; Brand-Mittel, in Seon, Hansligasse 432, Holzstapel', ['Brand-Mittel', 'Seon', 'Hansligasse 432', Holzstapel'])
]

def validate_examples(pattern, examples):
    compiled_pattern = re.compile(pattern)
    all_passed = True
    for example, expected_groups in examples:
        match = compiled_pattern.match(example)
        if match:
            groups = match.groups()
            # Extract the groups you are interested in (ignore 1st, 2nd, 5th in this case)
            relevant_groups = [groups[2], groups[3], groups[5], groups[6]]  # Adjust indices based on zero-indexing
            if relevant_groups == expected_groups:
                print(f"'{example}' matches the pattern with correct group values: {relevant_groups}")
            else:
                print(f"'{example}' matches the pattern but with incorrect group values: {relevant_groups}")
                all_passed = False
        else:
            print(f"'{example}' does NOT match the pattern.")
            all_passed = False
    
    if not all_passed:
        raise ValueError("Some examples failed to match the expected group values.")

if __name__ == "__main__":
    validate_examples(pattern, examples)
