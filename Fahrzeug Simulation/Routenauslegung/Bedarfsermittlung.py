import pandas as pd
import numpy as np


def Berechnung():

    ## Bevölkerungsdichte
    A = pd.read_csv("data/Bevölkerungsverteilung.csv", sep=";")
    rho_Volk = A["Bevölkerung je km^2"]
    rho_Volk_zStd = (rho_Volk[0] + rho_Volk[4])/2   # Bevökerungsdichte Zentrale Stadt
    rho_Volk_mStd_Raum = (rho_Volk[1] + rho_Volk[2] + rho_Volk[5] + rho_Volk[6])/4  # Bevökerungsdichte Mittelstadt/ Städtischer Raum
    rho_Volk_kStd_Dorf = (rho_Volk[3] + rho_Volk[7])/2  # Bevökerungsdichte Kleinstädtischer, dörflicher Raum
    rho_volk = np.zeros(3) # speichern aller drei arrays in einem:
    rho_volk[0] = rho_Volk_zStd
    rho_volk[1] = rho_Volk_mStd_Raum
    rho_volk[2] = rho_Volk_kStd_Dorf
    print(rho_volk)

    ## genutzte PKWs pro km (siehe BA_Kapitel:"Hintergrund", Untkapitel: "ländlicherIndividualverkehr")
    B = pd.read_csv("data/PKW_Dichte.csv", sep=";")
    haushalt = np.array(B['Haushaltsgroesse'])
    auto_pro_haushalt = np.array(B['Autos pro Haushalt'])
    autos_genutzt_tag = np.array(B['taegl genutzte PKWs'])
    autos_selten_genutzt = np.array(B['1-3 Tage Woche '])
    autos_seltener_genutzt = np.array(B['1-3 Tage Monat '])
    Haushalte_qkm = rho_volk/haushalt
    autos_verfuegbar = Haushalte_qkm*auto_pro_haushalt
    autos_qkm_tag_genutzt = np.rint(autos_verfuegbar*(autos_genutzt_tag/100)+(2/7)*autos_verfuegbar*autos_selten_genutzt/100+\
                        autos_verfuegbar*(2/28)*autos_seltener_genutzt/100)
    print(autos_qkm_tag_genutzt)



    ## Entfernung pro Tag in Fahrten und Strecken (siehe BA_Kapitel:"Hintergrund", Untkapitel: "ländlicherIndividualverkehr")
    C = pd.read_csv("data/Strecke_Fahrt.csv", sep=";")
    D = pd.read_csv("data/Regelmäßige berufliche Fahrten.csv", sep=";")
    n_fahrten_tag = np.array(C['Durschnittliche Anzahl der Fahrten am Stichtag'])
    s_fahrte= np.array(C["Durschnittliche Entfernung der Fahrten am Stichtag"])
    berufl_fahrt_auto = np.array(D["genutzer PKW %"])
    berufl_fahrt_s = np.array(D["km ges."])
    anteil_mit_regelm_berufl_weg = np.array(D["Prozent der Bevökerung mit regelmäßigen beruflichen Wege"])
    km_fahrt_zusaetzlich = (berufl_fahrt_auto/100) * berufl_fahrt_s * (anteil_mit_regelm_berufl_weg/100)
    s_fahrt = (s_fahrte*n_fahrten_tag+km_fahrt_zusaetzlich)/n_fahrten_tag

    ## Tagesverteilung der Fahrten nach MiD17 in Prozent
    F = pd.read_csv("data/Tagesverteilung.csv", sep=";")
    bis8 = np.array(F["5 - vor 8"]/100)
    bis10 = np.array(F["8 - vor 10"]/100)
    bis13 = np.array(F["10 - vor 13"]/100)
    bis16 = np.array(F["13 - vor 16"]/100)
    bis19 = np.array(F["16 - vor 19"]/100)
    bis22 = np.array(F["19 - vor 22"]/100)
    bis5 = np.array(F["22 - vor 5"]/100)
    tagesverteilung = np.array([bis8,bis10,bis13,bis16,bis19,bis22,bis5])

    return autos_qkm_tag_genutzt, n_fahrten_tag, s_fahrt, tagesverteilung

autos_qkm_tag_genutzt, n_fahrten_tag, s_fahrt, tagesverteilung = Berechnung()
#print(autos_qkm_tag_genutzt)
#print(n_fahrten_tag)
#print(s_fahrt)
#print(tagesverteilung)