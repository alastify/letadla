Vstupní úloha
=============

## Prerekvizity
Python3 a modul GeoBases3K

    $ pip install -r requirements.txt


## Spuštění

    $ python letadla.py [-i soubor] [-t cest] [-l letišť]


### Parametry
  * ``-i`` vstupní soubor (jinak se použije výchozí v adresáři projektu)
  * ``-t`` nejmenší počet hledaných cest (výchozí hodnota =  100)
  * ``-l`` počet navštívených letišť v rámci cesty (včetně výchozího a cílového) (výchozí hodnota = 10)


## Výstup
Výstupní soubor ``output.csv`` se ukládá do adresáře ``./output``.


## Algoritmus
V souboru ``./flyby/roundtrip.py`` je funkce ``hiker()``, která implementuje rekurzivní algoritmus pro hledání spojů.
