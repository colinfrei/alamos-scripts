# regex_validator.py

import re

# Define your regex pattern with capture groups
pattern = r'\d\d\.\d\d\.\d\d\d\d \d\d\:\d\d\; ((Nachalarmierung), )?(.*?)?, in (.*?),( (.*?),)? (.*)'

# Define the examples and expected group values
examples = [
    ('15.01.2023 16:08; BMA, in Seon, Oberdorfstrasse 33, Stiftung ABC, Hauptgebäude,', ['BMA', 'Seon', 'Oberdorfstrasse 33', 'Stiftung ABC, Hauptgebäude,']),
    ('06.02.2021 14:21; Brand-Mittel, in Seon, Hansligasse 432, Holzstapel', ['Brand-Mittel', 'Seon', 'Hansligasse 432', 'Holzstapel'])
    ('08.06.2023 15:06; Nachalarmierung, in Seon, Holdernweg, EFH,  Einrücken ins Magazin', ['Nachalarmierung', 'Seon', 'Holdernweg', 'EFH,  Einrücken ins Magazin'])
    ('24.03.2021 20:50; Nachalarmierung, Verkehrsregelung, in Lenzburg - Seon, bei FW Lenzburg Muster Hans melden.', ['Verkehrsregelung', 'Seon', 'bei FW Lenzburg Muster Hans melden'])
    ('07.02.2022 21:49; Brand-Gross, in Seon, Seetalstrasse, vis-à-vis Landi,  Brand in grossem leerstehenden Gebäude', ['Brand-Gross', 'Seon', 'Seetalstrasse', 'vis-à-vis Landi,  Brand in grossem leerstehenden Gebäude'])
    ('09.04.2023 08:01; Brand-Klein, in Seon, Ortsgebiet Seon,  PW-Barand zwischen Hallwil und Seon', ['Brand-Klein', 'Seon', 'Ortsgebiet Seon', 'PW-Barand zwischen Hallwil und Seon'])
    ('06.06.2006 16:36; Abklärung, in Egliswil, Schulstrasse 2, 06 Schule,  ', ['Abklärung', 'Egliswil', 'Schulstrasse 2', '06 Schule,  '])
    ('25.05.2020 09:44; Strassenrettung, in Seon, Iglisten 1, Höhe Max Hauri,  Verkehrsunfall', ['Strassenrettung', 'Seon', 'Iglisten 1', 'Höhe Max Hauri,  Verkehrsunfall'])
    ('17.07.2018 11:33; Techn. Hilfeleistung, in Seon, Ortsgebiet Seon,  Ölspur Seetalstrasse, Treffpunkt Feuerwehrmagazin', ['Techn. Hilfeleistung', 'Seon', 'Ortsgebiet Seon', 'Ölspur Seetalstrasse, Treffpunkt Feuerwehrmagazin'])
    ('25.02.2019 20:00; Elementarereignis, in Seon,  Reussgasse, Baum über Strasse.', ['Elementarereignis', 'Seon', 'Reussgasse', 'Baum über Strasse.'])
    ('15.05.2015 18:45; Probealarm, FW Seon-Egliswil, ', ['Probealarm', '', '', ''])
    ('22.08.2021 21:00; Nachalarmierung, Seetalstrase 5, Lenzburg, Atemschutz Modul 5, ADL Brandbekämpfung, Einrücken Magazin', ['Nachalarmierung', '', 'Seetalstrasse 5', 'Lenzburg, Atemschutz Modul 5, 'ADL Brandbekämpfung, Einrücken Magazin'])
    ('12.12.2023 17:21; Oel-, Benzin-, Chemie, in Seon, Birren 2,  grosse Menge auslaufende Phosphorsäure.', ['Oel-, Benzin-, Chemie', 'Seon', 'Birren 2', ' grosse Menge auslaufende Phosphorsäure.'])

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
