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
import random
import collections
import datetime
import sys
import os

#Allgemeine Startbedingungen
spielkarten = [200, 300, 400, 500, 600, "x2", "Aussetzer", "Strasse", "Feuerwerk", "plus_minus_tausend", "Kleeblatt"]
wahrscheinlichkeiten =[5,5,5,5,5,5,10,5,5,5,1] #56 Karten

def spieler_eingabe():
    spielername = -1
    spieler =[]
    while spielername != "":
        print(f"\nEingetragene Spieler: {', '.join(spieler)}\n")
        spielername = input("\nBitte geben Sie einzeln die Spielernamen ein (Enter zum Beenden): ")
        try:
            int(spielername)
            print("\nEingabe von Zahlen nicht erlaubt!\n")
            continue
        except:
            if spielername != "":
                if spielername in spieler:
                    print("\nName schon vorhanden.\n")
                    continue
                spieler.append(spielername)
    return spieler

def spielstand_speichern(punktestand):
    global spielmarker
    datum_uhrzeit = str(datetime.datetime.now())
    datum_uhrzeit = datum_uhrzeit[0:19:1]
    dateiname = input("Speichern als: ") + ".txt"
    dateiname = dateiname.replace(":", "-").replace(" ", "-").strip()
    with open(dateiname, 'w') as datei:
        datei.write(f"Aktueller Spielstand:\nAbgespeichert am {datum_uhrzeit}\n" + "-" * 30 + "\n" + f"Aktueller Spieler = {spielmarker}\n" + "-" * 30 + "\n")
        for spieler, punkte in punktestand.items():
            datei.write(f"{spieler}: {punkte}\n")
    print(f"Spiel erfolgreich im Arbeitsspeicher unter {dateiname} gespeichert.")
    sys.exit()

def spielstand_auswaehlen():
    alle_dateien = os.listdir('.')
    spielstaende = [datei for datei in alle_dateien if datei.endswith(".txt")]
    anzahl_dateien = len(spielstaende)
    if anzahl_dateien == 0:
        print("\nEs wurden keine Spielstände zum Laden gefunden.")
        return None
    print("\nAlle verfügbaren Spielstände: \n\n")
    i = 1
    for spielstand in spielstaende:
        print(f"{i}: {spielstand}")
        i += 1
    while True:
        try:
            auswahl = int(input("Welcher Spielstand soll geladen werden? [Nr.] Neues Spiel [0]\n\n"))
        except:
            print("Eingabe ungültig")
            continue
        if auswahl > anzahl_dateien:
            print("Eingabe ungültig")
            continue
        if auswahl == 0:
            return None
        dateiname = spielstaende[auswahl - 1]
        return dateiname
    

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
    wurf.sort()
    return wurf

def wuerfel_auswaehlen(wurf):   #!!! Achtung beim erneuten zurücklegen werden würfel gelöscht! Fälschlich weggelegt würfel lassen sich nicht zurückholen und verfallen beim , aber lösen ein tutto aus
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
        index = wurf.index(auswahl)
        del wurf[index]
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
        elif anzahl > 1:
            korrekte_Auswahl = False
    return punkte, korrekte_Auswahl

def spielkarte_bonus(bonus): #letzer Würfel muss auch "bewusst" gewählt werden, vll ändern 
    anzahl_wuerfel = 6
    punkte = 0
    nochmal_wuerfeln = "ja"
    tutto = False
    while nochmal_wuerfeln != "nein" and anzahl_wuerfel > 0:
        wurf=wuerfeln(anzahl_wuerfel)
        if punkte_pruefen(wurf)[0] == 0:
            print("\nIhr Wurf: ", *wurf,"\nKeine Punkte. Zug beendet.\n")
            punkte = 0
            return punkte, tutto
        while True:
            print(f"\nIhre aktelle Karte: Bonus {bonus}")
            weggelegte_wuerfel, uebrige_wuerfel  =wuerfel_auswaehlen(wurf)
            punkte_Auswahl, korrekte_Auswahl = punkte_pruefen(weggelegte_wuerfel)
            if korrekte_Auswahl == False:
                print("\nSie haben ungültige Würfel weggelegt. Bitte erneut Auswählen\n")
                continue
            punkte += punkte_Auswahl
            anzahl_wuerfel -= len(weggelegte_wuerfel)
            if punkte_pruefen(uebrige_wuerfel)[0] != 0:
                if input("\nSie könnten noch Würfel weglegen. Nochmal auswählen? [ja] ansonsten [nein]\n") == "ja":
                    continue
            break
        if len(uebrige_wuerfel) == 0:
            if bonus == "x2":
                punkte *= 2
            else:
                punkte += bonus
            tutto = True
        else:
            print(f"\nVor Ihnen liegen aktuell {punkte} Punkte.\n")
            print(f"\nNochmal mit {anzahl_wuerfel} Würfel würfeln [ja] oder Zug beenden [nein]: \n")
            nochmal_wuerfeln = input()
    return punkte, tutto

