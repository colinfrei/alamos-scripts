import csv
import argparse
from charset_normalizer import detect

# Export from Lodur with these fields: 
# Name, Vorname, Email, Alarmgruppen, Funktionen, Gruppe, Grad

###################################################################################
# Zur Nutzung:
# - Daten von Lodur exportieren (unter Mannschaftslisten, dann Tab 'Info' oben)
# - folgende Felder auswählen:
#   Name, Vorname, Email, Alarmgruppen, Funktionen, Gruppe, Grad
# - als CSV exportieren
#
# - Daten von Alamos als CSV exportieren (unter Adressbuch, Personen, Import/Export)
#
# - ausführen in Terminal (ev. in WSL): 
#   python compare_assignments.py mannschaftslisten.csv fe2_adressbuch.csv
#   einfach beide Dateinamen als Argumente mitgeben, die Reihenfolge sollte nicht
#   relevant sein
# 
###################################################################################


def detect_encoding(file_path):
    """Detect the encoding of a file."""
    with open(file_path, 'rb') as file:
        raw_data = file.read(10000)  # Read the first 10KB of the file
        result = detect(raw_data)
        return result['encoding']


def get_headers(file_path, encoding, delimiter):
    """Get the headers of a CSV file."""
    with open(file_path, mode='r', encoding=encoding) as file:
        reader = csv.reader(file, delimiter=delimiter)
        return next(reader)  # Return the first row (headers)


def identify_file(file_path):
    """Identify whether the file is a Lodur or Alamos file based on headers."""
    # Detect encoding
    encoding = detect_encoding(file_path)

    # Define delimiters
    lodur_delimiter = ','
    alamos_delimiter = ';'

    # Get headers for both possible delimiters
    lodur_headers = get_headers(file_path, encoding, lodur_delimiter)
    alamos_headers = get_headers(file_path, encoding, alamos_delimiter)

    # Define Lodur and Alamos headers
    lodur_expected_headers = {"Name", "Vorname", "E-Mail", "Alarmgruppen", "Funktionen", "Gruppe", "Grad"}
    alamos_expected_start_headers = [
        "Anzeigename", "Nachname", "Vorname", "ISSI", "mobil", "email", "aPagerPro",
        "aPagerPro Registrierung", "aPagerPro Token Provisionierung", "Kommentar",
        "Personalnummer", "Organisations-Admin"
    ]

    # Identify file type
    if lodur_expected_headers.issubset(set(lodur_headers)):
        return "lodur", encoding, lodur_delimiter
    elif alamos_headers[:len(alamos_expected_start_headers)] == alamos_expected_start_headers:
        return "alamos", encoding, alamos_delimiter
    else:
        raise ValueError(f"Could not identify file type for {file_path}. Headers: {lodur_headers} / {alamos_headers}")


def read_csv_file(file_path, key_column, delimiter):
    """Reads a CSV file and returns a dictionary keyed by the primary key column."""
    encoding = detect_encoding(file_path)

    # Read the file
    data = {}
    secondary_data = {}
    with open(file_path, mode='r', encoding=encoding, errors='replace') as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        for row in reader:
            # Combine first and last name as the primary key
            first_name = row.get('Vorname', '').strip()
            last_name = row.get('Nachname', row.get('Name', '')).strip()
            primary_key = f"{first_name} {last_name}"
            data[primary_key] = row

    return data, secondary_data


