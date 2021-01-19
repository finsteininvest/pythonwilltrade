# Wie Du mein Code zum laufen bekommst

Ich habe mit einem [Blogbeitrag](https://finsteininvest.pythonanywhere.com/) Dein Interesse geweckt und Du möchtest meine Analyse nachstellen?

Hier beschreibe ich, was Du installieren und machen musst.

## 1. Installiere Python
Lade und installiere Python von [hier](https://www.python.org/downloads/) herunter. Bitte auf jeden Fall Python 3 installieren!

## 2. Erzeuge eine virtuelle Umgebung
Im Kern besteht der Hauptzweck der virtuellen Umgebungen von Python darin, eine isolierte Umgebung für Python-Projekte zu schaffen. Das bedeutet, dass jedes Projekt seine eigenen Abhängigkeiten haben kann, unabhängig davon, welche Abhängigkeiten jedes andere Projekt hat.

Jetzt musst Du eine Kommandozeile öffnen.

- Windows: Auf die Lupe (links unten) klicken und "CMD" eingeben. Return drücken.
- Mac: CMD; Space gleichzeitig drücken: "Terminal" eingeben, kurz warten und dann "Return" drücken.

Am besten jetzt ein neues Verzeichnis anlegen:

- Windows: mkdir "PythonWillTrade"
- Mac: mkdir "PythonWillTrade"

Jetzt legen wir die virtuelle Umgebung an:

- Eintippen "python3 -m venv pwtenv" und "Return" drücken.

Mit diesem Kommando wird eine Umgebung mit dem Namen "pwtenv" erzeugt. Du kannst natürlich den Namen beliebig wählen.

** Achtung: Die virtuelle Umgebung musst Du jedesmal aktivieren, wenn Du Code von mir ausführen möchtest **

Um die Umgebung zu aktivieren musst Du:

"cd pwtenv/scripts"

- Windows: activate
- Mac: source ./activate

## 3. Den Code beschaffen
Der Code zu einem Blogbeitrag befindet sich gesammelt in einem Verzeichnis mit dem gleichen Titel, wie der Blogbeitrag.

Navigiere in das Verzeichnis und klick auf die verschiedenen .py Deteien. Dann auf "RAW"; rechts, oberhalb der Datei. In einem Verzeichnis auf Deinem Rechner speichern. Das machst Du für alle Dateien, die mit .py enden.

## 4. Installiere notwendige Module
In dem gleichen Verzeichnis findest Du auch eine Datei mit dem Namen "requirements.txt"

Diese Datei beinhaltet die notwendigen Module. Und die Installation dieser Module ist denkbar einfach:

pip install -r requirements.txt (auf der KLommandozeile eingeben)

** Nicht vergessen: vorher die virtuelle Umgebung aktivieren. **

## 5. Code ausführen
Im [Blog](https://finsteininvest.pythonanywhere.com/) steht in jedem Beitrag in welcher Reihenfolge, welches Programm ausgeführt werden soll.

Dazu: python3 name_des_programms.py eingeben. Manchmal müssen noch Parameter eingegeben werden; aber das gebe ich Blogbeitrag an. Statt python3 kann es auch sein, daß Du nur python eingeben musst.
