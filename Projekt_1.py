# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 21:05:08 2025

@author: fkrap
"""
import random
import collections

#Allgemeine Startbedingungen
spielkarten = [200, 300, 400, 500, 600, "x2", "Aussetzer", "Strasse"]
#spielkarten = ["Strasse"]

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
            print(f"\nVor Ihnen liegen akutell {punkte} Punkte.\n")
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


def spielerzug(): #Wenn 1. Wurf ein Nullwurf, Ausgabe "Alle Punkte verloren"
    punkte_runde = 0
    while True:
        punkte_karte = 0
        tutto = False
        gezogene_karte = random.choice(spielkarten)
        if isinstance(gezogene_karte, int) or gezogene_karte == "x2":
            punkte_karte, tutto = spielkarte_bonus(gezogene_karte)
        elif gezogene_karte == "Aussetzer":
            punkte_runde = 0
            print("\nSie müssen Aussetzen. Punkte aus dieser Runde wurden verloren.\n")
            return punkte_runde
        elif gezogene_karte == "Strasse":
            print("\n Sie haben eine Strasse gezogen\n")
            punkte_karte, tutto = spielkarte_strasse()
            
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

def spielablauf():
    spieler = spieler_eingabe() #Beim Erreichen der Punkte, wird Spiel direkt beendet.
    spielmarker = random.randint(0,len(spieler)+1)
    punktestand = {spielername: 0 for spielername in spieler}
    spiel_beendet = False
    while not spiel_beendet:
        for spieler_name, punkte in punktestand.items():
            if punkte >= 6000:
                print(f"\n{spieler_name}, Sie haben gewonnen und haben {punkte} Punkte.\n")
                spiel_beendet = True
                break
        if spiel_beendet == True:
            break
        if spielmarker > len(spieler) - 1:
            spielmarker = 0
        spieler_an_der_reihe = spieler[spielmarker]
        print(f"\nAktueller Punktestand: {punktestand}\n")
        print("\n",spieler_an_der_reihe, ", du bist dran:\n")
        punkte_runde = spielerzug()
        punktestand[spieler_an_der_reihe] += punkte_runde
        spielmarker += 1

spielablauf()














































