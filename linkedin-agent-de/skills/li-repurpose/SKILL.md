---
name: li-repurpose
description: >-
  Macht aus einem langen Inhalt - YouTube-Video, Podcast, Newsletter,
  Blogartikel, Transkript, Vortrag oder Kundengespräch - eine Woche
  LinkedIn-Posts. Verwenden, wenn der Nutzer sagt "verwerte das", "mach daraus
  Posts", "ich hab ein Video/einen Newsletter/ein Transkript", oder einen langen
  Text einfügt und ihn auf LinkedIn bringen will.
---

# li-repurpose

In einem guten langen Inhalt stecken vier bis sechs Posts. Die meisten holen
einen raus und werfen den Rest weg.

## Eingabe

Ein Transkript, ein Artikel, ein Newsletter, ein Skript, eine
Gesprächsnotiz. Gibt der Nutzer eine YouTube-URL und es gibt in der Sitzung ein
Transkript-Werkzeug, das benutzen; sonst um den Text bitten. Alles lesen, bevor
irgendetwas herausgezogen wird.

Bei Kundengesprächen und internen Unterlagen: vorher klären, was davon
öffentlich darf. Namen, Firmen, Objekte und Zahlen von Auftraggebern nur mit
Freigabe.

## Herausziehen, nicht zusammenfassen

Eine Zusammenfassung eines Videos ist kein Post. Keiner will die
Zusammenfassung. Den Inhalt durchgehen und rausziehen, was allein steht:

| Fund | was es ist |
| --- | --- |
| **Thesen** | jeder Satz, der eine Diskussion auslösen würde |
| **Zahlen** | jede Zahl, jeder Betrag, jede Dauer, jeder Prozentwert |
| **Geschichten** | jeder Moment mit einer Person, einer Szene und einem Preis |
| **Mechanismen** | jede „so funktioniert das“-Erklärung |
| **Fehler** | jedes Eingeständnis, dass etwas schiefging |
| **Sätze** | jeder Satz, der schon so zitierfähig ist |

Erst auflisten, was gefunden wurde, mit Anzahl, bevor irgendetwas geschrieben
wird. Ergibt der Inhalt weniger als vier Funde, ist er dünn, und vier daraus
gepresste Posts sind es auch. Sag das.

## Dann die Woche bauen

Jeder Fund wird ein Post, und jeder Post muss komplett für sich stehen. Der
Leser hat das Video nicht gesehen und wird es nie sehen. Nie „wie in meinem
letzten Video erwähnt“ schreiben. Der Post ist die Sache.

Jedem eine Hook-Formel aus `li-post/hooks.json` zuweisen, und variieren: Fünf
Posts aus einer Quelle mit derselben Hook-Form lesen sich wie eine
Content-Fabrik.

Über die Woche ordnen: die stärkste These zuerst, die Geschichte in der Mitte,
der Mechanismus-Post zuletzt, wenn die Leute, denen die ersten gefallen haben,
darauf warten.

## Ausgabe

```
QUELLE: "Warum wir den Erstbesuch abgeschafft haben" (18 Min, 3.400 Wörter)

GEFUNDEN  4 Thesen, 6 Zahlen, 2 Geschichten, 3 Mechanismen, 1 Fehler, 5 zitierfähige Sätze

WOCHE
DI  #1  Gegenthese      Der Erstbesuch ist eine Steuer für eine schlechte Website
MI  #17 Zeitanker       6 Stunden pro Woche zurück, weil wir einen Kalenderlink gelöscht haben
DO  #9  Kaltstart       "Können wir nicht einfach kurz telefonieren?"
FR  #21 Direkter Nutzen Das Formular mit 4 Fragen, das den Termin ersetzt. Nimm es.

Sag "schreib Dienstag" und ich entwerfe ihn.
```

Dann auf Zuruf einzeln entwerfen, jeden durch `/li-post` und `/li-human`. Nicht
vier fertige Posts auf einmal abladen - die klingen dann alle gleich, und der
Nutzer bearbeitet keinen davon.
