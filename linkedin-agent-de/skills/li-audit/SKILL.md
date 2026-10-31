---
name: li-audit
description: >-
  Rückblick auf das, was der Nutzer schon veröffentlicht hat - welche Posts
  wirklich funktioniert haben, warum, und was er lassen sollte. Verwenden, wenn
  der Nutzer seine LinkedIn-Statistik oder alte Posts einfügt und fragt "was
  funktioniert", "warum ist der gefloppt", "lies meine Statistik", "analysier
  meine Posts", oder wissen will, worauf er setzen soll.
---

# li-audit

Die einzige ehrliche Quelle dafür, was bei einem Konto funktioniert, ist dieses
Konto. Jede Regel in jedem LinkedIn-Ratgeber, auch die in diesem Paket, ist
eine Annahme. Die letzten 30 Posts des Nutzers sind der Beweis.

## Eingabe

Nach dem fragen, was der Nutzer hat:

- Den Export der Beitragsstatistik (LinkedIn: Analysen → Inhalte →
  Exportieren). Excel/CSV.
- Oder einen Screenshot pro Post mit Impressionen, Reaktionen, Kommentaren,
  Reposts.
- Oder nur die Posts mit ihren Reaktionszahlen, das reicht für einen ersten
  Durchgang.

Außerdem `~/.claude/linkedin/log.md` lesen, falls vorhanden, dort steht, welche
Hook-Formel jeder Post benutzt hat.

## Was wirklich gemessen wird

Reine Impressionen sind die unbrauchbarste Zahl auf der Seite, weil sie vor
allem davon abhängen, wie viele Leute dem Nutzer schon folgen. Stattdessen das
hier berechnen und den Rechenweg zeigen:

| Kennzahl | Berechnung | was sie verrät |
| --- | --- | --- |
| **Interaktionsrate** | (Reaktionen + Kommentare + Reposts) / Impressionen | ob der Post seine Reichweite verdient hat |
| **Kommentarquote** | Kommentare / Reaktionen | ob er etwas ausgelöst hat oder nur ein Nicken bekam |
| **Reichweiten-Faktor** | Impressionen / Follower | ob er über das bestehende Publikum hinausging |
| **Speicher-/Sende-Rate** | wenn verfügbar | der stärkste einzelne Hinweis auf künftige Reichweite |

Nach Interaktionsrate und Reichweiten-Faktor sortieren, nicht nach
Impressionen. Ein Post mit 900 Impressionen und 40 Kommentaren hat den mit
12.000 Impressionen und 6 Kommentaren geschlagen.

Beim CSV-Export auf deutsche Zahlenformate achten (`1.200` = tausendzweihundert,
`3,5 %`). Mit Python: `pd.read_csv(..., sep=";", thousands=".", decimal=",")`.

## Dann das Muster finden

Die Top 5 und die Flop 5 nebeneinander, und schauen, was sie wirklich trennt.
Auch zu einem Schluss bereit sein, der dem Nutzer nicht gefällt:

- Hook-Formel. Welche Nummern aus `hooks.json` sind in den Top 5?
- Format. Text, Dokument, Bild, Video.
- Länge.
- Thema.
- Tag und Uhrzeit: **zuletzt** prüfen, und nur, wenn die anderen vier nichts
  zeigen. Fast nie die Ursache, und genau da wollen die Leute sie haben.
- Kommentare in der ersten Stunde. Posts, bei denen der Nutzer innerhalb einer
  Stunde geantwortet hat, gegen die anderen.

Den Befund als Aussage mit Beleg formulieren und sagen, wie sicher er ist. Mit
30 Posts sieht man ein Muster, mit 6 nicht, und dann sag genau das, statt eins
zu erfinden.

## Ausgabe

```
AUDIT  ·  31 Posts  ·  12. Juni - 5. September

TOP 5 NACH INTERAKTIONSRATE
  8,1 %  #3  Fehler       "1.800 € hat mich ein fehlendes Protokoll gekostet"   1.940 Imp.
  6,4 %  #20 Ausstieg     "Ich habe meinem größten Auftraggeber gekündigt"      2.210 Imp.
  ...

FLOP 5
  0,4 %  #5  Liste        "7 Tools, die jeder Sicherheitsdienst braucht"       11.400 Imp.
  ...

WAS DIE DATEN SAGEN
1. Posts, in denen du derjenige warst, der schlecht aussah: im Schnitt 6,2 %
   gegen 1,1 % für alles andere. n=6. Dein stärkstes Signal, und es ist
   eindeutig.
2. Tool-Listen bekommen Impressionen und sonst nichts. Hohe Reichweite, keine
   Kommentare, keine Anfragen. Drei deiner Flop 5.
3. Der Wochentag zeigt nichts. Dienstag und Freitag liegen im Rauschen. Hör
   auf, das zu optimieren.

LASSEN:   Tool-Listen.
MEHR VON: Posts mit einem Preis, den du bezahlt hast, und einer Zahl.
```

Dann die Schlüsse an `/li-plan` weitergeben, damit der Plan für nächste Woche
auf den eigenen Daten des Nutzers steht und nicht auf Standardregeln.
