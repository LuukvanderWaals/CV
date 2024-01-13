# CV
Deze repository bevat een paar van de projecten die ik tijdens mijn studie heb gemaakt.

# Besturingssysteem
Bij deze opdracht moesten we een python programma schrijven die een paar eenvoudige operaties kan uitvoeren in het minix file systeem. De code kan op de volgende manier gebruikt worden.

Een nieuw textbestand aanmaken:
```
python mfstool.py disk.img touch <bestand naam>
```
Een nieuwe map aanmaken:
```
python mfstool.py disk.img mkdir <map naam>
```
Een bestand lezen:
```
python mfstool.py disk.img cat <bestand naam>
```
Tekst toevoegen aan een bestand:
```
python mfstool.py disk.img append "<tekst>"
```
# Route
Deze opdracht draaide om het implementeren van het A*-algoritme. Het algoitme moest je cre\"eren door simpelweg een paar stappen van de opdracht te volgen, maar de laatste stap was om je eigen idee toe te voegen aan het algoitme. Ik heb daarbij gekozen om een animatie toe te voegen in de terminal.

```
swipl vanderwaals.l.5.pl
?- route(<city1>, <city2>, Route, _), animate(Route).
```
Voor de twee steden kun je kiezen uit de volgende steden: amsterdam, breda, eindhoven, groningen, haarlem, hertogenbosch, leeuwarden, maastricht, rotterdam, utrecht, zwolle.

Bijvoorbeeld:
```
?- route(haarlem, maastricht, Route, _), animate(Route).
```
# Advent of Code

Een paar van de oplossingen die ik heb voor Advent of Code van 2022.
