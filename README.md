SIT trening automatisk oppmelding
Configurer når du vil melde deg opp i `sit_trening.yaml`

Installations you may need:

> pip install pyyaml
> pip install -U python-dotenv
> pip install -U selenium
> python -m pip install requests

Kan også hende man kan få problemer med geckodriver så det må reinstalleres. Evt. endre kodelinjen
webdriver.Firefox() til webdriver.dinNettLeser 

Need to also create ".env" file and copy paste below:
> name = ntnu_username
> password = ntnu_password
