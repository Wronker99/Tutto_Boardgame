# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 18:09:11 2025

@author: fkrap
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 21:05:08 2025

@author: fkrap
"""
import random, collections, datetime, sys, os, time

#Allgemeine Startbedingungen
spielkarten = [200, 300, 400, 500, 600, "x2", "Aussetzer", "Strasse", "Feuerwerk", "plus_minus_tausend", "Kleeblatt"]
wahrscheinlichkeiten =[5,5,5,5,5,5,10,5,500000,5,1] #56 Karten
verbotene_zeichen = ("!", "@", "#", "$", "%", "^", "&", "*", "(", ")",".", "+", "=", "{", "}", "[", "]", "|", "\\", ":", ";", "\"", "'", "<", ">", ",", "?", "/", "~", "`", "§", "€", "£", "¥", "°")

def spieler_eingabe():
    spielername = -1
    spieler =[]
    while spielername != "":
        print(f"\nEingetragene Spieler: {', '.join(spieler)}\n")
        spielername = input("\nBitte gib einzeln die Spielernamen ein (Enter zum Beenden): ")
        try:
            int(spielername)
            print("\nEingabe von Zahlen nicht erlaubt!\n")
            continue
        except:
            if any(zeichen in spielername for zeichen in verbotene_zeichen):
                print("\nUngültige Zeichen")
                continue
            if spielername != "":
                if spielername in spieler:
                    print("\nName schon vorhanden.\n")
                    continue
                spieler.append(spielername)
    return spieler

def spielstand_speichern(punktestand): #Noch prüfen, ob dateiname schon vorhanden ist.
    global spielmarker
    global spieler
    datum_uhrzeit = str(datetime.datetime.now())
    datum_uhrzeit = datum_uhrzeit[:19]
    if spiel_beendet:
        with open("Archiv.txt", 'a') as archiv:
            archiv.write(f"Finaler Spielstand:\nAbgespeichert am {datum_uhrzeit}\n" + "-" * 30 + "\n" + f"Gewinner = {spieler[spielmarker]}\n" + "-" * 30 + "\n\n")
            for spieler, punkte in punktestand.items():
                archiv.write(f"{spieler}: {punkte}\n")
            archiv.write(100 * "_" + "\n")
            print("\nDie Partie wurde im Archiv gespeichert.\n")
    else:
        while True:
            dateiname = input("Speichern als: ")
            if any(zeichen in dateiname for zeichen in verbotene_zeichen):
                print("\nUngültige Eingabe.")
                continue
            if dateiname + ".txt" in spielstaende:
                print("\nName schon vergeben.")
                continue
            dateiname = dateiname + ".txt"
            with open(dateiname, 'w') as datei:
                datei.write(f"Aktueller Spielstand:\nAbgespeichert am {datum_uhrzeit}\n" + "-" * 30 + "\n" + f"Aktueller Spieler = {spielmarker}\n" + "-" * 30 + "\n")
                for spieler, punkte in punktestand.items():
                    datei.write(f"{spieler}: {punkte}\n")
            print(f"Spiel erfolgreich im Arbeitsverzeichnis unter \"{dateiname[:-4]}\" gespeichert.")
            break
        
def spielstand_auswaehlen():
    global spielstaende
    pfad_programm = os.path.dirname(os.path.abspath(__file__))
    os.chdir(pfad_programm)
    alle_dateien = os.listdir('.')
    spielstaende = [datei for datei in alle_dateien if datei.endswith(".txt") and not datei.startswith("Archiv")]
    anzahl_dateien = len(spielstaende)
    if anzahl_dateien == 0:
        print("\nEs wurden keine Spielstände zum Laden gefunden.")
        return None
    print("\nVerfügbare Spielstände: \n\n")
    i = 1
    for spielstand in spielstaende:
        print(f"{i}: {spielstand[:-4]}\n")
        i += 1
    while True:
        try:
            auswahl = int(input("\nWelcher Spielstand soll geladen werden? [Nr.] Neues Spiel [0]\n\n"))
        except:
            print("\nEingabe ungültig")
            continue
        if auswahl < 0 or auswahl > anzahl_dateien:
            print("\nEingabe ungültig")
            continue
        if auswahl == 0:
            return None
        return spielstaende[auswahl - 1]

def spielstand_laden(dateiname):
    punktestand = {}
    spieler = []
    with open(dateiname, 'r') as datei:
        for _ in range(3):
            datei.readline()
        zeile_spielmarker = datei.readline()
        _, spielmarker = zeile_spielmarker.split("=", 1)
        datei.readline()
        for zeile in datei:
            zeile = zeile.strip()
            spieler_name, punkte_str = zeile.split(":", 1)
            punktestand[spieler_name] = int(punkte_str)
            spieler.append(spieler_name)
    return int(spielmarker.strip()), punktestand, spieler
            
def wuerfeln(anzahl_wuerfel):
    wurf = [random.randint(1,6) for _ in range(anzahl_wuerfel)]
    print(f"\nSie Würfeln mit {anzahl_wuerfel} Würfeln...\n")
    time.sleep(0.02)
    for wuerfel in wurf:
        print(wuerfel, end = " ", flush = True)
        time.sleep(0.07)
    print()        
    return sorted(wurf)

def wuerfel_auswaehlen(wurf):
    auswahl = -1
    weggelegte_wuerfel = [] 
    while auswahl != 0:
        print("-" * 30)
        print("Ausgewählte_Würfel: ", *weggelegte_wuerfel)
        print("Ihr wurf: ", *wurf)
        try:
            auswahl = int(input("Würfel zum Weglegen nennen (0 zum Abschließen): "))
        except ValueError:
            print("\n!!! Ungültige Eingabe !!!\n")
            continue
        if auswahl == 0:
            break
        if auswahl not in wurf:
            print("\n!!! Ungültige Eingabe !!!\n")
            continue
        wurf.remove(auswahl)
        weggelegte_wuerfel.append(auswahl)
        weggelegte_wuerfel.sort()
    return weggelegte_wuerfel, wurf

def punkte_pruefen(wurf):
    punkte = 0
    korrekte_Auswahl = True
    haeufigkeiten = collections.Counter(wurf)
    for wert, anzahl in list(haeufigkeiten.items()):
        while anzahl >= 3:
            if wert == 1:
                punkte += 1000
            else:
                punkte += wert * 100
            anzahl -= 3
            haeufigkeiten[wert] -= 3     
    for wert, anzahl in list(haeufigkeiten.items()):
        if wert == 1:
            punkte += anzahl * 100
        elif wert == 5:
            punkte += anzahl * 50
        elif anzahl >= 1:
            korrekte_Auswahl = False
    return punkte, korrekte_Auswahl

def spielkarte_bonus(bonus): #letzer Würfel muss auch "bewusst" gewählt werden, vll ändern 
    anzahl_wuerfel = 6
    punkte_karte = 0
    nochmal_wuerfeln = "ja"
    tutto = False
    while nochmal_wuerfeln != "nein" and anzahl_wuerfel > 0:
        print(f"\nIhre aktelle Karte: Bonus {bonus}\n")
        wurf=wuerfeln(anzahl_wuerfel)
        if punkte_pruefen(wurf)[0] == 0:
            print("\nKeine Punkte. Zug beendet.\n")
            punkte_karte = 0
            return punkte_karte, tutto
        while True:
            print(f"\n\nIhre aktelle Karte: Bonus {bonus}")
            weggelegte_wuerfel, uebrige_wuerfel  =wuerfel_auswaehlen(wurf)
            punkte_Auswahl, korrekte_Auswahl = punkte_pruefen(weggelegte_wuerfel)
            wurf = sorted(weggelegte_wuerfel + uebrige_wuerfel)
            if not korrekte_Auswahl:
                print("\nDu hast ungültige Würfel weggelegt. Bitte erneut Auswählen\n")
                continue
            if punkte_pruefen(uebrige_wuerfel)[0] != 0:
                while True:
                    eingabe = input("\nDu könntest noch Würfel weglegen. Nochmal auswählen? [ja] ansonsten [nein]\n")
                    if eingabe not in ("ja","nein"):
                        print("\nUngültige Eingabe")
                        continue
                    break
                if eingabe == "ja":
                    continue
                if eingabe =="nein":
                    break
            break
        punkte_karte += punkte_Auswahl
        anzahl_wuerfel -= len(weggelegte_wuerfel)  
        if len(uebrige_wuerfel) == 0:
            if bonus == "x2":
                punkte_karte *= 2
            else:
                punkte_karte += bonus
            tutto = True
        else:
            print(f"\nVor Ihnen liegen aktuell {punkte_karte} Punkte.\n")  
            while True:
                print(f"\nNochmal mit {anzahl_wuerfel} Würfel würfeln [ja] oder Zug beenden [nein]: \n")
                eingabe = input()
                if eingabe not in ("ja","nein"):
                    print("\nUngültige Eingabe")
                    continue
                nochmal_wuerfeln = eingabe
                break
    return punkte_karte, tutto

def spielkarte_strasse(): #Anzeige verbessern
    anzahl_wuerfel = 6
    strasse = []
    weitermachen = True
    print("\nDu hast eine Strasse gezogen.\n")
    while weitermachen and anzahl_wuerfel > 0:
        wurf = wuerfeln(anzahl_wuerfel)
        weitermachen = False
        for wuerfel in wurf:
            if wuerfel not in strasse:
                strasse.append(wuerfel)
                strasse.sort()
                anzahl_wuerfel -= 1
                weitermachen = True
        print(f"Deine Strasse sieht bisher so aus:\n{strasse}\n")
        time.sleep(1)
    if len(strasse) == 6:
        tutto = True
        punkte_karte = 2000
    else:
        print(f"Strasse leider nicht geschafft. Dein Ergebnis:\n{strasse}")
        tutto = False
        punkte_karte = 0
    return punkte_karte, tutto    

def spielkarte_feuerwerk():
    anzahl_wuerfel = 6
    punkte = 0
    print("\nDu hast ein Feuerwerk gezogen.\n")
    while True:
        wurf = wuerfeln(anzahl_wuerfel)
        #print(wurf)
        haeufigkeiten = collections.Counter(wurf)
        for wert, anzahl in list(haeufigkeiten.items()):
            while anzahl >= 3:
                if wert == 1:
                    punkte += 1000
                else:
                    punkte += wert * 100
                anzahl -= 3
                haeufigkeiten[wert] -= 3
                for _ in range(3):
                    wurf.remove(wert)
        for wert, anzahl in list(haeufigkeiten.items()):
            if wert == 1 and anzahl != 0:
                punkte += anzahl * 100
                for _ in range(anzahl):
                    wurf.remove(wert)
            elif wert == 5 and anzahl != 0:
                punkte += anzahl * 50
                for _ in range(anzahl):
                    wurf.remove(wert)
        if len(wurf) == anzahl_wuerfel:
            return punkte
        print(f"\nSie haben schon {punkte} Punkte gesammelt und es geht noch weiter...")
        if len(wurf) == 0:
            anzahl_wuerfel = 6
        else:
            anzahl_wuerfel = len(wurf)
        continue

def spielkarte_plus_minus_tausend():
    anzahl_wuerfel = 6
    while True:
        wurf = wuerfeln(anzahl_wuerfel)
        haeufigkeiten = collections.Counter(wurf)
        for wert, anzahl in list(haeufigkeiten.items()):
            while anzahl >= 3:
                anzahl -= 3
                haeufigkeiten[wert] -= 3
                for _ in range(3):
                    wurf.remove(wert)
        for wert, anzahl in list(haeufigkeiten.items()):
            if wert == 1 and anzahl != 0:
                for _ in range(anzahl):
                    wurf.remove(wert)
            elif wert == 5 and anzahl != 0:
                for _ in range(anzahl):
                    wurf.remove(wert)
        if len(wurf) == anzahl_wuerfel:
            return False
        elif len(wurf) == 0:
            return True
        else:
            anzahl_wuerfel = len(wurf)
            continue

def spielkarte_kleeblatt():
    print("\nDu hast das Kleeblatt gezogen!\n")
    #return spielkarte_plus_minus_tausend() and spielkarte_plus_minus_tausend() 

    if spielkarte_plus_minus_tausend():
        print("\nSie haben das 1. Tutto geschafft! Weiter gehts!")
        time.sleep(.5)
        return spielkarte_plus_minus_tausend()
    return False

def spielerzug(): #Wenn 1. Wurf ein Nullwurf, Ausgabe "Alle Punkte verloren"
    punkte_runde = 0
    global punktestand
    while True:
        punkte_karte = 0
        tutto = False
        gezogene_karte = random.choices(spielkarten, weights=wahrscheinlichkeiten,k=1)[0]
        if isinstance(gezogene_karte, int) or gezogene_karte == "x2":
            punkte_karte, tutto = spielkarte_bonus(gezogene_karte)
        elif gezogene_karte == "Aussetzer":
            punkte_runde = 0
            print("\nDu musst Aussetzen. Bisher gesammelte Punkte in dieser Runde gehen verloren.\n")
            return punkte_runde
        elif gezogene_karte == "Strasse":
            punkte_karte, tutto = spielkarte_strasse()
        elif gezogene_karte == "Feuerwerk":          
            punkte_karte = spielkarte_feuerwerk()
            print(f"\nDu hast {punkte_karte} Punkte erspielt.\n")
        elif gezogene_karte == "plus_minus_tausend":     
            print("\nDu hast +/- Tausend gezogen.\n")
            geschafft = spielkarte_plus_minus_tausend()
            if geschafft == True:
                punktestand_sortiert = dict(sorted(punktestand.items(), key = lambda item: item[1], reverse = True))
                fuehrender_spieler = next(iter(punktestand_sortiert))
                if punktestand[fuehrender_spieler] >= 1000 and fuehrender_spieler != spieler_an_der_reihe:
                    punktestand[fuehrender_spieler] -= 1000
                elif fuehrender_spieler != spieler_an_der_reihe:
                    punktestand[fuehrender_spieler] = 0
                if fuehrender_spieler != spieler_an_der_reihe:
                    print(f"\nDu hast das Tutto geschafft!\n\nDu erhältst 1000 Punkte und {fuehrender_spieler} werden 1000[max] abgezogen.")
                else:
                    print("\nDu hast das Tutto geschafft!\n\nDu erhältst 1000 Punkte")
                punkte_runde = 1000
                return punkte_runde
            else:
                print("\nTutto nicht geschafft. Der nächste Spieler ist an der Reihe.\n")
        elif gezogene_karte == "Kleeblatt":
            if spielkarte_kleeblatt() == True:
                punkte_runde = -1
                return punkte_runde
            else:
                punkte_runde = 0
                print("\nKleeblatt nicht geschafft.\n")
            
        #Hier weitere karten einfügen
        
        if punkte_karte > 0:
            punkte_runde += punkte_karte
        else:
            punkte_runde = 0
            print("\nKeine Punkte für diese Runde.\n") 
        if not tutto:
            return punkte_runde
        else:
            print("\nIn diesem Zug hast Du bisher", punkte_runde, "Punkte gesammelt.\n")
            while True:
                eingabe = input("\nNeue Karte ziehen [ja] oder Zug final beenden [nein]? \n")
                if eingabe not in ("ja", "nein"):
                    print("\nUngültige Eingabe")
                    continue
                if eingabe == "nein":
                    return punkte_runde
                break
        continue

def spielablauf():      #Beim Erreichen der Punkte, wird Spiel direkt beendet.
    global punktestand
    global spieler_an_der_reihe #Name des Spieler
    global spielmarker #Position des Spielers in der Liste spieler
    global spiel_beendet
    global spieler
    erste_runde = True
    spiel_beendet = False
    
    dateiname = spielstand_auswaehlen()
    if dateiname:
        spielmarker, punktestand, spieler = spielstand_laden(dateiname)
        beginnender_spieler = spielmarker
    else:
        print("\nEs wird ein neues Spiel gestartet.\n")
        spieler = spieler_eingabe()
        beginnender_spieler = random.randint(0,len(spieler) - 1)
        spielmarker = beginnender_spieler
        punktestand = {spielername: 0 for spielername in spieler}
        

    while not spiel_beendet:
                   
        #Speicherabfrage
        if spielmarker == beginnender_spieler and erste_runde != True:
            while True:
                speichern = input("\nMöchtest Du das Spiel speichern und beenden [ja] oder fortfahren [nein]?\n")
                if speichern == "nein":
                    break
                elif speichern == "ja":
                    print(f"\nAktueller Punktestand: {punktestand}\n")
                    spielstand_speichern(punktestand)
                    while True:
                        if input("Enter zum Beenden: ") != "":
                            print("\nUngültige Eingabe\n")
                            continue
                        break
                    sys.exit()
                else:
                    print("\nUngültige Eingabe")
                    continue

        #Zugbeginn
        spieler_an_der_reihe = spieler[spielmarker]
        print(f"\nAktueller Punktestand: {punktestand}\n")
        print(f"\n{spieler_an_der_reihe}, du bist dran:")
        punkte_runde = spielerzug()

            
        #Kleeblattabfrage
        if punkte_runde < 0:
            print(f"\n{spieler_an_der_reihe}, du hast durch das Kleblatt gewonnen!\n")
            spiel_beendet = True
            punktestand[spieler_an_der_reihe] = "Durch das Kleeblatt gewonnen!"
            spielstand_speichern(punktestand)
            while True:
                if input("Enter zum Beenden: ") != "":
                    print("\nUngültige Eingabe\n")
                    continue
                break
            sys.exit()
        else:
            #Punkte aufaddieren
            punktestand[spieler_an_der_reihe] += punkte_runde
            
            #Gewinnerabfrage
            for spieler_name, punkte in punktestand.items():
                if punkte >= 6000:
                    print(f"\n{spieler_name}, Du hast gewonnen und hast {punkte} Punkte.\n")
                    print(f"\nAbschließender Gesamtpunktstand: {punktestand}")
                    spiel_beendet = True
                    spielstand_speichern(punktestand)
                    break
            if spiel_beendet:
                if dateiname:
                    try:
                        os.remove(dateiname)
                        print(f"\nDie zuvor geladene Datei {dateiname[:-4]} wurde gelöscht.\n")
                    except:
                        print("\nFehler beim Löschen.")
                while True:
                    if input("Enter zum Beenden: ") != "":
                        print("\nUngültige Eingabe\n")
                        continue
                    break
                sys.exit()
            
            spielmarker += 1
            erste_runde = False
            if spielmarker > len(spieler) - 1:
                spielmarker = 0                
        
        
spielablauf()













































