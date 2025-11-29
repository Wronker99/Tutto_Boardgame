# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 21:05:08 2025

@author: fkrap
"""
import random
import collections
spielkarten = [200, 300, 400, 500, 600, "x2", "Aussetzer"]

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
    while nochmal_wuerfeln != "nein" and anzahl_wuerfel != 0:
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
            print("\nVor Ihnen liegen akutell", punkte, "Punkte.")
            nochmal_wuerfeln = input("\nNochmal würfeln [ja] oder Zug beenden [nein]: \n")
    return punkte, tutto

                
def spielerzug():
    punkte_runde = 0
    while True:
        punkte_karte = 0
        tutto = False
        gezogene_karte = random.choice(spielkarten)
        if isinstance(gezogene_karte, int) or gezogene_karte == "x2":
            punkte_karte, tutto = spielkarte_bonus(gezogene_karte)
        elif gezogene_karte == "Aussetzer":
            punkte_runde = 0
            print("Sie müssen Aussetzen.")
            return punkte_runde
        #Hier weitere karten einfügen
        if punkte_karte > 0:
            punkte_runde += punkte_karte
        else:
            punkte_runde = 0
            print("\nAlle Punkte verloren.\n")
        if tutto == False:
            return punkte_runde
        else:
            print("\nIn diesem Zug haben Sie bisher", punkte_runde, "Punkte gesammelt.\n")
            if input("Neue Karte ziehen [ja] oder Zug final beenden [nein]? ") == "ja":
                continue
            else:
                return punkte_runde

print(spielerzug())


















































