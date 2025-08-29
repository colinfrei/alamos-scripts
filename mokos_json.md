# MoKoS JSON Alarm via Email
Das Alarmierungssystem MoKoS hat die Möglichkeit, eine Alarmierung per Email zu senden, mit den Alarmdaten als JSON-Anhang.
Dies ist die Anleitung, wie diese JSON-Alarmdaten in Alamos genutzt werden können.

![Schematische Darstellung des Alarmierungsablaufs](/mokos_alamos_ablauf.png)


## Konfiguration
### 1. Vorbereitung
Für die Authentisierung wird ein Key benötigt, der an zwei Orten hinterlegt werden muss (in den Schritten 2 und 6).
Generiere dafür einen zufälligen String, zB [mit diesem Tool](https://www.random.org/strings/?num=1&len=32&digits=on&upperalpha=on&loweralpha=on&unique=on&format=html&rnd=new).

Du benötigst auch die Einheit-Nr. deiner Feuerwehr aus MoKoS. Du findest diese wenn du unter https://feuerwehralarmierung.ag.ch (oder vergleichbare MoKoS Web-Seite anderer Regionen) auf die Einheit klickst.

![Einheit-Nr in MoKoS](/mokos_einheit_nr.png)

### 2. Batch Script anpassen und auf Server ablegen
Öffne das Batch Script '[mokos_transform_json.bat](/mokos_transform_json.bat)' in einem Texteditor, und passe die Werte für _orgId_ und _authKey_ mit den Werten aus Schritt 1 an.

Lege die angepasste Datei auf dem Alamos-Server ab, im Ordner _C:\ProgramData\Alamos GmbH\FE2\Config\_.

Je nach Alamos-Setup muss der HTTP-Aufruf am Ende des Batch Files angepasst werden (zB Port).

### 3. Mail-Verarbeitungs Einheit erstellen
Lege in Alamos, unter 'Einheiten', eine neue Einheit mit dem Namen 'MoKoS Mail-Eingang' an.
Öffne diese, und importiere die Datei '[mokos_mail_eingang.json](/mokos_mail_eingang.json)'.

![Screenshot von MoKoS Mail Eingang Einheit in Alamos](/mokos_mail_eingang_einheit.png)

Je nach Alamos-Setup müssen ggf. die Pfade unter 'Datei einlesen' und 'Batch/Shell-Skripte' angepasst werden.

### 4. Alarmierungs-Einheit erstellen
Lege in Alamos, unter 'Einheiten', eine neue Einheit mit dem Namen 'MoKoS Alarmierung' an.
Öffne diese, und importiere  die Datei '[mokos_alarmierung.json](/mokos_alarmierung.json)'.

![Screenshot von MoKoS Alarmierung Einheit in Alamos](/mokos_alarmierung_einheit.png)

Passe diese Einheit nach deinen Alarmierungswünschen an.

Der Alarm hat ein Feld für jede Alarmgruppe gesetzt, im Format _alarmgruppe_xyz_ (zB _alarmgruppe_strassenrettung_), jeweils mit dem Wert _true_ oder _false_.  
[Komplette Liste der Gruppen](mokos_transform_json.bat#L45). 

Mit dem Whitelist-Plugin kann geprüft werden, ob diese Alarmgruppe alarmiert wurde, indem im Feld Wortliste der Wert _true_ eingetragen wird, und im Feld 'Quelle' im Tab 'Optionales' der Wert der Gruppe (zB _alarmgruppe_strassenrettung_).

### 5. Anlegen Mail-Alarmeingang
Füge in Alamos, unter 'Administration -> Alarmeingang', einen neuen Alarmeingang vom Typ [Mail-Überwachung](https://alamos-support.atlassian.net/wiki/spaces/documentation/pages/219480356/Mail-+berwachung) hinzu.
Konfiguriere diesen, neben der Konfiguration der Email-Daten, mit folgenden Werten:
- Reiter 'Sicherheit'
  - Erlaubte Absender-Email: 'kfa@die-agv.ch' eintragen
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
- Reiter 'Alarmierung'
  - Standard-Einheit 'MoKoS Alarmierung' wählen
- Reiter 'HTTP'
  - 'HTTP POST' ankreuzen
- Reiter 'Erlaubte Einheiten'
  - Erlaubte Einheit 'MoKoS Alarmierung' ankreuzen


## Weiteres
- Anleitung geschrieben basierend auf Alamos Version 2.38.110
- Offene Punkte:
  - Erkennen von Alarmübungen (AlertExercise?)
  - Erkennen von Nachalarmierungen (Alarmcount? // relevant?)
  - Spezielle Handhabung BMA
  - Objektdispositive?
  - Weitere Alarmgruppen (MGV, ...)
