# Simulation-of-hydrogen-fuel-station

Die Bachelorarbeit von Felix Hecht befasst sich mit der Bereitstellung von Wasserstoff im ländlichen Individualverkehr und dessen Integration in bestehende Infrastrukturen. Wasserstoff, ein umweltfreundlicher Energieträger, wird in Fahrzeugen eingesetzt, wobei Wasser als Nebenprodukt entsteht, was zu einer Reduktion von Treibhausgasemissionen im Verkehrssektor beiträgt. Ein wesentlicher Fokus der Arbeit liegt auf dem optimierten Betrieb von Wasserstofftankstellen in verschiedenen Regionen. Es wird untersucht, wie sich der Wasserstoffverbrauch in Fahrzeugen je nach Region unterscheidet, wobei festgestellt wurde, dass Fahrzeuge in zentralen und Kleinstädten einen höheren Wasserstoffverbrauch pro 100 km aufweisen als in Mittelstädten.

Die Arbeit analysiert auch, wie Tankstellen auf einen saisonal schwankenden Bedarf reagieren können, insbesondere durch Variationen in ihrer Dimensionierung. Es wird gezeigt, dass mit einer steigenden Anzahl an Zapfsäulen die Betriebskonfigurationen zunehmen, jedoch bei höheren Temperaturen abnehmen. Für unterschiedliche Regionen ergeben sich diverse Dimensionierungen der Nachfrage nach Wasserstoff. So kann beispielsweise eine Tankstelle in einer zentralen Stadt mit einer Zapfsäule einen täglichen Bedarf von etwa 86 kg (mit einer Schwankung von ± 54 kg) decken, während die gleiche Konfiguration in einer Kleinstadt nur einen Bedarf von etwa 51 kg (mit einer Schwankung von ± 29 kg) erfüllt. Zudem wurde festgestellt, dass die Betankungszeit mit steigender Umgebungstemperatur zunimmt, wobei eine Temperaturdifferenz von 48 °C die Betankungszeit um bis zu 173 Sekunden verlängern kann​​.

## Verteilung der simulierten Fahrzeugmasse nach einem Tag:
Das Bild zeigt die Verteilung des Verkehrs auf Grundlage des statischen Fahrverhaltens des ländlichen Individualverkehrs (siehe Abschlussarbeit für Quellen und Berechnung, sowie Tankstellensimulation). Die Massenverteilung von Fahrzeugen nach einem Tag der Nutzung und am Anfang des spezifischen Stichtag variiert, je nachdem wie viele Fahrten gemacht wurden und diese in der jeweiligen Region verbrauchen. Die Daten der Verkehrssimulation sind entscheidend für die Analyse des Wasserstoffverbrauchs, da die Fahrzeugmasse direkt den Energiebedarf für die Fortbewegung beeinflusst.
![Verteilung der simulierten Fahrzeugmasse des Verkehrs einer Region](https://github.com/FelixGitReporian/Simulation-of-hydrogen-fuel-station/blob/main/Ergebnisse/Bilder/Beispiel%20Verteilung_%20Verkehr%201.png)


## Fahrverhalten für eine bestimmte ländliche Region für eine Fahrt:
Dieses Bild wird der Zusammenhang zwischen der Geschwindigkeit der Fahrzeuge und ihrem Wasserstoffbedarf über Zeit dargestellt. Die Kurven zeigen die Schwankungen der Geschwindigkeit im Tagesverlauf und den entsprechenden Wasserstoffverbrauch, was für die Planung der Kapazität von Wasserstofftankstellen von Bedeutung ist.
![Fahrverhalten](https://github.com/FelixGitReporian/Simulation-of-hydrogen-fuel-station/blob/main/Ergebnisse/Bilder/Resulte%20Fahrzeuge%203.png)

## Temperaturverlauf:
Dieses Bild veranschaulicht die mittlere Temperatur Deutschlands nach dem DWD, mit Durchschnittswerten für verschiedene Jahreszeiten. Diese Abhängigkeit ist kritisch für die Dimensionierung und das Management von Wasserstoff, aufgrund der Schwankung im Kühlenergiebedarf beim Betankungsprozess.
![Deutschlands durchschnittlicher Temperaturverlauf](https://github.com/FelixGitReporian/Simulation-of-hydrogen-fuel-station/blob/main/Ergebnisse/Bilder/Temperaturverlauf.png)
