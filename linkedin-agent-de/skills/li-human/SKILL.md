---
name: li-human
description: >-
  Entfernt den Maschinen-Fingerabdruck aus deutschen Texten - Geviertstriche,
  englische Anführungszeichen, KI-Floskeln, unsichtbare Zeichen - und bewertet
  den Text mit fünf Prüfungen, bevor er rausgeht. Verwenden, wann immer ein
  Text menschlich klingen soll: "humanisieren", "klingt das nach KI", "mach
  das weniger KI-mäßig", "Floskeln raus", "wird das erkannt", sowie vor jedem
  LinkedIn-Post, Kommentar, jeder Antwort oder DM, die dem Nutzer gezeigt wird.
---

# li-human

In diesem Ordner liegen zwei Werkzeuge, und beide laufen wirklich. Benutz sie.
Nicht nach Augenmaß schätzen.

```bash
python3 humanize.py entwurf.txt --report          # bereinigen, Änderungen zeigen
python3 detect.py entwurf.txt                      # bewerten, fünf Prüfungen
python3 detect.py vorher.txt nachher.txt           # Verbesserung belegen
python3 humanize.py entwurf.txt --striche komma    # Gedankenstriche zu Kommas
```

Beide lesen `slop.json`, das Lexikon: rund 120 deutsche Floskeln, Buzzwords
und Denglisch-Begriffe, 17 Klassen unsichtbarer Zeichen und 14 Strukturmuster.
Es ist zum Bearbeiten gedacht. Wenn der Nutzer ein Wort bewusst verwendet, das
das Lexikon anmeckert, nimm es raus.

## Was automatisch korrigiert wird

**1. Unsichtbare Zeichen.** Zero-Width-Zeichen, Word Joiner, weiche
Trennstriche, BOMs, Unicode-Tag-Zeichen, geschützte und schmale Leerzeichen.
Keine Tastatur erzeugt die. Sie überleben Copy-Paste und sind das
mechanischste Merkmal generierter Texte.

**2. Typografie - deutsch-korrekt, nicht englisch.**

| vorher | nachher | warum |
| --- | --- | --- |
| `—` Geviertstrich | ` – ` Gedankenstrich | im Deutschen nie korrekt, typisch für übersetzten KI-Text |
| `“so”` englisch | `„so“` deutsch | `”` als Schlusszeichen gibt's im Deutschen nicht |
| `’` | `'` | einheitlicher Apostroph |
| `…` | `...` | |
| `•` am Zeilenanfang | `-` | |

**Bleibt stehen:** deutsche Anführungszeichen `„…“`, einzelne Gedankenstriche
` – ` und Bis-Striche (`6–14 Uhr`). Das ist korrekter deutscher Satz, kein
KI-Merkmal. Ab drei Gedankenstrichen pro Post wird aber markiert, denn
KI-Texte übertreiben genau das.

**3. Floskeln.** „In der heutigen schnelllebigen Welt“, „von entscheidender
Bedeutung“, nahtlos, maßgeschneidert, ganzheitlich, Learnings, Mehrwert und
der Rest werden durch schlichte Wörter ersetzt. Die **Endung bleibt erhalten**
(„nahtlosen“ wird „reibungslosen“), die Großschreibung am Satzanfang auch, URLs
bleiben unberührt.

## Was NICHT automatisch korrigiert wird

Im Deutschen bricht eine blinde Ersetzung schnell die Grammatik (Genus,
trennbare Verben, Verbzweitstellung). Deshalb werden viele Einträge nur
**markiert**:

- Floskeln ohne sauberen Ersatz: „spannend“, „Mindset“, „Impact“, „auf das
  nächste Level“, „Potenzial entfalten“, „das ist kein Zufall“ ...
- Verstärker am Satzanfang: „Zweifellos ist das wichtig“ würde nach dem
  Löschen zu „Ist das wichtig“, also zur Frage. Wird markiert, nicht gelöscht.

