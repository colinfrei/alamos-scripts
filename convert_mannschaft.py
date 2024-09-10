import csv
import argparse

# Export from Lodur with these fields: 
# Name, Vorname, Email, Alarmgruppen, Funktionen, Gruppe, Grad

###################################
# Zur Nutzung:
# - Daten von Lodur exportieren (unter Mannschaftslisten, dann Tab 'Info' oben)
# - folgende Felder exportieren:
#   Name, Vorname, Email, Alarmgruppen, Funktionen, Gruppe, Grad
# - Script anpassen
#   - Variablen input_file und output_file anpassen
#   - Feldlisten für Alarmgruppen und Funktionen anpassen, ggf. Logik anpassen
# - ausführen in Terminal (ev. in WSL): python convert_mannschaft.py
# 
# - Script kann mit --test ausgeführt werden, um die Email-Adressen so anzupassen,
#   dass keine Emails versandt werden (@example.com)
#
##################################


# Input and output file paths
input_file = 'mannschaftslisten.csv'
output_file = 'transformed_mannschaftslisten.csv'

# Define the function to transform the input data
def transform_data(input_file, output_file, test_mode=False):
    # Open the input CSV file for reading with ISO-8859-1 encoding
    with open(input_file, mode='r', encoding='ISO-8859-1') as infile:
        reader = csv.DictReader(infile)
        
        # Define the output field names
        fieldnames = [
            "Anzeigename", "Nachname", "Vorname", "ISSI", "mobil", "email", "aPagerPro", "aPagerPro Registrierung", 
            "aPagerPro Token Provisionierung", "Kommentar", "Personalnummer", "Organisations-Admin", "externalDbId", 
            
            # Alarmgruppen
            "Gruppe 1", "Gruppe 2", "Gruppe 3", "Kommandogruppe", "Atemschutz", "Konferenzgespräch", "Notfalltreffpunkte", "Strassenrettung", "Verkehrsgruppe",
            # Funktionen
            "F_Grfhr", "F_Fahrer", "F_Offizier", "F_B-Fahrer", "F_Sanität", "F_Verkehr", "F_Maschinist", "F_Atemschutz", "F_Kommando",
            
            "NOTIF_VIA_APAGER", "NOTIF_VIA_EMAIL", "NOTIF_NEW_PERSON", 
            "NOTIF_NEW_ROADBLOCK", "NOTIF_NEW_VEHICLEFAULT", "NOTIF_PROGRESS_VEHICLEFAULT", "NOTIF_NEW_SIRENFAULT", 
            "NOTIF_NEW_OBJECT_SHARED", "NOTIF_NEW_OBJECT_FEEDBACK", "NOTIF_NEW_REPORT", "NOTIF_NEW_AVAILABILITY", 
            "NOTIF_LINKED_VEHICLE_STATUS_CHANGE", "NOTIF_SERVERSTART", "NOTIF_MASTER_SLAVE", "NOTIF_LICENSE_INVALID", 
            "NOTIF_INPUT_CHANGE"
        ]
        
        # Open the output CSV file for writing with UTF-8 encoding
        with open(output_file, mode='w', newline='', encoding='ISO-8859-1') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_ALL, delimiter=';')
            writer.writeheader()
            
            # Process each row of the input CSV
            for row in reader:
                anzeigename = f"{row['Name']} {row['Vorname']}"
                nachname = row['Name']
                vorname = row['Vorname']
                
                email = row['E-Mail']
                if test_mode:
                    email = email.replace('@', '__').replace('.', '_') + '@example.com'
                
                alarmgroup_list = [alarmgroup.strip() for alarmgroup in row['Alarmgruppen'].split(',')]
                gruppe_1 = 'x' if 'Gruppe 1' in alarmgroup_list else ''
                gruppe_2 = 'x' # nicht explizit gesetzt
                gruppe_3 = 'x' if 'Gruppe 3' in alarmgroup_list else ''
                gruppe_kommando = 'x' if 'Kommandogruppe' in alarmgroup_list else ''
                gruppe_atemschutz = 'x' if 'Atemschutz' in alarmgroup_list else ''
                gruppe_konferenzgespraech = 'x' if 'Konferenzgespräch' in alarmgroup_list else ''
                gruppe_ntp = 'x' if 'Notfalltreffpunkte' in alarmgroup_list else ''
                gruppe_strassenrettung = 'x' if 'Strassenrettung' in alarmgroup_list else ''
                gruppe_verkehr = 'x' if 'Verkehrsgruppe' in alarmgroup_list else ''

                group_list = [group.strip() for group in row['Gruppe'].split(',')]
                f_of = 'x' if row['Grad'] in ['Lt', 'Oblt', 'Hptm'] else ''
                f_grfhr = 'x' if ('Kader' in group_list and not f_of) else ''
                f_fahrer = 'x' if 'Chauffeure' in group_list else ''
                f_bfahrer = 'x' if 'B-Fahrer' in group_list else ''
                f_sanitaet = 'x' if 'Sanitätsabteilung' in group_list else ''
                f_verkehr = 'x' if 'Verkehrsabteilung' in group_list else ''
                f_maschinist = 'x' if 'Maschinisten' in group_list else ''
                f_atemschutz = 'x' if 'Atemschutz' in group_list else ''
                f_kommando = 'x' if 'Kommandant' in row['Funktionen'] else ''
                
                # Create the output row
                output_row = {
                    "Anzeigename": anzeigename,
                    "Nachname": nachname,
                    "Vorname": vorname,
                    "ISSI": "",
                    "mobil": "",
                    "email": email,
                    "aPagerPro": "",
                    "aPagerPro Registrierung": "TOKEN",
                    "aPagerPro Token Provisionierung": "",
                    "Kommentar": "",
                    "Personalnummer": "",
                    "Organisations-Admin": "",
                    "externalDbId": "",
                    # Alarmgruppen
                    "Gruppe 1": gruppe_1,
                    "Gruppe 2": gruppe_2,
                    "Gruppe 3": gruppe_3,
                    "Kommandogruppe": gruppe_kommando,
                    "Atemschutz": gruppe_atemschutz,
                    "Konferenzgespräch": gruppe_konferenzgespraech,
                    "Notfalltreffpunkte": gruppe_ntp,
                    "Strassenrettung": gruppe_strassenrettung,
                    "Verkehrsgruppe": gruppe_verkehr,

                    # Funktionen
                    "F_Offizier": f_of,
                    "F_Grfhr": f_grfhr,
                    "F_Fahrer": f_fahrer,
                    "F_B-Fahrer": f_bfahrer,
                    "F_Sanität": f_sanitaet,
                    "F_Verkehr": f_verkehr,
                    "F_Maschinist": f_maschinist,
                    "F_Atemschutz": f_atemschutz,
                    "F_Kommando": f_kommando,
                    
                    "NOTIF_VIA_APAGER": "false",
                    "NOTIF_VIA_EMAIL": "false",
                    "NOTIF_NEW_PERSON": "false",
                    "NOTIF_NEW_ROADBLOCK": "false",
                    "NOTIF_NEW_VEHICLEFAULT": "false",
                    "NOTIF_PROGRESS_VEHICLEFAULT": "false",
                    "NOTIF_NEW_SIRENFAULT": "false",
                    "NOTIF_NEW_OBJECT_SHARED": "false",
                    "NOTIF_NEW_OBJECT_FEEDBACK": "false",
                    "NOTIF_NEW_REPORT": "false",
                    "NOTIF_NEW_AVAILABILITY": "false",
                    "NOTIF_LINKED_VEHICLE_STATUS_CHANGE": "false",
                    "NOTIF_SERVERSTART": "false",
                    "NOTIF_MASTER_SLAVE": "false",
                    "NOTIF_LICENSE_INVALID": "false",
                    "NOTIF_INPUT_CHANGE": "false"
                }
                
                # Write the output row to the CSV
                writer.writerow(output_row)

# Define the main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description='Transform the CSV file.')
    parser.add_argument('--test', action='store_true', help='Rewrite all emails to example.com domain')
    args = parser.parse_args()
    
    # Transform the data with the specified options
    transform_data(input_file, output_file, test_mode=args.test)

# Run the main function
if __name__ == '__main__':
    main()
