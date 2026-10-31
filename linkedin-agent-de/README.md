# LinkedIn-Agent auf Deutsch

Elf Claude-Skills, die einen LinkedIn-Account betreuen, komplett auf Deutsch.
Kostenlos, MIT-Lizenz, keine Anmeldung, kein API-Key, nichts zu verbinden.

Deutsche Fassung von [avi691/linkedin-agent-skill](https://github.com/avi691/linkedin-agent-skill)
(ursprünglich von Jake Schincariol). Nicht einfach übersetzt: Der Humanizer ist
für die deutsche Sprache umgebaut.

**Es wird nichts gepostet, bevor du ja sagst.** Die Skills schreiben. Du postest.

## Installation

In Claude Code, global für alle Projekte:

```bash
cp -r linkedin-agent-de/skills/li-* ~/.claude/skills/
mkdir -p ~/.claude/linkedin
cp linkedin-agent-de/templates/voice.md ~/.claude/linkedin/voice.md
```

Nur für ein Projekt: dieselben Ordner nach `.claude/skills/` im Projekt
kopieren.

Als Plugin, sobald der Ordner als eigenes GitHub-Repo liegt:

```
/plugin marketplace add <dein-github-name>/linkedin-agent-de
/plugin install linkedin-agent-de
```

> Hast du das englische Original schon installiert? Erst die alten
> `~/.claude/skills/li-*` löschen. Die Skills heißen gleich und würden sich
> sonst überschreiben.

Danach zehn Minuten in `~/.claude/linkedin/voice.md` stecken, oder drei eigene
Posts in Claude einfügen und sagen: „Schreib mir daraus meine voice.md“. Jeder
Skill liest diese Datei.

## Die elf

| Befehl | was er macht |
| --- | --- |
| `/li-post` | Eine Idee wird ein Post. Drei Hooks aus [21 Formeln](skills/li-post/hooks.json), ein Entwurf, humanisiert. |
| `/li-comment` | Kommentare unter fremden Posts. Neun Typen, nie „Toller Beitrag!“. |
| `/li-reply` | Antworten unter deinen Posts, sortiert in Lead / Substanz / Kollege / Support / Rauschen. |
| `/li-profile` | Bewertet dein Profil mit [12 Kriterien](skills/li-profile/rubric.json) und bis zu 100 Punkten, schreibt es um. |
| `/li-plan` | Die Woche: was, wann, und mit welchen 10 Leuten du interagierst. |
| `/li-human` | Der deutsche Humanizer. Zwei Skripte, die wirklich laufen. |
| `/li-carousel` | Dokument-Posts: Text pro Folie, Titelblatt, PDF. |
| `/li-repurpose` | Ein Video, Newsletter oder Transkript wird eine Woche Posts. |
| `/li-dm` | Einladung mit 200 Zeichen, erste Nachricht, zwei Nachfassungen. |
| `/li-inbox` | Postfach sortieren und die Antworten schreiben, die sich lohnen. |
| `/li-audit` | Rückblick auf deine Posts nach Interaktionsrate, nicht Impressionen. |

## Was der deutsche Humanizer anders macht

Das englische Original ist für deutsche Texte praktisch unbrauchbar: Wörter mit
Umlauten wurden zerhackt, jedes großgeschriebene Substantiv galt als Name, und
die Floskel-Liste kannte nur englische Begriffe. Hier ist umgebaut worden:

| Thema | Original | Deutsche Fassung |
| --- | --- | --- |
| Wörter zählen | `[A-Za-z]` - „für“ wird „f“ + „r“ | Umlaute und ß zählen |
| Sätze trennen | jeder Punkt beendet einen Satz | z. B., bzw., ca., Nr., „am 3. März“ trennen nicht |
| Floskeln | 113 englische | ~120 deutsche: Buzzwords, Denglisch, übersetzte KI-Phrasen |
| Flexion | - | „nahtlosen“ wird „reibungslosen“, nicht „reibungslos“ |
| Grammatik | ersetzt blind | Ersatz nur, wo er sicher passt, sonst nur markieren |
| Satzanfang | „Zweifellos ist das gut“ wird zu „Ist das gut“ | wird markiert statt gelöscht (Verbzweitstellung) |
| Geviertstrich — | wird Komma | wird deutscher Gedankenstrich ` – ` (oder Komma mit `--striche komma`) |
| Anführungszeichen | alles wird gerade | englische “…” werden deutsche „…“, deutsche bleiben |
| Konkretheit | großgeschriebene Wörter = Namen | Zahlen, €, %, Uhrzeiten, IHK/DGUV, § 34a, wörtliche Rede |
| Stimme | englische Kurzformen (don't) | Modalpartikeln und Umgangssprache (halt, eben, mal, echt, geht's) |
| Strukturmuster | „It's not just X“ | „Nicht nur X, sondern auch Y“, „Spoiler:“, „Kennst du das?“, „Ich freue mich, mitteilen zu dürfen“ ... |

```bash
cd skills/li-human
python3 humanize.py beispiele/schlecht.txt --report -o /tmp/sauber.txt
python3 detect.py beispiele/schlecht.txt /tmp/sauber.txt
python3 detect.py beispiele/gut.txt
```

Ergebnis mit den mitgelieferten (erfundenen) Beispielen:

```
schlecht.txt   MENSCH-WERT  20,3  AUFFÄLLIG
nach humanize  MENSCH-WERT  27,3  AUFFÄLLIG   (+7,0, die markierten Stellen sind noch nicht umgeschrieben)
gut.txt        MENSCH-WERT  88,4  OK
```

Den Rest bis OK macht ein Mensch: Das Skript markiert die Satzmuster absichtlich
nur, statt sie mit einer Regex zu verhunzen.

**Tests:** `python3 -m unittest discover tests` (19 Tests, keine Abhängigkeiten).

## Das Kleingedruckte, ehrlich

**Diese Skills posten nicht auf LinkedIn, und das sollen sie auch nicht.**
Automatisches Posten, Scraping und Nachrichten-Sequenzen verstoßen gegen die
[LinkedIn-Nutzervereinbarung](https://www.linkedin.com/legal/user-agreement)
und führen zu Kontoeinschränkungen. Jeder Skill endet mit einem kopierfertigen
Block, und du fügst ihn ein.

**Die fünf Prüfungen sind lokale Heuristiken, keine Detektor-APIs.** Sie laufen
nur auf deinem Rechner. Sie sind nicht GPTZero, Originality oder Turnitin und
können deren Urteil nicht versprechen. Niemand kann dir ehrlich „unerkennbar“
verkaufen.

**Hier wird nichts erfunden.** Keine ausgedachten Zahlen, Kunden oder Ergebnisse
unter deinem Namen. Fehlt eine Zahl, steht `{{deine Zahl}}` im Entwurf.

**Datenschutz und Verschwiegenheit.** Keine Namen von Auftraggebern, Kollegen
oder Mietern ohne Freigabe, keine Details aus vertraulichen Einsätzen. Die
Skills weisen darauf hin, die Verantwortung bleibt bei dir.

## Dateien

```
skills/li-post/hooks.json        21 Hook-Formeln: Vorlage, Beispiel, Einsatz, Falle
skills/li-human/slop.json        das Lexikon: ~120 Floskeln, 17 unsichtbare Zeichenklassen, 14 Strukturmuster
skills/li-human/gemeinsam.py     gemeinsame Textfunktionen (Wörter, Sätze, Abkürzungen, Flexion)
skills/li-human/humanize.py      die drei Bereinigungsdurchgänge
skills/li-human/detect.py        die fünf Prüfungen
skills/li-human/beispiele/       ein schlechter und ein guter Beispieltext (erfunden)
skills/li-profile/rubric.json    die 100-Punkte-Bewertung fürs Profil
templates/voice.md               dein Stimmprofil. Zuerst ausfüllen.
tests/test_humanizer.py          Tests für den Humanizer
```

## Lizenz

MIT. Ursprünglich von Jake Schincariol ([opusjake.ai](https://opusjake.ai)),
geteilt von Avi Grondin, deutsche Fassung von Jörg Noack. Siehe `LICENSE`.
