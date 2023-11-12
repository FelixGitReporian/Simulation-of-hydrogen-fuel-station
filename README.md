# Simulation-of-hydrogen-fuel-station

Die Bachelorarbeit von Felix Hecht befasst sich mit der Bereitstellung von Wasserstoff im ländlichen Individualverkehr und dessen Integration in bestehende Infrastrukturen. Wasserstoff, ein umweltfreundlicher Energieträger, wird in Fahrzeugen eingesetzt, wobei Wasser als Nebenprodukt entsteht, was zu einer Reduktion von Treibhausgasemissionen im Verkehrssektor beiträgt. Ein wesentlicher Fokus der Arbeit liegt auf dem optimierten Betrieb von Wasserstofftankstellen in verschiedenen Regionen. Es wird untersucht, wie sich der Wasserstoffverbrauch in Fahrzeugen je nach Region unterscheidet, wobei festgestellt wurde, dass Fahrzeuge in zentralen und Kleinstädten einen höheren Wasserstoffverbrauch pro 100 km aufweisen als in Mittelstädten.

Die Arbeit analysiert auch, wie Tankstellen auf einen saisonal schwankenden Bedarf reagieren können, insbesondere durch Variationen in ihrer Dimensionierung. Es wird gezeigt, dass mit einer steigenden Anzahl an Zapfsäulen die Betriebskonfigurationen zunehmen, jedoch bei höheren Temperaturen abnehmen. Für unterschiedliche Regionen ergeben sich diverse Dimensionierungen der Nachfrage nach Wasserstoff. So kann beispielsweise eine Tankstelle in einer zentralen Stadt mit einer Zapfsäule einen täglichen Bedarf von etwa 86 kg (mit einer Schwankung von ± 54 kg) decken, während die gleiche Konfiguration in einer Kleinstadt nur einen Bedarf von etwa 51 kg (mit einer Schwankung von ± 29 kg) erfüllt. Zudem wurde festgestellt, dass die Betankungszeit mit steigender Umgebungstemperatur zunimmt, wobei eine Temperaturdifferenz von 48 °C die Betankungszeit um bis zu 173 Sekunden verlängern kann​​.


## Aufbau einer Wasserstofftankstelle:
Das Diagramm illustriert die Schlüsselkomponenten und den Arbeitsablauf einer Wasserstofftankstelle. Es zeigt den Weg des Wasserstoffs vom Elektrolyseur über verschiedene Kompressionsstufen bis hin zum Hochdruckbündel. Die Anlage umfasst auch Sensoren und Sicherheitsmechanismen, die während des Betankungsvorgangs des Fahrzeugs eine präzise Steuerung und Überwachung ermöglichen.
![Schematische Darstellung einer Wasserstofftankstelle](https://github.com/FelixGitReporian/Simulation-of-hydrogen-fuel-station/blob/main/Ergebnisse/Bilder/Wasserstofftankstelle%20technischer%20Aufbau.png)

## Verteilung der simulierten Fahrzeugmasse nach einem Tag:
Das Bild zeigt die Verteilung des Verkehrs auf Grundlage des statischen Fahrverhaltens des ländlichen Individualverkehrs (siehe Abschlussarbeit für Quellen und Berechnung, sowie Tankstellensimulation). Die Massenverteilung von Fahrzeugen nach einem Tag der Nutzung und am Anfang des spezifischen Stichtag variiert, je nachdem wie viele Fahrten gemacht wurden und diese in der jeweiligen Region verbrauchen. Die Daten der Verkehrssimulation sind entscheidend für die Analyse des Wasserstoffverbrauchs, da die Fahrzeugmasse direkt den Energiebedarf für die Fortbewegung beeinflusst. Die Fahrzeuge fangen Gaußverteilt mit einer Masse zwischen 30 bis 100% ihrer Tankmasse an und tanken Gaußverteilt zwischen 10 - 50 % des Restwertes. Die Fahrten pro Auto und Region werden ebenso gaußverteilt.
![Verteilung der simulierten Fahrzeugmasse des Verkehrs einer Region](https://github.com/FelixGitReporian/Simulation-of-hydrogen-fuel-station/blob/main/Ergebnisse/Bilder/Beispiel%20Verteilung_%20Verkehr%201.png)


## Fahrverhalten für eine bestimmte ländliche Region für eine Fahrt:
In diesem Bild wird der Zusammenhang zwischen der Geschwindigkeit, Beschleungigung und Gesamtfahrtstrecke bei einer Fahrt dargestellt. Dies entsprich einem bestimmten Fahrverhalten, wie er sonst für die Berechnung von CO2 und Stickoxiden verwendet wird.
![Fahrverhalten](https://github.com/FelixGitReporian/Simulation-of-hydrogen-fuel-station/blob/main/Ergebnisse/Bilder/Verkehr%203.png)

## Temperaturverlauf:
Dieses Bild veranschaulicht die mittlere Temperatur Deutschlands nach dem DWD, mit Durchschnittswerten für verschiedene Jahreszeiten. Diese Abhängigkeit ist kritisch für die Dimensionierung und das Management von Wasserstoff, aufgrund der Schwankung im Kühlenergiebedarf beim Betankungsprozess.
![Deutschlands durchschnittlicher Temperaturverlauf](https://github.com/FelixGitReporian/Simulation-of-hydrogen-fuel-station/blob/main/Ergebnisse/Bilder/Temperaturverlauf.png)

## Betankungsparameter:
Diese Tabelle präsentiert die Betankungsparameter für Wasserstofftankstellen, die nach dem SAE J2601 Standard klassifiziert sind. Sie veranschaulicht, wie unterschiedliche Umgebungstemperaturen und der anfängliche Tankdruck die Zielparameter für die Betankung beeinflussen, wie den Tankdruck (P_target) und die Auffüllrate (ΔPRR). Solche Daten sind entscheidend für die Anpassung der Betankungssysteme an variierende klimatische Bedingungen und stellen sicher, dass die Tankstellen effizient und sicher arbeiten.
![Tabelle der T40 Wasserstoffbetankung gemäß SAE J2601](https://github.com/FelixGitReporian/Simulation-of-hydrogen-fuel-station/blob/main/Ergebnisse/Bilder/Tabelle%20einer%20T40%20Wasserstoffbetankung%20gem%C3%A4%C3%9F%20SAE%20J2601.png)

## Resulatet Fahrzeug
Das Bild zeigt den Bedarf an Wasserstoff für eine Fahrt in einer Region aufgrund des entsprechenden Fahrverhaltens.
![Abbildung 1](https://github.com/FelixGitReporian/Simulation-of-hydrogen-fuel-station/blob/main/Ergebnisse/Bilder/Resulte%20Fahrzeuge%203.png)

## Resultate Betankung:
Die drei zwei Bilder zeigen die Temperatur- und Massenverteilung, sowie den nach den Betankungsparametern berechneten Strom eines Fahrzeugtanks während eines Betankungsprozesses.
![Abbildung 1](https://github.com/FelixGitReporian/Simulation-of-hydrogen-fuel-station/blob/main/Ergebnisse/Bilder/Betankung%20vergleich_%20Temperatur_%20Tank.png)
![Abbildung 2](https://github.com/FelixGitReporian/Simulation-of-hydrogen-fuel-station/blob/main/Ergebnisse/Bilder/Betankung%20vergleich_%20Masse_%20Tank.png)
![Abbildung 1](https://github.com/FelixGitReporian/Simulation-of-hydrogen-fuel-station/blob/main/Ergebnisse/Bilder/Betankung%20vergleich.png)

## Resultate 



