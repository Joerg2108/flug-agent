---
name: li-comment
description: >-
  Schreibt Kommentare unter fremde LinkedIn-Posts, die nach einem Menschen mit
  Meinung klingen, nicht nach einem Bot. Verwenden, wenn der Nutzer einen Post
  einfügt und einen Kommentar will: "kommentier das", "was schreib ich da
  drunter", "interagier mit dem Post", oder eine Runde Kommentare für seine
  Engagement-Zeit braucht.
---

# li-comment

Kommentieren ist der größte Hebel auf LinkedIn und gleichzeitig das, was man am
leichtesten verbockt. Ein Kommentar unter einem Post mit 400 Reaktionen wird
von mehr Leuten gesehen als die meisten eigenen Posts. Ein generischer wird
von niemandem gesehen und kostet Glaubwürdigkeit beim Autor.

## Eingabe

Der Nutzer fügt den Text des Posts ein (plus Name und Rolle des Autors, wenn
vorhanden). Bei einem Screenshot: lesen. Bei einer URL, die du nicht öffnen
kannst: um den Text bitten. Nicht raten, was drinstand, und keinen Browser
zum Auslesen des Feeds benutzen.

## Die neun Kommentartypen

Nach dem auswählen, was der Post wirklich ist. Nie standardmäßig Typ 1.

| # | Typ | wann | Form |
| --- | --- | --- | --- |
| 1 | **Datenpunkt ergänzen** | der Post behauptet etwas, das du mit einer Zahl stützen kannst | „Haben wir genauso erlebt: 40 % unserer ...“ |
| 2 | **Fehlenden Fall ergänzen** | der Post stimmt, ist aber unvollständig | „Gilt, bis {Bedingung}. Dann ...“ |
| 3 | **Respektvoll widersprechen** | du hältst es wirklich für falsch | erst die Zustimmung, dann die Abzweigung |
| 4 | **Eine Zeile weiterdenken** | ein Satz im Post ist der gute | zitieren, dann darauf aufbauen |
| 5 | **Die echte Frage stellen** | der Post hat den schwierigen Teil ausgelassen | eine Frage, konkret, kein „Bin gespannt auf ...“ |
| 6 | **Der Beleg** | du hast genau das selbst gemacht | was passiert ist, in zwei Sätzen |
| 7 | **Die Korrektur** | es gibt einen Sachfehler | richtig, kurz, freundlich, sicher |
| 8 | **Neu einordnen** | richtige Fakten, falscher Rahmen | „Man kann das auch so lesen:“ |
| 9 | **Der Einzeiler** | der Post braucht nichts, du willst präsent sein | unter 12 Wörter, muss witzig oder wahr sein |

## Regeln

- **2 bis 4 Sätze.** Länger wirkt wie eine Übernahme. Kürzer wie Füllmaterial.
- **Nie anfangen mit** „Toller Beitrag“, „Super Post“, „Sehr spannend“, „So
  wahr“, „Kann ich nur unterschreiben“, „Danke fürs Teilen“ oder dem Vornamen
  mit Ausrufezeichen. Alle sieben sind unsichtbar.
- **Kein Emoji am Anfang.** Kein 🔥 oder 👏 als erstes Zeichen.
- **Den Post nie nacherzählen.** Der Autor weiß, was er geschrieben hat, alle
  anderen auch.
- **Eine Idee.** Ein Kommentar mit zwei Punkten wirkt wie ein Blogversuch.
- **Das Konkrete sagen.** Wenn der Kommentar unter jedem Post zum Thema stehen
  könnte, ist es kein Kommentar, sondern Rauschen.
- **Widerspruch ist erlaubt und funktioniert**, aber die Zustimmung kommt
  zuerst und muss echt sein.
- **Du/Sie spiegeln.** Siezt der Autor in seinem Post, wird im Kommentar
  gesiezt. Sonst gilt die Vorgabe aus `voice.md`; im Zweifel duzen, das ist auf
  LinkedIn in Deutschland Standard.

## Ausgabe

**Zwei Optionen unterschiedlichen Typs**, beschriftet, plus ein Satz, welche du
posten würdest. Beide vorher durch `/li-human`. Ein Kommentar mit Geviertstrich
fällt mehr auf als ein Post, weil Kommentare kurz sind und genau gelesen werden.

```
KOMMENTAR-OPTIONEN  (zum Post von @Autor über Personalgewinnung)

[6 · Beleg]
Wir haben das ohne Lebenslauf bei 3 Einstellungen letztes Jahr probiert. Zwei
waren unsere besten Leute. Der Dritte war ein Reinfall, und der Unterschied
war, ob sie den Job vorher schon mal gemacht hatten, nicht das Gespräch.

[3 · Respektvoll widersprechen]
Beim Problem mit den Signalen bin ich bei dir. Geholfen hat uns aber nicht,
den Lebenslauf wegzulassen, sondern jedem Bewerber denselben bezahlten
Probedienst von 4 Stunden zu geben. Gleiches Ergebnis, viel weniger Diskussion.

Nimm den ersten. Eigene Zahlen, und er gibt einen Fehlschlag zu. Darauf
antworten Leute.
```

## Batch-Modus

Will der Nutzer eine Engagement-Runde: 5-10 Posts als eingefügten Text in einer
Nachricht anfordern, je einen Kommentar in einem Block zurückgeben, und in
`~/.claude/linkedin/log.md` festhalten, bei wem diese Woche schon kommentiert
wurde. Jeden Tag dieselben drei Leute zu kommentieren fällt auf, und es wirkt
genau so, wie es ist.

## Nie

Nicht automatisch posten. Kein Browser-Tool, um Kommentare im Namen des
Nutzers zu veröffentlichen. Automatisches Posten und Scraping verstoßen gegen
die LinkedIn-Nutzervereinbarung und gefährden das Konto. Dieser Skill schreibt
den Kommentar. Der Nutzer postet ihn.
