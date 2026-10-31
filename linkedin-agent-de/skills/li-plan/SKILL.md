---
name: li-plan
description: >-
  Plant die LinkedIn-Woche - was gepostet wird, wann, und mit wem interagiert
  wird. Verwenden, wenn der Nutzer sagt "plan meine Woche", "was soll ich
  posten", "Redaktionsplan", "Content-Kalender", "mir fällt nichts ein", oder
  einen Posting-Plan und eine Engagement-Liste will.
---

# li-plan

Die Zentrale. Alles andere in diesem Paket führt aus, das hier entscheidet,
was ausgeführt wird. Einmal pro Woche laufen lassen, immer am selben Tag.

## Eingabe

Wenn `~/.claude/linkedin/voice.md` und `log.md` existieren, lesen. Der Plan
soll kein Thema der letzten zwei Wochen wiederholen. Gibt es sie nicht, nach
vier Dingen fragen und sie aufschreiben:

1. Was der Nutzer anbietet, und wem.
2. Die drei oder vier Themen, für die er bekannt sein will.
3. Was diese Woche wirklich passiert ist: ein Kundengespräch, eine Zahl, ein
   Fehler, etwas Gebautes, eine Diskussion. Daraus entstehen Posts.
4. Zehn bis zwanzig Personen oder Firmen, bei denen er sichtbar sein will.

## Was gepostet wird

Vier Posts pro Woche schlagen sieben. Regelmäßigkeit ist die Untergrenze, kein
Ziel, und der fünfte Post einer Woche ist fast immer der schwache, der den
Schnitt runterzieht. Für den Anfang sind auch zwei bis drei völlig in Ordnung.

Über die Woche mischen, nie zweimal denselben Typ hintereinander:

| Typ | Anteil | Aufgabe |
| --- | --- | --- |
| **Beleg** | 1 pro Woche | etwas, das passiert ist, mit Zahl |
| **Meinung** | 1 pro Woche | eine Position, die Follower kosten könnte |
| **Wissen** | 1 pro Woche | eine Sache, die der Leser heute umsetzen kann |
| **Geschichte** | 1 alle zwei Wochen | eine Szene mit Dialog und einem Preis |
| **Angebot** | 1 alle zwei Wochen | was du anbietest, klar gesagt, ohne Entschuldigung |

Für jeden Slot: das Thema, der konkrete Winkel aus dem, was diese Woche
passiert ist, und die Hook-Nummer aus `li-post/hooks.json`. Kein Thema, ein
Winkel. „Sicherheit“ ist kein Plan. „Der Lieferant, der um 23:40 ohne
Lieferschein am Tor stand“ ist ein Post.

## Wann gepostet wird

Posten, wenn das Publikum am Schreibtisch sitzt. Für ein deutsches
B2B-Publikum ist Dienstag bis Donnerstag, 7:30-9:30 Uhr der Standard, mit
12:00-13:00 Uhr (Mittagspause) und Montagnachmittag als zweite Wahl. Freitag
ab Mittag ist tot. Wochenenden nur für persönliche Geschichten oder gar nicht.

Für Schichtarbeiter als Zielgruppe (z. B. Sicherheitsdienst) gilt das nur
eingeschränkt: Die lesen eher zum Schichtwechsel, abends ab 19 Uhr oder am
Wochenende. Die eigenen Zahlen aus `/li-audit` schlagen jede Regel.

Aber klar sagen: **Tag und Uhrzeit zählen viel weniger als eine gute erste
Zeile.** Wenn der Nutzer Posting-Zeiten optimiert, bevor seine Hooks
funktionieren, poliert er das Falsche, und das solltest du ihm sagen.

## Mit wem interagiert wird

Eine Liste mit 10, dreigeteilt:

- **5 Reichweite**: Leute mit einem Publikum, das der Nutzer will, und deren
  Posts er wirklich etwas hinzufügen kann. Kommentieren, bevor 20 Kommentare
  drunter stehen, sonst sieht es keiner.
- **3 Kollegen**: gleiche Ebene, gleiches Feld. Das ist die Gruppe, die
  zurückgibt.
- **2 Entscheider**: Leute, die wirklich kaufen, beauftragen oder einstellen
  könnten. Wochenlang ihre Posts kommentieren, bevor irgendeine DM kommt, und
  nie in einem Kommentar verkaufen.

20 Minuten am Tag, vor dem Posten, nicht danach. Kommentare unter fremden Posts
sorgen dafür, dass der eigene Post ankommt.

## Ausgabe

```
WOCHE AB 9. SEPTEMBER

MO   nur interagieren  (20 Min, Liste unten)
DI   8:15  BELEG       #17 Zeitanker     - Wachbericht von 45 auf 10 Minuten
MI   nur interagieren
DO   8:00  MEINUNG     #1  Gegenthese    - warum Präsenz allein nichts bringt
FR   8:30  WISSEN      #21 Direkter Nutzen - die Übergabe-Checkliste, verschenkt
SA   -
SO   18:00 GESCHICHTE  #9  Kaltstart     - "Sie haben mir hier gar nichts zu sagen"

INTERAGIEREN  (5 Reichweite / 3 Kollegen / 2 Entscheider)
  ...

Sag "schreib Dienstag" und ich entwerfe ihn.
```

Den Plan nach `~/.claude/linkedin/plan.md` schreiben, damit die anderen Skills
ihn lesen können. Nichts wird irgendwo geplant oder gepostet. Das ist ein Plan,
und der Nutzer setzt ihn um.
