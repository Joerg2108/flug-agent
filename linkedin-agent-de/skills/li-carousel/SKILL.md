---
name: li-carousel
description: >-
  Baut einen LinkedIn-Dokument-Post (Karussell) - Text Folie für Folie, das
  Titelblatt, das zum Wischen bringt, und die PDF zum Hochladen. Verwenden, wenn
  der Nutzer sagt "Karussell", "Dokument-Post", "Slides für LinkedIn", "mach
  daraus ein Karussell", oder eine listenförmige Idee hat, die als Textpost
  eingehen würde.
---

# li-carousel

Dokument-Posts haben auf LinkedIn die höchste Verweildauer, weil jedes Wischen
zählt und Scrollen nicht. Das Format belohnt eine Idee in Schritten. Es bestraft
einen Textpost, der in Stücke geschnitten wurde.

## Wann statt eines Textposts

Ein Karussell, wenn die Idee eine **Abfolge** hat: Schritte, ein Countdown, ein
Vorher/Nachher-Verlauf, ein Modell mit Teilen. Ein Textpost, wenn die Idee eine
einzelne Aussage ist. Eine Aussage auf acht Folien zu verteilen ist der
häufigste Grund, warum Karussells scheitern. Wenn der Nutzer genau das hat, sag
es und gib ihn an `/li-post` weiter.

## Aufbau

8-12 Folien. Unter 8 ist es ein Textpost. Über 12 bricht die Abschlussrate ein.

```
1        TITEL        der Hook, höchstens 6 Wörter, plus eine Zeile Versprechen
2        DIE FALLHÖHE warum das wichtig ist, in einem Satz
3-N      EINE IDEE PRO FOLIE. Überschrift mit 3-7 Wörtern, darunter höchstens
                      25 Wörter. Braucht eine Folie einen Absatz, sind es zwei Folien.
N+1      ÜBERSICHT    alles als Liste, damit der Screenshot nützlich ist
LETZTE   AUFFORDERUNG eine Handlung. Folgen, ein Stichwort kommentieren, oder der Link. Eins.
```

## Regeln für den Folientext

- **Folie 1 macht 80 % des Ergebnisses.** Sechs Wörter. Groß. Der Rest kann
  ein Titelblatt nicht retten, über das keiner wischt.
- **Jede Folie nummerieren** (3/10). Die Abschlussrate steigt, wenn man das Ende
  sieht.
- **Keine Folie ist ein Absatz.** Geht es nicht in 25 Wörtern, teilen. Deutsche
  Komposita sind lang: „Sicherheitsdienstleistungsunternehmen“ sprengt eine
  Zeile in 48 pt. Lieber „Sicherheitsfirma“.
- **Die Übersichtsfolie wird gescreenshottet.** Sie muss allein funktionieren.
- **Der Name des Nutzers auf jeder Folie**, klein, unten in der Ecke.
  Screenshots reisen ohne dich.

## Die PDF bauen

LinkedIn will eine PDF, 1080×1350 (4:5) für maximale Fläche im Feed, unter
100 MB, unter 300 Seiten. Als HTML bauen und zu PDF drucken:

```bash
# eine Seite pro Folie, 1080x1350, keine Ränder, dann z. B.:
chromium --headless --no-sandbox --print-to-pdf=karussell.pdf --no-pdf-header-footer karussell.html
```

Im HTML eine `<section>` pro Folie mit `width:1080px; height:1350px;
page-break-after:always`, eine einzige Akzentfarbe, keine Schrift unter 28 px,
weil die Leute das am Handy in Vorschaugröße lesen, und `@page { size: 1080px
1350px; margin: 0 }`. Gibt es im Projekt einen Markenstil oder ein
Designsystem, das verwenden und keine eigene Palette erfinden.

## Ausgabe

Zuerst der Text Folie für Folie, als nummerierte Liste, die der Nutzer in zehn
Sekunden lesen kann. Dann der **Begleittext**: Ein Karussell braucht 2-3 Zeilen
darüber, das ist der eigentliche Hook im Feed. Beides durch `/li-human`. Die
PDF erst bauen, wenn der Nutzer den Text freigegeben hat.

Nichts wird zu LinkedIn hochgeladen. Der Nutzer postet die PDF selbst.
