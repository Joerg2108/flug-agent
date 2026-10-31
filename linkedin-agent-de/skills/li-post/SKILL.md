---
name: li-post
description: >-
  Schreibt aus einer rohen Idee einen deutschen LinkedIn-Post mit 21 Hook-Formeln,
  in der eigenen Stimme des Nutzers, humanisiert, damit er nicht nach KI klingt.
  Verwenden, wenn der Nutzer einen LinkedIn-Post, einen Hook oder einen Entwurf
  will: "schreib einen Post über X", "mach daraus einen LinkedIn-Post", "gib mir
  Hook-Varianten". Liefert drei Hooks, einen fertigen Entwurf und einen
  kopierfertigen Block. Nichts wird ohne ausdrückliches Ja veröffentlicht.
---

# li-post

Macht aus einer rohen Idee einen LinkedIn-Post, der nach der Person klingt,
die ihn postet.

## Bevor du schreibst

1. Lies `~/.claude/linkedin/voice.md`, falls vorhanden. Das ist das
   Stimmprofil des Nutzers: wie er redet, was er nie sagt, für wen er
   schreibt, **ob er duzt oder siezt**. Gibt es die Datei nicht, frag nach
   **drei eigenen alten Posts**, leite die Stimme daraus ab und schreib die
   Datei. Nicht überspringen und keine Stimme erfinden. Ein Post in der
   falschen Stimme ist schlimmer als gar keiner.
2. Lies `hooks.json` in diesem Ordner: alle 21 Formeln mit Vorlage, Beispiel,
   Einsatzzweck und typischer Falle. Die Beispiele sind erfunden und zeigen
   nur die Form.
3. Wenn die Idee dünn ist („Post über KI“), nicht aufblasen. Stell eine
   gebündelte Frage: Was ist passiert, wem, und was hat es gekostet oder
   gebracht? Ein Post braucht eine konkrete, wahre Sache. Hol sie dir vorher.

## Die Form

LinkedIn belohnt Verweildauer, Speichern und Kommentare, in dieser Reihenfolge:

```
Zeile 1     der Hook. Allein. Muss den Abschnitt bei ~140 Zeichen (mobil) überleben.
Zeile 2     die Auflösung von Zeile 1, kein Anlauf für Zeile 3.
Hauptteil   kurze Absätze, 1-3 Zeilen, Leerzeile zwischen jedem.
            Keine Textwand. Der Weißraum ist das Format.
Die Wende   eine Zeile, die das Vorherige neu einordnet.
Schluss     eine konkrete Frage ODER eine Handlungsanweisung. Nie beides.
```

Länge: 900-1.300 Zeichen ist der Arbeitsbereich für einen Textpost. Deutsche
Sätze sind länger als englische, also lieber kürzen als ausreizen. Unter 400
liest sich wie ein Gedanke, nicht wie ein Post. Über 2.000 muss sich jede Zeile
verdienen.

## Ablauf

**1. Drei Hooks, nicht einer.** Lass die Idee durch `hooks.json` laufen und
wähl die drei Formeln, die wirklich passen. Verschiedene Formeln, nicht drei
Varianten derselben. Als drei nummerierte Zeilen zeigen und in einem Satz
sagen, welchen du nehmen würdest und warum.

**2. Den ganzen Post** auf dem stärksten Hook schreiben.

**3. Humanisieren.** Den Entwurf durch `/li-human` jagen, bevor du ihn zeigst
(Entwurf in eine Datei schreiben, `humanize.py --report`, markierte Stellen
selbst umschreiben, `detect.py`). Jeder Post aus diesem Skill wird
humanisiert. Das ist kein optionaler Extraschritt.

**4. Den Block ausgeben.** Kopierfertig, in einem Codeblock, genau so, wie er
eingefügt werden soll. Darunter:

```
POST FERTIG
Hook:        #17 Zeitanker
Länge:       1.140 Zeichen
Humanizer:   6 Artefakte entfernt, Mensch-Wert 84 OK
Posten am:   Dienstag 8:15 Uhr (aus deinem Plan)

Antworte mit "ja" zum Loggen, oder sag mir, was ich ändern soll.
```

**5. Nie selbst veröffentlichen.** Dieser Skill produziert Text. Der Nutzer
postet. Bei „ja“ den Post an `~/.claude/linkedin/log.md` anhängen, mit Datum,
Hook-Nummer und erster Zeile, damit `/li-audit` später eine Historie hat.

## Regeln, die den Unterschied machen

- **Eine Idee pro Post.** Hat der Entwurf zwei, sind es zwei Posts. Sag das.
- **Zahlen statt Adjektive.** „1.800 €“ schlägt „eine Menge“. Fehlt die Zahl,
  frag danach, statt um das Loch herumzuschreiben.
- **Kein Engagement-Köder.** „Was denkt ihr?“ und „Wer kennt das?“ sind tot.
  Die Schlussfrage muss eine sein, die nur dieser Post stellen kann.
- **Kein Denglisch, wo es ein deutsches Wort gibt.** Learnings, Insights,
  Mindset, Impact, Gamechanger: der Humanizer meckert die an, und zwar zu Recht.
- **Höchstens drei Hashtags**, am Ende, und nur echte Kategorien, denen Leute
  folgen.
- **Keine Links im Post.** LinkedIn drosselt Posts mit externen Links. Link in
  den ersten Kommentar und das im Beleg dazuschreiben.
- **Nie erfinden.** Keine ausgedachten Zahlen, Kunden, Umsätze oder Ergebnisse
  unter dem Namen des Nutzers, auch nicht als Platzhalter. Fehlt eine Zahl,
  `{{deine Zahl}}` im Entwurf lassen und darauf hinweisen.
- **Rechtlich sauber bleiben.** Keine Namen von Auftraggebern, Kollegen oder
  Mietern ohne Freigabe, keine Details aus vertraulichen Einsätzen (Objekt,
  Adresse, Sicherheitslücken). Im Zweifel anonymisieren und den Nutzer fragen.

## Beispiel

```
/li-post wir haben eine Vorlage gebaut, die den Wachbericht von 45 auf 10 Minuten drückt
```

```
HOOKS
1. #17 Zeitanker      Ein Wachbericht hat mich früher 45 Minuten gekostet. Heute sind es 10.
2. #12 Vergleich      Eine teure Software gegen eine Word-Vorlage mit 6 Feldern. Die Vorlage hat gewonnen.
3. #3  Fehler         Zwei Jahre lang habe ich nach jeder Schicht eine Stunde für Formatierung verschenkt.

Ich nehme #17: Das Verhältnis ist glaubwürdig und die Zahl ist deine.
```
