# alamos-scripts
Alamos Scripts, genutzt von der Feuerwehr Seon-Egliswil, mit Lodur / MoKoS

## MoKoS Alarmierung via Email
Die Alarmierung via Email bietet am meisten Informationen.  
[Anleitung im Ordner mokos_email](mokos_email/README.md)

## MoKoS Alarmierung via SMS
Die Alarmierung via SMS importiert das SMS, wie es jeder Alarmierte erhält.  
[Anleitung im Ordner mokos_sms](mokos_sms/README.md)

## convert_mannschaft.py
Wandelt den CSV-Export aus Lodur um, damit er in Alamos importiert werden kann  
Hilfsdateien: [example_mannschaftslisten.csv](example_mannschaftslisten.csv) (Input), [example_transformed_mannschaftslisten.csv](example_transformed_mannschaftslisten.csv) (Output)

## Lodur Kalender-Import
Grundsätzliches Vorgehen: Google Kalender erstellen, Termine mit Import/Export in diesen importieren (mit Feed URL aus Lodur Übersichtsseite), "geheime" iCal URL aus Google Calendar kopieren und in Alamos in iCal Kalender hinterlegen.
Muss jeweils gemacht werden wenn neue Termine hinzugefügt werden, bei uns ein mal im Jahr.
