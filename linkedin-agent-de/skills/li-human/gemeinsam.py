"""
gemeinsam.py - Hilfsfunktionen, die humanize.py und detect.py teilen.

Deutsche Besonderheiten, die das englische Original nicht kannte:
  - Wörter mit Umlauten und ß zählen als Wörter.
  - Abkürzungen (z. B., bzw., ca., Nr. ...) und Ordinalzahlen ("am 3. März")
    zerschneiden keine Sätze.
  - Floskeln mit Flexion: "nahtlos" erwischt auch "nahtlose", "nahtlosen" ...
    und die Ersetzung bekommt dieselbe Endung ("reibungslosen").
  - Einträge mit "replace": null werden nur markiert, nicht ersetzt. Im
    Deutschen bricht eine blinde Ersetzung sonst schnell die Grammatik
    (Genus, trennbare Verben).
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
LEX_PATH = os.path.join(HERE, "slop.json")

# Buchstaben inkl. Umlaute/ß, optional mit Apostroph ("geht's").
WORD_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")

ABKUERZUNGEN = [
    "z. B.", "z.B.", "d. h.", "d.h.", "u. a.", "u.a.", "o. Ä.", "o.Ä.",
    "u. U.", "i. d. R.", "z. T.", "bzw.", "ca.", "etc.", "usw.", "vgl.",
    "Nr.", "Dr.", "Prof.", "inkl.", "exkl.", "ggf.", "evtl.", "bspw.",
    "zzgl.", "Std.", "Min.", "Mio.", "Mrd.", "Tsd.", "Abs.", "Art.", "Str.",
    "Tel.", "max.", "mind.", "sog.", "Hr.", "Fr.", "Jh.", "gem.", "lt.",
]
_MONATE = ("Januar|Februar|März|April|Mai|Juni|Juli|August|September|"
           "Oktober|November|Dezember|Jan|Feb|Mär|Apr|Jun|Jul|Aug|Sep|Okt|Nov|Dez")
ORDINAL_RE = re.compile(r"(?<=\d)\.(?=\s?(?:" + _MONATE + r"|[a-zäöüß]))")
_MASKE = ""

# Endungen, die ein Adjektiv/Partizip im Deutschen bekommen kann.
ADJ_ENDUNG = r"(?:ere|eren|erer|eres|erem|e|en|er|es|em)?"

DEFAULT_HINWEIS = "Umformulieren: sag konkret, was du meinst."


def load_lexicon(path=LEX_PATH):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def mask_abbrev(text):
    """Punkte in Abkürzungen und Ordinalzahlen unsichtbar machen (nur für die
    Satzzählung - der Text, der ausgegeben wird, bleibt unberührt)."""
    for abk in sorted(ABKUERZUNGEN, key=len, reverse=True):
        text = text.replace(abk, abk.replace(".", _MASKE))
    return ORDINAL_RE.sub(_MASKE, text)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(mask_abbrev(text)) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def sentence_cv(text):
    """Variationskoeffizient der Satzlängen. None bei weniger als 4 Sätzen."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return None, len(lens)
    mean = sum(lens) / len(lens)
    var = sum((n - mean) ** 2 for n in lens) / len(lens)
    return ((var ** 0.5) / mean if mean else 0.0), len(lens)


def is_flag_only(entry):
    return entry.get("replace") is None


def build_pattern(entry):
    """Regex für einen Lexikon-Eintrag.

    - Leerzeichen in Phrasen matchen auch Zeilenumbrüche/mehrere Leerzeichen.
    - "stem": true -> Endungen werden mitgenommen (Gruppe "endung").
    - Wortgrenzen nur dort, wo der Eintrag mit einem Wortzeichen beginnt/endet.
    """
    find = entry["find"]
    core = r"\s+".join(re.escape(t) for t in find.split())
    if entry.get("stem"):
        endung = r"\w*" if is_flag_only(entry) else ADJ_ENDUNG
        core += r"(?P<endung>" + endung + r")"
    pre = r"\b" if find[0].isalnum() else ""
    post = r"\b" if (find[-1].isalnum() or entry.get("stem")) else ""
    return re.compile(pre + core + post, re.IGNORECASE)


def lexicon_entries(lex):
    """Alle Einträge, längste zuerst - damit Phrasen vor Einzelwörtern greifen."""
    return sorted(lex["phrases"] + lex["words"], key=lambda e: len(e["find"]), reverse=True)


def find_lexicon_hits(text, lex):
    """Zählt Floskeln ohne Doppelzählung (gefundene Stellen werden maskiert).
    Rückgabe: Liste von (eintrag, anzahl)."""
    hits = []
    for entry in lexicon_entries(lex):
        pattern = build_pattern(entry)
        n = len(pattern.findall(text))
        if n:
            hits.append((entry, n))
            text = pattern.sub(lambda m: _MASKE * len(m.group(0)), text)
    return hits


def scan_structures(text, lex):
    """Strukturmuster, die gemeldet, aber nie automatisch umgeschrieben werden."""
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"])
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"id": s["id"], "name": s["name"], "count": len(found), "fix": s["fix"]})

    # Gedankenstrich-Häufung: im Deutschen korrekt, aber KI-Texte übertreiben es.
    striche = len(re.findall(r"\s–\s", text))
    limit = lex.get("gedankenstrich_limit", 2)
    if striche > limit:
        flags.append({
            "id": "gedankenstriche",
            "name": f"Viele Gedankenstriche ({striche}x ' – ')",
            "count": striche,
            "fix": "Max. 1-2 pro Post. Ersetz den Rest durch Punkt, Komma oder Doppelpunkt.",
        })

    cv, n = sentence_cv(text)
    if cv is not None and cv < 0.35:
        flags.append({
            "id": "gleichfoermig",
            "name": f"Gleich lange Sätze (Variation {cv:.2f})",
            "count": n,
            "fix": "Teil einen Satz in zwei. Lass einen anderen richtig lang laufen. Maschinen schreiben gleichmäßig.",
        })
    return flags