def validate_alamos_fields(lodur_row):
    """Validate Alamos fields based on Lodur data."""
    alarmgroup_list = [alarmgroup.strip() for alarmgroup in lodur_row['Alarmgruppen'].split(',')]
    group_list = [group.strip() for group in lodur_row['Gruppe'].split(',')]

    # Logic for validation
    validation = {
        "Gruppe 1": 'x' if 'Gruppe 1' in alarmgroup_list else '',
        "Gruppe 2": 'x' if 'Gruppe 2' in alarmgroup_list else '',
        "Gruppe 3": 'x' if 'Gruppe 3' in alarmgroup_list else '',
        "Kommandogruppe": 'x' if 'Kommandogruppe' in alarmgroup_list else '',
        "Atemschutz": 'x' if 'Atemschutz' in alarmgroup_list else '',
        "Konferenzgespräch": 'x' if 'Konferenzgespräch' in alarmgroup_list else '',
        "Notfalltreffpunkte": 'x' if 'Notfalltreffpunkte' in alarmgroup_list else '',
        "Strassenrettung": 'x' if 'Strassenrettung' in alarmgroup_list else '',
        "Verkehrsgruppe": 'x' if 'Verkehrsgruppe' in alarmgroup_list else '',
        "F_Offizier": 'x' if lodur_row['Grad'] in ['Lt', 'Oblt', 'Hptm'] else '',
        "F_Grfhr": 'x' if ('Kader' in group_list and not lodur_row['Grad'] in ['Lt', 'Oblt', 'Hptm']) else '',
        "F_Fahrer": 'x' if 'Chauffeure' in group_list else '',
        "F_B-Fahrer": 'x' if 'B-Fahrer' in group_list else '',
        "F_Sanität": 'x' if 'Sanitätsabteilung' in group_list else '',
        "F_Verkehr": 'x' if 'Verkehrsabteilung' in group_list else '',
        "F_Maschinist": 'x' if 'Maschinisten' in group_list else '',
        "F_Atemschutz": 'x' if 'Atemschutz' in group_list else '',
        "F_Kommando": 'x' if 'Kommandant' in lodur_row['Funktionen'] else '',
    }

    return validation


def compare_csv_files(lodur_data, alamos_data):
    """Compares Lodur and Alamos data and validates specific fields."""
    mismatched_rows = {}

    for name, lodur_row in lodur_data.items():
        if name not in alamos_data:
            mismatched_rows[name] = mismatched_rows.get(name, {})
            mismatched_rows[name]['Missing'] = {"Lodur": "Exists", "Alamos": "Missing"}
        else:
            alamos_row = alamos_data[name]

            # Compare email addresses
            if lodur_row['E-Mail'] != alamos_row['email']:
                mismatched_rows[name] = mismatched_rows.get(name, {})
                mismatched_rows[name]['Email'] = {
                    "Lodur": lodur_row['E-Mail'],
                    "Alamos": alamos_row['email'],
                }

            # Validate Alamos fields based on Lodur data
            expected_alamos_values = validate_alamos_fields(lodur_row)

            for field, lodur_value in expected_alamos_values.items():
                if field in alamos_row and alamos_row[field] != lodur_value:
                    mismatched_rows[name] = mismatched_rows.get(name, {})
                    mismatched_rows[name][field] = {
                        "Lodur": lodur_value,
                        "Alamos": alamos_row[field],
                    }

    for name, alamos_row in alamos_data.items():
        if name not in lodur_data:
            mismatched_rows[name] = mismatched_rows.get(name, {})
            mismatched_rows[name]['Missing'] = {"Lodur": "Missing", "Alamos": "Exists"}

    return mismatched_rows


def print_differences(mismatched_rows):
    """Prints mismatched rows in a clear and concise format."""
    print("\n=== Mismatched Rows ===")
    for name, mismatches in mismatched_rows.items():
        print(f"Name: {name}")
        for field, values in mismatches.items():
            print(f"  Field: {field}")
            print(f"    Lodur: {values['Lodur']}")
            print(f"    Alamos: {values['Alamos']}")


def main():
    parser = argparse.ArgumentParser(description="Compare two CSV files.")
    parser.add_argument("file1", help="Path to the first CSV file.")
    parser.add_argument("file2", help="Path to the second CSV file.")

    args = parser.parse_args()

    # Identify files
    file1_type, _, file1_delimiter = identify_file(args.file1)
    file2_type, _, file2_delimiter = identify_file(args.file2)

    # Ensure correct identification
    if file1_type == file2_type:
        raise ValueError("Both files are of the same type. One should be Lodur and the other Alamos.")

    # Assign the correct email column and delimiter based on file type
    if file1_type == "lodur":
        lodur_file, alamos_file = args.file1, args.file2
        lodur_delimiter, alamos_delimiter = file1_delimiter, file2_delimiter
    else:
        lodur_file, alamos_file = args.file2, args.file1
        lodur_delimiter, alamos_delimiter = file2_delimiter, file1_delimiter

    # Read data from both files
    lodur_data, _ = read_csv_file(lodur_file, "E-Mail", lodur_delimiter)
    alamos_data, _ = read_csv_file(alamos_file, "email", alamos_delimiter)

    # Compare files and validate fields
    mismatched_rows = compare_csv_files(lodur_data, alamos_data)

    # Print results
    print_differences(mismatched_rows)


if __name__ == "__main__":
    main()
