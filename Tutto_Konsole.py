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
#wahrscheinlichkeiten =[5,5,5,5,5,5,10,5,5,5,1] #56 Karten
wahrscheinlichkeiten =[0,0,0,0,0,0,0,0,0,0,1] #56 Karten
verbotene_zeichen = ("!", "@", "#", "$", "%", "^", "&", "*", "(", ")",".", "+", "=", "{", "}", "[", "]", "|", "\\", ":", ";", "\"", "'", "<", ">", ",", "?", "/", "~", "`", "§", "€", "£", "¥", "°", " ")

def spieler_eingabe():
    spielername = -1
    spieler =[]
    while True:
        while spielername != "":
            print(f"\nEingetragene Spieler: {', '.join(spieler)}")
            #schreiben("\nBitte gib einzeln die Spielernamen ein (Enter zum Beenden): ")
            spielername = input("\nBitte gib einzeln die Spielernamen ein (Enter zum Beenden): ")
            #spielername = input()
            try:
                int(spielername)
                print("\nEingabe von Zahlen nicht erlaubt!\n")
                continue
            except ValueError:
                if any(zeichen in spielername for zeichen in verbotene_zeichen):
                    print("\nUngültige Zeichen")
                    continue
                if spielername != "":
                    if spielername in spieler:
                        print("\nName schon vorhanden.\n")
                        continue
                    spieler.append(spielername)
        if len(spieler) < 2:
            print("\nMindestens 2 Spieler eingeben!")
            spielername = None
            continue
        break
    return spieler

def spielstand_speichern(punktestand, spielmarker, spiel_beendet, spielstaende, spieler, dateiname, gewinner):
    
    datum_uhrzeit = str(datetime.datetime.now())
    datum_uhrzeit = datum_uhrzeit[:19]
    if spiel_beendet:
        
        #Archiv
        if dateiname == None:
            while True:
                print("\nBitte gib dem Spiel noch einen Namen (Für das Archiv): \n")
                dateiname = input()
                if any(zeichen in dateiname for zeichen in verbotene_zeichen):
                    print("\nUngültige Eingabe.\n")
                    continue
                if dateiname == "":
                    print("\nUngültige Eingabe.\n")
                    continue
                break
        with open("Archiv.txt", 'a') as archiv:
            archiv.write(f"\nDateiname: {dateiname}\nAbgespeichert am {datum_uhrzeit}\n" + "-" * 30 + "\n" + f"Gewinner = {gewinner}\n" + "-" * 30 + "\n\n")
            for spieler, punkte in punktestand.items():
                archiv.write(f"{spieler}: {punkte}\n")
            archiv.write(100 * "_" + "\n")
            print("\nDie Partie wurde im Archiv gespeichert.\n")
        
        #Bestenliste
        
            
        
    else:
        while True:
            dateiname_neu = input("Speichern als: ")
            ueberschrieben = False
            if any(zeichen in dateiname_neu for zeichen in verbotene_zeichen):
                print("\nUngültige Eingabe.\n")
                continue
            if dateiname == "":
                print("\nUngültige Eingabe.\n")
                continue
            if dateiname_neu == "Archiv" or dateiname_neu == "archiv":
                print("\nUngültige Eingabe.\n")
                continue
            if dateiname_neu + ".txt" in spielstaende and dateiname_neu + ".txt" != dateiname:
                print("\nName schon vergeben.\n")
                continue
            if dateiname and dateiname_neu == dateiname[:-4]:
                os.remove(dateiname)
                ueberschrieben = True
        
            dateiname_neu = dateiname_neu + ".txt"
            with open(dateiname_neu, 'w') as datei:
                datei.write(f"Aktueller Spielstand:\nAbgespeichert am {datum_uhrzeit}\n" + "-" * 30 + "\n" + f"Aktueller Spieler = {spielmarker}\n" + "-" * 30 + "\n")
                for spielername, punkte in punktestand.items():
                    datei.write(f"{spielername}: {punkte}\n")
            if ueberschrieben:
                print(f"\nDer Spielstand \"{dateiname_neu[:-4]}\" wurde überschrieben.\n")
            else: 
                print(f"Spiel erfolgreich im Arbeitsverzeichnis unter \"{dateiname_neu[:-4]}\" gespeichert.")
            break
        
