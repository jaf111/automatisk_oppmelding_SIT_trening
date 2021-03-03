Automatisk oppmelding for SIT trening. Jeg har prøvd å gjøre mitt beste (men jeg ville ikke bruke mange timer så derfor er koden litt dårlig strukturert) :) Tar gjerne i mot forslag til endringer! 

# Hvordan repoet fungerer #

I stedet får å bruke masse tid på logge inn på sit.no/trening så trengs det bare å kjøre dette skripte her så er du oppmeldt til egentrenig på SIT 

# Hvordan sette opp #

Konfigurer `sit_trening.yaml` slik at du blir meldt opp til riktig tidspunkt (Støtter bare treningssenter i Trondheim).

Må sette ntnu passord og brukernavn i ".env" fila (får å logge inn med Feide).

Run: sit_trening.py

Hvis du ønsker å melde deg opp til flere tidspunkt, så må du bare endre `sit_trening.yaml` tid og kjøre skripte på nytt. 

# Feilsøking #

Installations you may need:

> pip install pyyaml

> pip install -U python-dotenv

> pip install -U selenium

> python -m pip install requests

Kan også hende man kan få problemer med geckodriver så det må reinstalleres. Evt. endre kodelinjen
webdriver.Firefox() til webdriver.dinNettLeser()

Hvis noen andre feilmedlinger skulle forekomme så kjør skripte på nytt eller sjekk at du har nett :) 

OBS: Har bare testet for Ubuntu 20.04 og brukt python 3.8.

# Kjente feil #

- Skripte kan brukes til å melde deg opp til timer senere enn 48h men du blir egentlig ikke meldt opp :(

- Skripte lar deg melde deg opp til like timer på forskjellige trenigssenter selv om det ikke egentlig går.

- 
