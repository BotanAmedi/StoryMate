# Kwaliteitscontrole User Story

Voer onderstaande controle uit voordat een User Story wordt gegenereerd.

## 1. Actor controle

Gebruik nooit een generieke actor zoals:

* gebruiker
* medewerker
* eindgebruiker

wanneer een specifiekere actor uit de context kan worden afgeleid.

Voorbeelden:

* HR-medewerker
* Nieuwe medewerker
* Functioneel Beheerder
* Servicedeskmedewerker
* Teamleider
* Inwoner
* Leverancier

Indien de actor niet duidelijk is, stel maximaal 1 aanvullende vraag.

---

## 2. Gebruikerswaarde controle

Een User Story moet altijd een duidelijke gebruikerswaarde bevatten.

Gebruik het format:

Als [actor]
wil ik [functionaliteit]
zodat [gebruikerswaarde]

Controleer of het onderdeel "zodat" daadwerkelijk een voordeel beschrijft.

Goedgekeurd:

"zodat nieuwe medewerkers direct kunnen starten"

Afgekeurd:

"zodat een workflow wordt gestart"

---

## 3. Oplossing versus behoefte

Focus op het probleem en de gewenste uitkomst.

Vermijd technische oplossingen als primaire User Story.

Voorbeeld:

Input:
"Maak een Python script dat laptops registreert"

Slecht:
"Als beheerder wil ik een Python script"

Goed:
"Als Servicedeskmedewerker wil ik automatisch laptopregistraties laten verwerken zodat handmatige registratie niet meer nodig is"

---

## 4. INVEST controle

Controleer iedere User Story op INVEST.

Independent
Negotiable
Valuable
Estimable
Small
Testable

Wanneer een User Story niet voldoet aan Small of Estimable moet deze als Epic worden beoordeeld.

---

## 5. Epic beoordeling

Beoordeel eerst of het verzoek een Epic of User Story is.

Beschouw een item als Epic wanneer:

* meerdere functionaliteiten aanwezig zijn
* meerdere processen geraakt worden
* het niet binnen één sprint kan worden gerealiseerd
* aanvullende opsplitsing noodzakelijk is

Voorbeelden van Epics:

* Website bouwen
* MFA implementeren
* Onboardingproces automatiseren
* Nieuw zaaksysteem invoeren

Wanneer een Epic wordt vastgesteld:

* genereer geen User Story
* geef eerst een Epic beoordeling
* splits de Epic op in meerdere User Stories

---

## 6. Acceptatiecriteria

Gebruik altijd Given / When / Then.

Formaat:

Given [beginsituatie]

When [actie]

Then [verwacht resultaat]

Voorbeeld:

Given een nieuwe medewerker heeft een startdatum

When het onboardingproces wordt gestart

Then wordt automatisch een laptop toegewezen

Gebruik minimaal 3 acceptatiecriteria indien voldoende informatie beschikbaar is.

---

## 7. Story Point regel

Verzin nooit Story Points.

De AI beschikt niet over voldoende context om een betrouwbare inschatting te maken.

Gebruik:

Schatting: Door het team te bepalen

of

Indicatie: Klein / Middel / Groot

zonder numerieke Story Points.

---

## 8. Laatste kwaliteitscontrole

Controleer vóór oplevering:

* Is de actor specifiek?
* Is de gebruikerswaarde duidelijk?
* Is het een User Story en geen Epic?
* Zijn de acceptatiecriteria in Given/When/Then formaat?
* Is geen technische oplossing als gebruikerswaarde gebruikt?
* Zijn geen Story Points verzonnen?
* Is de Story begrijpelijk voor een niet-technische gebruiker?

Indien één van bovenstaande controles faalt, verbeter de User Story voordat deze wordt getoond.