def spielstand_auswaehlen():
    pfad_programm = os.path.dirname(os.path.abspath(__file__))
    os.chdir(pfad_programm)
    alle_dateien = os.listdir('.')
    spielstaende = [datei for datei in alle_dateien if datei.endswith(".txt") and not datei.startswith("Archiv")]
    anzahl_dateien = len(spielstaende)
    if anzahl_dateien == 0:
        print("\nEs wurden keine Spielstände zum Laden gefunden.")
        return None, spielstaende
    print("\nVerfügbare Spielstände: \n\n")
    i = 1
    for spielstand in spielstaende:
        print(f"{i}: {spielstand[:-4]}\n")
        i += 1
    while True:
        try:
            auswahl = int(input("\nWelcher Spielstand soll geladen werden? [Nr.] Neues Spiel [0]\n\n"))
        except ValueError:
            print("\nEingabe ungültig")
            continue
        if auswahl < 0 or auswahl > anzahl_dateien:
            print("\nEingabe ungültig")
            continue
        if auswahl == 0:
            return None, spielstaende
        return spielstaende[auswahl - 1], spielstaende

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
    print(f"\nSie Würfeln mit {anzahl_wuerfel} Würfeln...[ENTER]\n")
    eingabe = input()
    while eingabe != "":
        eingabe = input()
        print("\nUngültige Eingabe.\n")
        continue
    #time.sleep(0.2)
    for wuerfel in wurf:
        print(wuerfel, end = " ", flush = True)
        #time.sleep(0.3)
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
            auswahl = int(input("Würfel zum Weglegen nennen (0 zum Abschließen)\n + [ENTER]: "))
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

def spielkarte_bonus(bonus, punkte_runde): #letzer Würfel muss auch "bewusst" gewählt werden, vll ändern 
    anzahl_wuerfel = 6
    punkte_karte = 0
    nochmal_wuerfeln = "ja"
    tutto = False
    while nochmal_wuerfeln != "nein" and anzahl_wuerfel > 0:
        print(32*"#","\n",4*"#",f" DEINE KARTE: BONUS {bonus}"," ",4*"#","\n",32*"#", sep="")
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
            print("\n!!! TUTTO !!!")
            if bonus == "x2":
                punkte_karte *= 2
            else:
                punkte_karte += bonus
            tutto = True
        else:
            print(f"\nVor Ihnen liegen aktuell {punkte_runde + punkte_karte} Punkte.\n")  
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
        print(f"\nDeine Strasse sieht bisher so aus:\n{strasse}\n")
        time.sleep(1)
    if len(strasse) == 6:
        tutto = True
        punkte_karte = 2000
    else:
        print(f"Strasse leider nicht geschafft. Dein Ergebnis:\n{strasse}")
        tutto = False
        punkte_karte = 0
    return punkte_karte, tutto    

def spielkarte_feuerwerk(punkte_runde):
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
        print(f"\nSie haben schon {punkte + punkte_runde} Punkte gesammelt und es geht noch weiter...")
        if len(wurf) == 0:
            anzahl_wuerfel = 6
            print("\n!!! TUTTO !!!")
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
            print("\n!!! TUTTO !!!")
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

def spielerzug(punktestand, spieler_an_der_reihe): #Wenn 1. Wurf ein Nullwurf, Ausgabe "Alle Punkte verloren"
    punkte_runde = 0
    while True:
        punkte_karte = 0
        tutto = False
        gezogene_karte = random.choices(spielkarten, weights=wahrscheinlichkeiten,k=1)[0]
        if isinstance(gezogene_karte, int) or gezogene_karte == "x2":
            punkte_karte, tutto = spielkarte_bonus(gezogene_karte, punkte_runde)
        elif gezogene_karte == "Aussetzer":
            punkte_runde = 0
            print("\nDu musst Aussetzen. Bisher gesammelte Punkte in dieser Runde gehen verloren.\n")
            return punkte_runde
        elif gezogene_karte == "Strasse":
            punkte_karte, tutto = spielkarte_strasse()
        elif gezogene_karte == "Feuerwerk":          
            punkte_karte = spielkarte_feuerwerk(punkte_runde)
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
                punkte_karte = 1000
                time.sleep(1)
                return punkte_runde
            else:
                punkte_karte = 0
                print("\nTutto nicht geschafft. Der nächste Spieler ist an der Reihe.\n")
                time.sleep(1)
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

