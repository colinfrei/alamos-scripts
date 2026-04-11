# MoKoS JSON Alarm via Email
Das Alarmierungssystem MoKoS hat die Möglichkeit, eine Alarmierung per Email zu senden, mit den Alarmdaten als JSON-Anhang.
Dies ist die Anleitung, wie diese JSON-Alarmdaten in Alamos genutzt werden können.

![Schematische Darstellung des Alarmierungsablaufs](/mokos_email/mokos_alamos_ablauf.png)


## Konfiguration
### 1. Vorbereitung
Für die Authentisierung wird ein Key benötigt, der an zwei Orten hinterlegt werden muss (in den Schritten 2 und 6).
Generiere dafür einen zufälligen String, zB [mit diesem Tool](https://www.random.org/strings/?num=1&len=32&digits=on&upperalpha=on&loweralpha=on&unique=on&format=html&rnd=new).

Du benötigst auch die Einheit-Nr. deiner Feuerwehr aus MoKoS. Du findest diese wenn du unter https://feuerwehralarmierung.ag.ch (oder vergleichbare MoKoS Web-Seite anderer Regionen) auf die Einheit klickst.

![Einheit-Nr in MoKoS](/mokos_email/mokos_einheit_nr.png)

### 2. Batch Script anpassen und auf Server ablegen
Öffne das Batch Script '[mokos_transform_json.bat](/mokos_email/mokos_transform_json.bat)' in einem Texteditor, und passe die Werte für _orgId_ und _authKey_ mit den Werten aus Schritt 1 an.

Lege die angepasste Datei auf dem Alamos-Server ab, im Ordner _C:\ProgramData\Alamos GmbH\FE2\Config\_.

Je nach Alamos-Setup muss der HTTP-Aufruf am Ende des Batch Files angepasst werden (zB Port).

### 3. Mail-Verarbeitungs Einheit erstellen
Lege in Alamos, unter 'Einheiten', eine neue Einheit mit dem Namen 'MoKoS Mail-Eingang' an.
Öffne diese, und importiere die Datei '[mokos_mail_eingang.json](/mokos_email/mokos_mail_eingang.json)'.

![Screenshot von MoKoS Mail Eingang Einheit in Alamos](/mokos_email/mokos_mail_eingang_einheit.png)

Je nach Alamos-Setup müssen ggf. die Pfade unter 'Datei einlesen' und 'Batch/Shell-Skripte' angepasst werden.

### 4. Alarmierungs-Einheit erstellen
Lege in Alamos, unter 'Einheiten', eine neue Einheit mit dem Namen 'MoKoS Alarmierung' an.
Öffne diese, und importiere  die Datei '[mokos_alarmierung.json](/mokos_email/mokos_alarmierung.json)'.

![Screenshot von MoKoS Alarmierung Einheit in Alamos](/mokos_email/mokos_alarmierung_einheit.png)

Passe diese Einheit nach deinen Alarmierungswünschen an.

Der Alarm hat im Feld `alarmGroups` eine Liste der alarmierten Gruppen der eigenen Feuerwehr. Die Gruppen sind so wie sie von der KNZ übermittelt werden, aktuell kennen wir diese möglichen Werte:
- Gruppe 1 (_ID: 1_)
- Gruppe 2 (_ID: 2_)
- Gruppe 3 (_ID: 50_)
- Gruppe 4 (_ID: 111_)
- Kommandogruppe (_ID: 3_)
- Kommandogruppe 2 (_ID: 20_)
- Atemschutz (_ID: 4_)
- Verkehrsgruppe (_ID: 5_)
- Konferenzgespräch (_ID: 6_)
- Sanitätsgruppe (_ID: 9_)
- Strassenrettung (_ID: 53_)
- Gruppe HRF (_ID: 200_)
- Gruppe MGV (_ID: 428_)
- Notfalltreffpunkte (_ID: 468_)

Zusätzlich werden im Feld `alarmGroupsOther` die aufgebotenen Gruppen der Nachbarfeuerwehren aufgelistet, jeweils mit dem Prefix der Feuerwehr (zB _FW Seon-Egliswil: Gruppe 1_).

Mit dem Whitelist-Plugin kann geprüft werden, ob eine Alarmgruppe alarmiert wurde, indem im Feld Wortliste die ID der Gruppe eingetragen wird, und im Feld 'Quelle' im Tab 'Optionales' der Wert _alarmGroupsIds_.

### 5. Anlegen Mail-Alarmeingang
Füge in Alamos, unter 'Administration -> Alarmeingang', einen neuen Alarmeingang vom Typ [Mail-Überwachung](https://alamos-support.atlassian.net/wiki/spaces/documentation/pages/219480356/Mail-+berwachung) hinzu.
Konfiguriere diesen, neben der Konfiguration der Email-Daten, mit folgenden Werten:
- Reiter 'Sicherheit'
  - Erlaubte Absender-Email: 'feuerwehralarmstelle@kapo.ag.ch' (bis 20.4.2026: 'kfa@die-agv.ch') eintragen
- Reiter 'Alarmierung'
  - Standard-Einheit 'MoKoS Mail-Eingang' wählen
  - Zu alarmierende Einheit wählen: Über Betreff
- Reiter 'Anhänge'
  - 'Anhänge verarbeiten' ankreuzen
  - 'Anhänge und Inhalt separat speichern' ankreuzen
- Reiter 'Erlaubte Einheiten'
  - Erlaubte Einheit 'MoKos Mail-Eingang' ankreuzen

### 6. Anlegen Schnittstelle-Alarmeingang
Füge in Alamos, unter 'Administration -> Alarmeingang', einen neuen Alarmeingang vom Typ [Externe Schnittstelle](https://alamos-support.atlassian.net/wiki/spaces/documentation/pages/219480366/Externe+Schnittstelle) hinzu.
Konfiguriere diesen mit folgenden Werten:
- Reiter 'Einstellungen'
  - Version Datenformat: v2
  - Gültige Absender: Key aus Schritt 1 einfügen
  - Checkbox _Patientendaten in Alarmaktualisierung einbeziehen_ ankreuzen (siehe technische Details unten)
- Reiter 'Alarmierung'
  - Standard-Einheit 'MoKoS Alarmierung' wählen
- Reiter 'HTTP'
  - 'HTTP POST' ankreuzen
- Reiter 'Erlaubte Einheiten'
  - Erlaubte Einheit 'MoKoS Alarmierung' ankreuzen

## Technische Details
### Patienten-Daten?
Alamos [aktualisiert nur bestimmte Felder](https://alamos-support.atlassian.net/wiki/spaces/documentation/pages/219480366/Externe+Schnittstelle#Parameter%2C-die-f%C3%BCr-eine-Einsatzaktualisierung-ber%C3%BCcksichtigt-werden) in einem Alarm, und das Feld welches wir für die Alarmgruppen nutzen ist nicht dabei. Um trotzdem Aktualisierungen zu ermöglichen, werden die IDs der Alarmgruppen zusätzlich in die Patienteninfos gespeichert, da diese aktualisiert werden. 
Die Liste der Alarmgruppen in Text-Form wird aktuell nicht aktualisiert

### Matching in Einheit
Da Alarmgruppen überlappende Namen haben können (zB _Kommandegruppe_ vs _Kommandogruppe 2_) kann das Whitelist-Plugin nicht nur mit dem Begriff verwendet werden. Stattdessen wird mit einer Regular Expression in diesem Format gematched: `(?:^|\r?\n)3(?=\r?\n|$)`

Diese setzt sich zusammen aus:
- `(?:^|\r?\n)` - Anfang der Zeile oder Anfang des Feld-Textes
- `3` - ID der Alarmgruppe
- `(?=\r?\n|$)` - Ende der Zeile oder Ende des Feld-Textes

### Beispiel-Alarme
Im Ordner _examples_ sind verschiedene Beispiele von Anhängen der MoKoS-Email abgelegt. Sie sind hier für bessere Lesbarkeit schön formatiert, im tatsächlichen Email fehlen die Zeilenumbrüche und Einrückungen.
Beispiele (u.A.):
- `probealarm.json` - mehrere Gruppen, ohne Caller, ohne Koordinaten
- `kommandogruppe.json` - Pagertext enthält auch Textbausteine die sonst nicht vorkommen ('Baum über Strasse')
- TODO: Nachbarfeuerwehr
- TODO: Nachalarmierung

## Weiteres
- Anleitung geschrieben basierend auf Alamos Version 2.38.245
- Offene Punkte:
  - Erkennen von Alarmübungen (AlertExercise?)
  - Erkennen von Nachalarmierungen (Alarmcount? // relevant?)
  - Spezielle Handhabung BMA
  - Unwetteralarme
  - Objektdispositive?

## Changelog
### 2025-12-12: Alarme ohne Koordinaten
Alarme ohne Koordinaten (zB Probealarm) werden jetzt korrekt gehandhabt.
Um zu aktualisieren muss
- die `mokos_transform_json.bat` Datei ersetzt werden
### 2025-11-05: UTF-8 Verbesserung
Bessere Handhabung von UTF-8, damit Wörter wie 'Abklärung' korrekt verarbeitet werden.
Um zu aktualisieren muss
- die `mokos_transform_json.bat` Datei ersetzt werden
- in der `MoKoS Mail Eingang` Einheit im `Datei einlesen` Plugin die Checkbox _UTF-8 Encoding_ angekreuzt werden