def spielkarte_strasse():
    anzahl_wuerfel = 6
    strasse = []
    weitermachen = True
    while weitermachen == True and anzahl_wuerfel > 0:
        wurf = wuerfeln(anzahl_wuerfel)
        weitermachen = False
        for wuerfel in wurf:
            if wuerfel not in strasse:
                strasse.append(wuerfel)
                anzahl_wuerfel -= 1
                weitermachen = True     
    strasse.sort()
    if len(strasse) == 6:
        tutto = True
        punkte_karte = 2000
    else:
        tutto = False
        punkte_karte = 0
    return punkte_karte, tutto    

def spielkarte_feuerwerk():
    anzahl_wuerfel = 6
    punkte = 0
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
                wurf.remove(wert)
            elif wert == 5 and anzahl != 0:
                punkte += anzahl * 50
                wurf.remove(wert)
        if len(wurf) == anzahl_wuerfel:
            return punkte
        if len(wurf) == 0:
            anzahl_wuerfel = 6
        else:
            anzahl_wuerfel = len(wurf)
        #print(wurf)
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
                wurf.remove(wert)
            elif wert == 5 and anzahl != 0:
                wurf.remove(wert)
        if len(wurf) == anzahl_wuerfel:
            tutto = False
            return tutto
        elif len(wurf) == 0:
            tutto = True
            return tutto
        else:
            anzahl_wuerfel = len(wurf)
            continue

def spielkarte_kleeblatt():
    tutto_1 = spielkarte_plus_minus_tausend()
    if tutto_1 == True:
        tutto_2 = spielkarte_plus_minus_tausend()
    else:
        return False
    if tutto_2 == True:
        return True
    else:
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
            print("\nSie müssen Aussetzen. Bisher gesammelte Punkte in dieser Runde gehen verloren.\n")
            return punkte_runde
        elif gezogene_karte == "Strasse":
            print("\nSie haben eine Strasse gezogen.\n")
            punkte_karte, tutto = spielkarte_strasse()
        elif gezogene_karte == "Feuerwerk":
            print("\nSie haben ein Feuerwerk gezogen.\n")
            punkte_karte = spielkarte_feuerwerk()
            print(f"\nSie haben {punkte_karte} Punkte erspielt.\n")
        elif gezogene_karte == "plus_minus_tausend":
            print("\nSie haben +/- Tausend gezogen.\n")
            geschafft = spielkarte_plus_minus_tausend()
            if geschafft == True:
                punktestand_sortiert = dict(sorted(punktestand.items(), key = lambda item: item[1], reverse = True))
                fuehrender_spieler = next(iter(punktestand_sortiert))
                if punktestand[fuehrender_spieler] >= 1000 and fuehrender_spieler != spieler_an_der_reihe:
                    punktestand[fuehrender_spieler] -= 1000
                elif fuehrender_spieler != spieler_an_der_reihe:
                    punktestand[fuehrender_spieler] = 0
                if fuehrender_spieler != spieler_an_der_reihe:
                    print(f"\nSie haben das Tutto geschafft!\n\nSie erhalten 1000 Punkte und {fuehrender_spieler} werden 1000[max] abgezogen.")
                else:
                    print("\nSie haben das Tutto geschafft!\n\nSie erhalten 1000 Punkte")
                punkte_runde = 1000
                return punkte_runde
            else:
                print("\nTutto nicht geschafft. Der nächste Spieler ist an der Reihe.\n")
        elif gezogene_karte == "Kleeblatt":
            geschafft = spielkarte_kleeblatt()
            if geschafft == True:
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
        if tutto == False:
            return punkte_runde
        else:
            print("\nIn diesem Zug haben Sie bisher", punkte_runde, "Punkte gesammelt.\n")
            if input("\nNeue Karte ziehen [ja] oder Zug final beenden [nein]? \n") == "ja":
                continue
            else:
                return punkte_runde

def spielablauf():      #Beim Erreichen der Punkte, wird Spiel direkt beendet.
    global punktestand
    global spieler_an_der_reihe #Name des Spieler
    global spielmarker #Position des Spielers in der Liste spieler
    
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
        
        
    erste_runde = True
    spiel_beendet = False
    while not spiel_beendet:
        for spieler_name, punkte in punktestand.items():
            if punkte >= 6000:
                print(f"\n{spieler_name}, Sie haben gewonnen und haben {punkte} Punkte.\n")
                print(f"\nAbschließender Gesamtpunktstand: {punktestand}")
                spiel_beendet = True
                break
        if spiel_beendet == True:
            break
        if spielmarker == beginnender_spieler and erste_runde != True:
            speichern = input("\nMöchtest Du das Spiel speichern und beenden [ja] oder fortfahren [nein]?\n")
            if speichern == "nein":
                pass
            if speichern == "ja":
                print(f"\nAktueller Punktestand: {punktestand}\n")
                spielstand_speichern(punktestand)
        spieler_an_der_reihe = spieler[spielmarker]
        print(f"\nAktueller Punktestand: {punktestand}\n")
        print(f"\n{spieler_an_der_reihe}, du bist dran:")
        punkte_runde = spielerzug()

        if punkte_runde < 0:
            print(f"\n{spieler_an_der_reihe}, du hast durch das Kleblatt gewonnen!\n")
            break
        else:
            punktestand[spieler_an_der_reihe] += punkte_runde
            spielmarker += 1
            erste_runde = False
            if spielmarker > len(spieler) - 1:
                spielmarker = 0
        
spielablauf()













