def spielablauf():
    erste_runde = True
    spiel_beendet = False
    spieler_an_der_reihe = None
    gewinner = None
    
    #Initialisieren
    dateiname, spielstaende = spielstand_auswaehlen()
    if dateiname:
        spielmarker, punktestand, spieler = spielstand_laden(dateiname)
        beginnender_spieler = spielmarker
    else:
        print("\nEs wird ein neues Spiel gestartet.\n")
        spieler = spieler_eingabe()
        beginnender_spieler = random.randint(0,len(spieler) - 1)
        spielmarker = beginnender_spieler
        punktestand = {spielername: 0 for spielername in spieler}
        dateiname = None
        

    while not spiel_beendet:
        
        #Gewinnerabfrage
        if erste_runde != True:
            for spieler_name, punkte in punktestand.items():
                if punkte >= 6000 and spielmarker == beginnender_spieler:
                    punktestand_sortiert = dict(sorted(punktestand.items(), key = lambda item: item[1], reverse = True))
                    punktezahlen = list(punktestand_sortiert.values())
                    if len(punktezahlen) > 1 and punktezahlen[0] == punktezahlen[1]:
                        print("Unglaublich! Ein Unentschieden! Das Spiel wurde nicht gespeichert. Am besten ihr spielt nochmal =)")
                        sys.exit()
                    gewinner = next(iter(punktestand_sortiert))
                    print(f"\n{gewinner}, Du hast gewonnen und hast {punkte} Punkte.\n")
                    print(80*"-",f"\nAbschließender Gesamtpunktestand: {punktestand}\n",80*"-", sep="")
                    spiel_beendet = True
                    spielstand_speichern(punktestand, spielmarker, spiel_beendet, spielstaende, spieler, dateiname, gewinner)
                    break
            if spiel_beendet:
                if dateiname:
                    try:
                        os.remove(dateiname)
                        print(f"\nDie zuvor geladene Datei {dateiname[:-4]} wurde gelöscht.\n")
                    except OSError:
                        print("\nFehler beim Löschen.")
                while True:
                    if input("Enter zum Beenden: ") != "":
                        print("\nUngültige Eingabe\n")
                        continue
                    break
                sys.exit()
            
        #Speicherabfrage
        if spielmarker == beginnender_spieler and erste_runde != True:
            while True:
                speichern = input("\nMöchtest Du das Spiel speichern und beenden [ja] oder fortfahren [nein]?\n")
                if speichern == "nein":
                    break
                elif speichern == "ja":
                    print(f"\nAktueller Punktestand: {punktestand}\n")
                    spielstand_speichern(punktestand, spielmarker, spiel_beendet, spielstaende, spieler, dateiname, gewinner)
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
        print(80*"-",f"\nAktueller Punktestand: {punktestand}\n",80*"-", sep="")
        print(f"\n{spieler_an_der_reihe}, du bist dran. [ENTER] zum Fortfahren.")
        eingabe = input()
        while eingabe != "":
            eingabe = input()
            print("\nUngültige Eingabe.\n")
            continue
        punkte_runde = spielerzug(punktestand, spieler_an_der_reihe)
        if punkte_runde >= 0:
            print(f"\nDu hast diese Runde insgesamt {punkte_runde} Punkte gesammelt!")

            
        #Kleeblattabfrage
        if punkte_runde < 0:
            print(f"\n{spieler_an_der_reihe}, du hast durch das Kleblatt gewonnen!\n")
            spiel_beendet = True
            gewinner = spieler_an_der_reihe
            punktestand[spieler_an_der_reihe] = 99999
            spielstand_speichern(punktestand, spielmarker, spiel_beendet, spielstaende, spieler, dateiname, gewinner)
            while True:
                if input("Enter zum Beenden: ") != "":
                    print("\nUngültige Eingabe\n")
                    continue
                break
            sys.exit()
        else:
            #Punkte aufaddieren
            punktestand[spieler_an_der_reihe] += punkte_runde
            spielmarker += 1
            erste_runde = False
            if spielmarker > len(spieler) - 1:
                spielmarker = 0                
        
        
spielablauf()













































