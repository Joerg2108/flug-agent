---
name: li-inbox
description: >-
  Sortiert das LinkedIn-Postfach - Kontaktanfragen und Nachrichten in Leads,
  Recruiter, Kollegen und Spam - und entwirft die Antworten, die sich lohnen.
  Verwenden, wenn der Nutzer sagt "mein Postfach ist ein Chaos", "sortier meine
  Nachrichten", "soll ich darauf antworten", einen Stapel LinkedIn-Nachrichten
  einfügt, oder in Kontaktanfragen untergeht.
---

# li-inbox

Die meisten LinkedIn-Postfächer sind zu 80 % Rauschen, und der Preis dafür ist,
dass die wichtigen 20 % eine Woche liegen bleiben. Dieser Skill trennt sie und
schreibt nur, was sich lohnt.

## Eingabe

Der Nutzer fügt die Nachrichten ein. Screenshots gehen. Nicht in sein Konto
einloggen und das Postfach nicht mit einem Browser auslesen. Die Nachrichten
enthalten personenbezogene Daten Dritter: nur für diese Aufgabe verwenden,
nichts davon in Dateien speichern außer dem, was der Nutzer ausdrücklich will.

## In fünf Gruppen sortieren

| Gruppe | Signal | Aktion |
| --- | --- | --- |
| **LEAD** | beschreibt ein Problem, das der Nutzer löst, oder fragt nach Zusammenarbeit | heute antworten, vollständig |
| **RECRUITER** | eine Stelle, eine Firma, ein Gehaltsrahmen | antworten, wenn die Stelle echt ist, sonst eine Zeile |
| **KOLLEGE** | jemand aus dem gleichen Feld mit etwas zu sagen | diese Woche antworten, menschlich |
| **BITTE** | will Rat, Zeit, eine Vorstellung, einen Gefallen | antworten, wenn es wenig kostet und konkret ist, sonst sauber absagen |
| **SPAM** | Agentur-Pitch, Lead-Gen-Sequenz, Krypto, „kurze Frage“ ohne Frage | archivieren, keine Antwort |

Zuerst die Anzahl ausgeben. „3 Leads, 2 Recruiter, 41 Spam“ zu sehen, ist schon
der halbe Nutzen.

## Eine Sequenz erkennen

Automatisierte Ansprache hat eine Form: eine Einladung ohne Details, eine
Nachricht wenige Minuten nach der Annahme, „Kurze Frage“, „Mir ist aufgefallen,
dass Sie in der Branche {X} tätig sind“, ein Kalenderlink in Nachricht eins,
dann genau vier Tage später ein „Wollte nur nochmal nachhaken“. Wenn du das
siehst: SPAM, und sag, welches Merkmal es verraten hat. Der Nutzer schuldet
einem Skript keine Antwort.

## Antworten

- **LEAD**: die eigentliche Frage in der Nachricht beantworten, vollständig,
  kostenlos. Passt es, ist das Angebot ein Satz am Ende. Passt es nicht, das
  sagen und an eine sinnvolle Stelle verweisen. Beides ist ein gutes Ergebnis.
- **RECRUITER**: Ist die Stelle wirklich interessant, die drei Dinge fragen,
  die fehlen: Gehaltsrahmen, Ebene, und ob vor Ort oder remote. Im
  Sicherheitsbereich zusätzlich: Tarifbindung (BDSW-Tarif), Schichtmodell und
  ob § 34a bzw. Fachkraft vorausgesetzt wird. Ist sie nicht interessant, eine
  Zeile: Suche gerade nicht, empfehle gern weiter - und dann auch wirklich.
- **BITTE**: Kostet es unter zehn Minuten und ist konkret, machen. Ist es „kann
  ich dich mal kurz ausquetschen“, in einem freundlichen Satz absagen und die
  eine Antwort geben, die man im Gespräch gegeben hätte. Das ist die höfliche
  und gleichzeitig die nützlichere Variante.
- **ABSAGEN** sind kurz, freundlich und endgültig. Kein „Lass uns im dritten
  Quartal nochmal sprechen“, wenn es kein drittes Quartal gibt.

## Ausgabe

Nach Gruppen sortiert, Anzahlen zuerst, Entwürfe nur für die Gruppen, die
Antworten bekommen, jeder humanisiert. Dann die Sperre: Der Nutzer verschickt
sie selbst.

```
POSTFACH  ·  52 Einträge  ·  3 LEAD, 2 RECRUITER, 4 KOLLEGE, 2 BITTE, 41 SPAM

SPAM  (41) - archivieren. 38 sind dieselbe Sequenz: Einladung ohne Bezug,
"Kurze Frage" 4 Minuten nach der Annahme, Kalenderlink in Nachricht eins.
```