Und die **Strukturmuster**, weil man für einen Satzumbau Urteilsvermögen
braucht:

- „Nicht nur X, sondern auch Y“ / „Es geht nicht um X, es geht um Y“
- „Das ist nicht X. Das ist Y.“
- Rhetorische Ein-Wort-Zeilen: „Das Ergebnis?“
- Inszenierte Pointen: „Spoiler:“, „Fakt ist:“, „Die bittere Wahrheit:“
- „Kennst du das?“ / „Stell dir vor“ als Einstieg
- „Ich freue mich, mitteilen zu dürfen ...“
- Dreierketten „A, B und C.“
- Rakete, Feuer, Glühbirne, Funkeln, Zielscheibe
- Hashtag-Wände, „Fazit:“, „Was denkt ihr?“
- Gehäufte Gedankenstriche, gleich lange Sätze, gleich lange Aufzählungen

Diese Liste ist dein Job. Schreib jede markierte Stelle von Hand um, behalte
die Aussage, und lass `detect.py` nochmal laufen. Genau dieser Schritt bringt
den Wert von PRÜFEN auf OK, und genau den kann kein Skript.

## Die fünf Prüfungen

`detect.py` bewertet fünf Signale von 0 bis 100, höher ist menschlicher:

| Prüfung | was gemessen wird | so sieht Maschine aus |
| --- | --- | --- |
| RHYTHMUS | Variation der Satzlängen | jeder Satz gleich lang |
| KONKRETHEIT | Zahlen, €/%, Uhrzeiten, Kürzel (IHK, DGUV), Paragrafen, wörtliche Rede pro 100 Wörter | abstrakte Substantive, keine Fakten |
| FLOSKELN | Lexikon-Treffer pro 100 Wörter | Buzzword-Bingo |
| FINGERABDRUCK | unsichtbare Zeichen, Geviertstriche, englische Anführung, gehäufte Gedankenstriche pro 1.000 Zeichen | englische Typografie in deutschem Text |
| STIMME | Umgangssprache und Modalpartikeln (halt, eben, mal, ja, echt, geht's), ich/du/wir, Strukturmuster | steril, unpersönlich, inszeniert |

Das Urteil gewichtet den Mittelwert mit 60 % und die **schwächste einzelne
Prüfung** mit 40 %, weil ein Detektor nur ein Signal braucht. OK braucht
insgesamt 70+ und keine Prüfung unter 55.

**Hinweis zu Du/Sie:** Ein Post in Sie-Form hat naturgemäß weniger
Umgangssprache. Wenn `voice.md` „Sie“ vorgibt, ist ein STIMME-Wert um 50
normal. Erzwing dann keine Lockerheit, die nicht zum Nutzer passt.

## Ehrlich bleiben

Das sind fünf lokale Heuristiken, angelehnt an die Signale öffentlicher
Detektoren. Sie laufen komplett auf dem Rechner des Nutzers, nichts wird
hochgeladen. Sie sind **nicht** GPTZero, Originality, Copyleaks oder Turnitin,
rufen deren APIs nicht auf und können deren Urteil nicht versprechen. Sag dem
Nutzer nie, sein Text sei „unerkennbar“.

## Reihenfolge

1. `humanize.py entwurf.txt -o sauber.txt --report`
2. Markierte Floskeln und Strukturmuster lesen. Diese Stellen selbst umschreiben.
3. `detect.py entwurf.txt sauber.txt` für Vorher/Nachher.
4. Wenn nicht OK: das schwächste Signal aus der Ausgabe beheben, nochmal.
   Zwei Runden sind normal. Fünf heißen, der Entwurf ist nach Schema F
   geschrieben, und die Lösung ist ein neuer Entwurf, nicht mehr Runden.
5. Dem Nutzer den bereinigten Text **und** den Wert zeigen. Nie nur den Wert.
