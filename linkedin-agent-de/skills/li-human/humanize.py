#!/usr/bin/env python3
"""
humanize.py - entfernt den Maschinen-Fingerabdruck aus einem deutschen Entwurf.

Drei Durchgänge, in dieser Reihenfolge:

  1. UNSICHTBAR   Zeichen, die keine Tastatur erzeugt: Zero-Width-Zeichen,
                  Word Joiner, weiche Trennstriche, BOMs, Unicode-Tag-Zeichen,
                  geschützte und schmale Leerzeichen. Sie überleben Copy-Paste
                  und sind das mechanischste Merkmal generierter Texte.
  2. TYPOGRAFIE   Deutsch-korrekt statt englisch:
                    Geviertstrich —            -> Gedankenstrich " – "
                                                  (oder Komma mit --striche komma)
                    englische Anführung "x"    -> deutsche „x“
                    ’ ′                        -> '
                    …                          -> ...
                    • · am Zeilenanfang        -> -
                  Deutsche Anführungszeichen „…“, Gedankenstriche " – " und
                  Bis-Striche (5–10) bleiben stehen: das ist korrekter Satz,
                  kein KI-Merkmal.
  3. FLOSKELN     ersetzt Einträge aus slop.json durch schlichte Wörter, mit
                  passender Endung und Groß-/Kleinschreibung, URLs bleiben
                  unberührt. Einträge ohne Ersetzung werden nur MARKIERT.

Strukturmuster ("nicht nur X, sondern auch Y", Dreierketten, Hashtag-Wände,
"Was denkt ihr?") werden GEMELDET, nie automatisch umgeschrieben - einen Satz
umzubauen braucht Urteilsvermögen.

Aufruf
  python3 humanize.py entwurf.txt
  python3 humanize.py entwurf.txt --report
  pbpaste | python3 humanize.py - --report
  python3 humanize.py entwurf.txt --json
  python3 humanize.py entwurf.txt -o sauber.txt
  python3 humanize.py entwurf.txt --striche komma
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from gemeinsam import (DEFAULT_HINWEIS, LEX_PATH, build_pattern, is_flag_only,  # noqa: E402
                       lexicon_entries, load_lexicon, scan_structures)

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")


def _cp(spec):
    """'U+200B' -> 0x200B;  'U+E0000-U+E007F' -> (start, ende)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": "gelöscht" if entry["action"] == "delete" else "-> Leerzeichen"})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Jedes übrige Cf-Zeichen (Format) ist per Definition unsichtbar.
    # \x00 ist Cc, nicht Cf - die URL-Platzhalter bleiben also heil.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "sonstige unsichtbare Formatzeichen", "count": len(stray),
                     "action": "gelöscht"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, striche="behalten"):
    hits = []

    def hit(name, n, to):
        if n:
            hits.append({"name": name, "count": n, "to": to})

    # Geviertstrich: im Deutschen praktisch nie korrekt -> Gedankenstrich.
    n = text.count("—")
    if n:
        ziel = " – " if striche == "behalten" else ", "
        text = re.sub(r"[ \t]*—[ \t]*", ziel, text)
        hit("— Geviertstrich (englischer Satz)", n, ziel.strip() or ziel)

    # Gedankenstriche nur auf Wunsch in Kommas umwandeln. Bis-Striche (5–10) nie.
    if striche == "komma":
        n = len(re.findall(r"[ \t]+–[ \t]+", text))
        text = re.sub(r"[ \t]+–[ \t]+", ", ", text)
        hit("– Gedankenstrich", n, ",")

    # Englische Anführung “…” -> deutsche „…“
    pattern = re.compile(r"“([^“”„\n]*)”")
    n = len(pattern.findall(text))
    text = pattern.sub(r"„\1“", text)
    hit("“…” englische Anführungszeichen", n, "„…“")
    # Übrig gebliebene einzelne ” (z. B. ”so”) ebenfalls angleichen.
    n = text.count("”")
    text = text.replace("”", "“")
    hit("” rechtes englisches Anführungszeichen", n, "“")

    # Apostrophe vereinheitlichen. ‘ nur, wenn keine deutschen ‚…‘ im Text sind.
    n = text.count("’") + text.count("′")
    text = text.replace("’", "'").replace("′", "'")
    hit("’ typografischer Apostroph", n, "'")
    if "‚" not in text:
        n = text.count("‘")
        text = text.replace("‘", "'")
        hit("‘ einfaches Anführungszeichen", n, "'")

    n = text.count("…")
    text = text.replace("…", "...")
    hit("… Auslassungszeichen", n, "...")

    n = len(re.findall(r"(?m)^[ \t]*[•·][ \t]*", text))
    text = re.sub(r"(?m)^([ \t]*)[•·][ \t]*", r"\1- ", text)
    hit("• Aufzählungspunkt am Zeilenanfang", n, "-")

    # Ein eingefügtes Komma vor vorhandener Satzzeichen liest sich falsch.
    text = re.sub(r",[ \t]*([,.;:!?])", r"\1", text)
    text = re.sub(r",[ \t]*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def _at_sentence_start(text, pos):
    before = text[:pos].rstrip(" \t")
    return not before or before[-1] in ".!?\n:"


def pass_lexical(text, lex):
    """Floskeln ersetzen bzw. markieren. Längste zuerst, damit Phrasen gewinnen."""
    replaced, flagged = [], []
    for entry in lexicon_entries(lex):
        pattern = build_pattern(entry)

        if is_flag_only(entry):
            n = len(pattern.findall(text))
            if n:
                flagged.append({"find": entry["find"], "count": n, "family": entry["family"],
                                "hinweis": entry.get("hinweis", DEFAULT_HINWEIS)})
            continue

        repl = entry["replace"]
        if repl == "":
            # Löschen inkl. Folgekomma. Steht das Wort im Vorfeld (Satzanfang),
            # wird NICHT gelöscht: "Zweifellos ist das gut" -> "Ist das gut"
            # wäre ein Fragesatz (Verbzweitstellung). Dort nur markieren.
            pattern = re.compile(pattern.pattern + r"[ \t]*,?[ \t]*", re.IGNORECASE)
        found, vorfeld = [], []

        def sub(m, repl=repl, found=found, vorfeld=vorfeld):
            if repl == "":
                if _at_sentence_start(m.string, m.start()):
                    vorfeld.append(1)
                    return m.group(0)
                found.append(1)
                return ""
            found.append(1)
            endung = m.groupdict().get("endung") or ""
            return _match_case(m.group(0), repl + endung)

        text = pattern.sub(sub, text)
        if found:
            replaced.append({"find": entry["find"], "replace": repl or "(gelöscht)",
                             "count": len(found), "family": entry["family"]})
        if vorfeld:
            flagged.append({"find": entry["find"], "count": len(vorfeld), "family": entry["family"],
                            "hinweis": "Steht am Satzanfang - Löschen würde die Wortstellung brechen. "
                                       "Satz umbauen: 'Zweifellos ist X wichtig' -> 'X ist wichtig'."})

    # Aufräumen nach Löschungen.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*([,.;:])[ \t]*", "", text)
    text = re.sub(r"[ \t]+([,.;:!?])", r"\1", text)
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, replaced, flagged


def humanize(text, lex, striche="behalten"):
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, striche)
    text, lexi, markiert = pass_lexical(text, lex)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "flagged_lexical": markiert,
        "structures": scan_structures(text, lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for k in ("invisible", "typographic", "lexical") for h in report[k])
    n_flags = len(report["structures"]) + len(report["flagged_lexical"])

    head("HUMANIZE-BERICHT")
    print(f"{total} Maschinen-Artefakte entfernt, {n_flags} Stellen zum Umschreiben markiert",
          file=out)

    if report["invisible"]:
        head("1. UNSICHTBARE ZEICHEN")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  {h['action']}", file=out)
    if report["typographic"]:
        head("2. TYPOGRAFIE")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. FLOSKELN ERSETZT")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["flagged_lexical"]:
        head("4. FLOSKELN MARKIERT  (nicht ersetzt - selbst umformulieren)")
        for h in report["flagged_lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}   [{h['family']}]\n        {h['hinweis']}", file=out)
    if report["structures"]:
        head("5. STRUKTURMUSTER  (nicht automatisch geändert - selbst umschreiben)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("SAUBER")
        print("  Nichts zu entfernen.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Entfernt den Maschinen-Fingerabdruck aus einem Entwurf.")
    ap.add_argument("input", nargs="?", default="-", help="Datei, oder - für stdin")
    ap.add_argument("-o", "--out", help="bereinigten Text hierhin schreiben statt nach stdout")
    ap.add_argument("--report", action="store_true", help="Änderungen auf stderr ausgeben")
    ap.add_argument("--json", action="store_true", help="{text, report} als JSON ausgeben")
    ap.add_argument("--lexicon", default=LEX_PATH, help="Pfad zu slop.json")
    ap.add_argument("--striche", choices=["behalten", "komma"], default="behalten",
                    help="Gedankenstriche ' – ' stehen lassen (Standard) oder in Kommas umwandeln")
    args = ap.parse_args()

    if args.input == "-":
        raw = sys.stdin.read()
    else:
        with open(args.input, encoding="utf-8") as fh:
            raw = fh.read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex, args.striche)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"geschrieben: {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
