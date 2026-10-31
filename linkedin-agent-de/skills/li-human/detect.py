#!/usr/bin/env python3
"""
detect.py - fünf Prüfungen, die bewerten, wie maschinell ein deutscher Entwurf wirkt.

Was das ist:   fünf lokale Heuristiken nach den Signalen, auf die öffentliche
KI-Detektoren achten: Satzrhythmus, Konkretheit, Floskeln, typografischer
Fingerabdruck und Stimme. Alles wird auf deinem Rechner aus dem Text selbst
berechnet. Nichts wird hochgeladen.

Was das NICHT ist:  GPTZero, Originality, Copyleaks, Winston oder Turnitin.
Es ruft keine dieser APIs auf und kann deren Urteil nicht versprechen.

Unterschiede zum englischen Original:
  - KONKRETHEIT zählt keine großgeschriebenen Wörter als Namen (im Deutschen
    ist jedes Substantiv groß), sondern Zahlen, €/%, Uhrzeiten, Abkürzungen
    wie IHK/DGUV, Paragrafen (§ 34a) und wörtliche Rede „…“.
  - STIMME misst Umgangssprache und Modalpartikeln (halt, eben, mal, ja,
    doch, echt, geht's ...) statt englischer Kurzformen.
  - FINGERABDRUCK bestraft deutsche Anführungszeichen „…“ und einzelne
    Gedankenstriche nicht - die sind korrekt. Englische Typografie (—, “”)
    und gehäufte Gedankenstriche schon.

Jede Prüfung liefert einen MENSCH-Wert von 0 bis 100. Höher ist besser.

Aufruf
  python3 detect.py entwurf.txt
  pbpaste | python3 detect.py -
  python3 detect.py entwurf.txt --json
  python3 detect.py vorher.txt nachher.txt      # zwei Fassungen vergleichen

Exit-Code: 0 = OK, 1 = PRÜFEN/AUFFÄLLIG, 2 = Eingabe zu kurz oder Fehler.
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from gemeinsam import (LEX_PATH, find_lexicon_hits, load_lexicon,  # noqa: E402
                       scan_structures, sentences, words)

UMGANGSSPRACHE = re.compile(
    r"\b(?:halt|eben|mal|ja|doch|eigentlich|echt|ziemlich|bisschen|bissl|"
    r"gibt's|geht's|gibts|gehts|hab|hab's|hat's|ist's|war's|nen|ne|grad|nix|"
    r"klar|okay|ok|naja|tja|krass|mega|bock|kram|zeug|ehrlich gesagt)\b",
    re.IGNORECASE)
PRONOMEN = re.compile(
    r"\b(?:ich|mich|mir|mein\w*|wir|uns|unser\w*|du|dich|dir|dein\w*|ihr|euch|euer|eure\w*)\b",
    re.IGNORECASE)
# Höfliche Anrede: case-sensitiv, damit "sie" (Plural) nicht mitzählt.
SIE_FORM = re.compile(r"\b(?:Sie|Ihnen|Ihr|Ihre|Ihren|Ihrem|Ihrer|Ihres)\b")
KONKRET = [
    re.compile(r"\d+(?:[.,]\d+)*"),                       # Zahlen: 3, 1.200, 15,5
    re.compile(r"[€$%]|\b(?:Euro|Prozent|Uhr|Minuten?|Stunden?|Std|Tagen?|Wochen?|"
               r"Monaten?|Monate|Jahren?|Jahre|Meter|km|Kilometer|qm|m²)\b"),  # Einheiten
    re.compile(r"\b(?:Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag|"
               r"Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|"
               r"November|Dezember)s?\b"),                 # Zeitanker
    re.compile(r"\b(?:zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|elf|zwölf|"
               r"zwanzig|dreißig|hundert|tausend)(?:mal|fach)?\b", re.IGNORECASE),  # Zahlwörter
    re.compile(r"\b[A-ZÄÖÜ]{2,6}s?\b"),                    # Abkürzungen: IHK, DGUV, BGB
    re.compile(r"§+\s?\d"),                                # Paragrafen
    re.compile(r"„[^“\n]{3,}“"),                           # wörtliche Rede
]


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """value auf 0-100 abbilden: `human` -> 100, `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def check_rhythmus(text):
    """Menschen variieren die Satzlänge stark. Modelle schreiben gleichmäßig."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "zu kurz zum Bewerten"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"Variation {cv:.2f} über {len(lens)} Sätze (Ziel: 0,55+)"


def check_konkretheit(text):
    """Zahlen, Kürzel, Paragrafen, Zitate. Floskeltext ist abstrakt."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "zu kurz zum Bewerten"
    hits = sum(len(p.findall(text)) for p in KONKRET)
    density = hits * 100 / len(w)
    score = scale(density, human=5.0, machine=0.5)
    return score, f"{hits} konkrete Marker, {density:.1f} pro 100 Wörter (Ziel: 4+)"


def check_floskeln(text, lex):
    w = words(text)
    if not w:
        return 50.0, "leer"
    hits = find_lexicon_hits(text, lex)
    total = sum(n for _, n in hits)
    density = total * 100 / len(w)
    score = scale(density, human=0.0, machine=3.0)
    detail = f"{total} Floskeln, {density:.1f} pro 100 Wörter"
    if hits:
        names = sorted(e["find"] for e, _ in hits)
        detail += " (" + ", ".join(names[:4]) + (", ..." if len(names) > 4 else "") + ")"
    return score, detail


def check_fingerabdruck(text, lex):
    """Zeichen, die eine (deutsche) Handytastatur nicht erzeugt."""
    unsichtbar = sum(1 for c in text if unicodedata.category(c) == "Cf")
    geviert = text.count("—")
    englisch = text.count("”")  # im Deutschen schließt „ mit “, nie mit ”
    striche = len(re.findall(r"\s–\s", text))
    zu_viele_striche = max(0, striche - lex.get("gedankenstrich_limit", 2))
    ellipse = text.count("…")
    hart = sum(text.count(c) for c in "   ")
    total = unsichtbar * 4 + geviert * 2 + englisch + zu_viele_striche + ellipse * 0.5 + hart
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{unsichtbar} unsichtbar, {geviert} Geviertstrich, {englisch} engl. Anführung, "
              f"{striche} Gedankenstrich, {ellipse} Ellipse, {hart} gesch. Leerzeichen")
    return score, detail


def check_stimme(text, lex):
    """Umgangssprache, Person, und die Satzmuster, zu denen Modelle greifen."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "zu kurz zum Bewerten"
    per100 = 100 / len(w)
    locker = len(UMGANGSSPRACHE.findall(text)) * per100
    sie = len(SIE_FORM.findall(text))
    person = (len(PRONOMEN.findall(text)) + sie) * per100
    # Ein Sie-Text darf sachlicher klingen: Umgangssprache zählt dann weniger,
    # direkte Ansprache mehr.
    formell = sie >= 2
    structs = [s for s in scan_structures(text, lex) if s["id"] != "gleichfoermig"]
    tells = sum(s["count"] for s in structs)
    names = [s["id"] for s in structs]
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*(?:[-*•✅👉]|\d+[.)])\s+(.+)$", text)]
    uniform = len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6
    w_locker, w_person = (0.10, 0.60) if formell else (0.35, 0.35)
    score = (scale(locker, human=2.5, machine=0.2) * w_locker
             + scale(person, human=7.0, machine=1.0) * w_person
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("gleiche-aufzaehlungen")
    detail = (f"{locker:.1f} Umgangssprache, {person:.1f} Pronomen (ich/du/wir) "
              f"pro 100 Wörter, {tells} Strukturmuster" + (", Sie-Form erkannt" if formell else ""))
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["RHYTHMUS", "KONKRETHEIT", "FLOSKELN", "FINGERABDRUCK", "STIMME"]


def run(text, lex):
    results = {
        "RHYTHMUS": check_rhythmus(text),
        "KONKRETHEIT": check_konkretheit(text),
        "FLOSKELN": check_floskeln(text, lex),
        "FINGERABDRUCK": check_fingerabdruck(text, lex),
        "STIMME": check_stimme(text, lex),
    }
    scores = [results[c][0] for c in CHECKS]
    # Die schwächste Prüfung zieht das Urteil runter: ein Detektor braucht nur ein Signal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "OK" if overall >= 70 and min(scores) >= 55 else (
        "PRÜFEN" if overall >= 50 else "AUFFÄLLIG")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "KI-ERKENNUNGS-PANEL" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 64), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<14} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<14} {detail}", file=out)
    print("-" * 64, file=out)
    print(f"  {'MENSCH-WERT':<14} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "OK":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Schwächstes Signal: {weakest}. Das zuerst beheben.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Bewertet, wie maschinell ein Entwurf wirkt.")
    ap.add_argument("input", nargs="?", default="-", help="Datei, oder - für stdin")
    ap.add_argument("compare", nargs="?", help="zweite Datei, für Vorher/Nachher")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX_PATH)
    args = ap.parse_args()

    lex = load_lexicon(args.lexicon)

    def read(p):
        if p == "-":
            return sys.stdin.read()
        try:
            with open(p, encoding="utf-8") as fh:
                return fh.read()
        except FileNotFoundError:
            sys.exit(f"Fehler: Datei nicht gefunden: {p}")
        except UnicodeDecodeError:
            sys.exit(f"Fehler: {p} ist nicht UTF-8. Als UTF-8 speichern und nochmal versuchen.")

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))
    for name, text in targets:
        if len(words(text)) < 10:
            print(f"Zu kurz zum Bewerten ({len(words(text))} Wörter in {name}). "
                  "Mindestens ein paar Sätze nötig.", file=sys.stderr)
            sys.exit(2)

    payload, rendered = [], []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        rendered.append((name, results, overall, verdict))
        payload.append({
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
    else:
        for name, results, overall, verdict in rendered:
            render(results, overall, verdict,
                   label=os.path.basename(name) if args.compare else None)
        if args.compare:
            a, b = payload
            delta = b["human_score"] - a["human_score"]
            print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
                  f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "OK" else 1)


if __name__ == "__main__":
    main()
