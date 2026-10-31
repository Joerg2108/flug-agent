---
name: li-profile
description: >-
  Bewertet ein LinkedIn-Profil mit bis zu 100 Punkten nach 12 Kriterien und
  schreibt die Teile um, die Punkte kosten - Headline, Info, Berufserfahrung,
  Im Fokus, Titelbild. Verwenden, wenn der Nutzer sagt "optimier mein Profil",
  "bewerte mein LinkedIn", "schreib meine Headline neu", "mach meinen Info-Text
  besser", oder sein Profil einfügt und fragt, wie es wirkt.
---

# li-profile

Ein Profil ist kein Lebenslauf. Ein Lebenslauf beantwortet „was hast du
gemacht“. Ein Profil beantwortet „sollte ich dieser Person schreiben“, und zwar
in etwa vier Sekunden, aus der Headline und den ersten zwei Zeilen des
Info-Texts.

## Eingabe

Den Nutzer bitten, einzufügen: Headline, Info-Text, aktuelle Position und die
letzten zwei Einträge der Berufserfahrung, plus ob er ein Titelbild und einen
„Im Fokus“-Bereich hat. Für den ersten Durchgang reicht ein Screenshot der
oberen Profilkarte. Nicht im Namen des Nutzers bei LinkedIn einloggen.

## Bewerten

Lies `rubric.json` in diesem Ordner: zwölf Punkte, 100 Punkte gesamt, jeweils
mit Beschreibung, wie volle Punktzahl aussieht. Jeden Punkt bewerten, Tabelle
zeigen, Summe nennen. Ehrlich sein: Die meisten Profile landen beim ersten
Durchgang in den 30ern und 40ern, und eine großzügige Bewertung ist nutzlos.

```
PROFIL-WERT  41/100

  Headline                3/12   nur Jobbezeichnung, kein Ergebnis, keine Zielgruppe
  Info, erste 2 Zeilen    2/10   fängt mit "leidenschaftlich" an
  Info, Rest              4/10   Werdegang statt Angebot
  Im Fokus                0/8    leer
  Titelbild               0/6    Standard-Blau
  ...
```

## Dann umschreiben, in dieser Reihenfolge

Nach verlorenen Punkten absteigend. Nicht alles auf einmal - der Nutzer muss
jeden Teil selbst einfügen.

**1. Headline (220 Zeichen).** Die Formel, die funktioniert:
`{was du für wen tust} | {Beleg} | {wie man startet}`. Nicht die
Jobbezeichnung. Nicht „Ich helfe X, Y zu erreichen“ als die ersten Wörter, so
fängt inzwischen jedes zweite Profil an. Drei Optionen geben.

Beispiel-Form (erfunden):
`Objektschutz für Logistik-Standorte in Sachsen | 0 Einbrüche seit 2022 an meinen Objekten | Geprüfte Schutz- und Sicherheitskraft (IHK)`

**2. Info, erste zwei Zeilen.** Alles nach Zeile 2 steckt mobil hinter
„... mehr“, also sind diese zwei Zeilen für die meisten Leser der ganze
Info-Text. Sie müssen sagen, wem du hilfst und was sich ändert. Kein
„leidenschaftlich“, kein „ergebnisorientiert“, keine Bio in der dritten Person,
kein Einstieg mit dem eigenen Namen.

**3. Info, Rest.** An einen Leser geschrieben, in der Anrede aus `voice.md`.
Aufbau: das Problem des Lesers, was du dagegen tust, ein Beleg mit Zahl, was er
als Nächstes tun soll. Unter 1.400 Zeichen, auch wenn 2.600 erlaubt sind.

**4. Im Fokus.** Drei Einträge: der beste Post, der Beleg, der Kontaktweg. Ein
leerer Fokus-Bereich sind acht Punkte, und das ist der einzige Ort im Profil,
den du komplett selbst kontrollierst.

**5. Berufserfahrung.** Jede Position bekommt eine Zeile zum Umfang und zwei bis
drei Punkte, die Ergebnisse mit Zahlen sind, keine Aufgaben. Alles älter als
zehn Jahre auf eine Zeile kürzen.

**6. Titelbild.** Ein Satz Positionierung und ein Kontaktweg. Der
Standard-Verlauf ist das deutlichste Signal auf der Seite, dass keiner zu Hause
ist.

## Ausgabe

Bewertungstabelle, dann die Umschreibungen als kopierfertige Blöcke in
Reparatur-Reihenfolge, jeder schon durch `/li-human`. Am Ende neu bewerten und
die Differenz ehrlich zeigen: Landet die Überarbeitung bei 88 und nicht bei 98,
sag 88, und sag, was die fehlenden Punkte brauchen (meist Empfehlungen, ein
echtes Titelbild und Posting-Historie, die kann kein Umschreiben erzeugen).

Dieser Skill speichert nichts bei LinkedIn. Der Nutzer fügt jeden Abschnitt
selbst ein. Keine Abschlüsse, Zertifikate oder Ergebnisse erfinden, die der
Nutzer nicht genannt hat.
