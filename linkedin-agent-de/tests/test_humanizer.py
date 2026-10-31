"""Tests für die deutsche Fassung des Humanizers.  Aufruf:  python3 -m unittest discover tests"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "..", "skills", "li-human")
sys.path.insert(0, LIB)

import detect  # noqa: E402
import humanize  # noqa: E402
from gemeinsam import load_lexicon, sentences, words  # noqa: E402

LEX = load_lexicon()


def clean(text, **kw):
    return humanize.humanize(text, LEX, **kw)[0].strip()


def beispiel(name):
    with open(os.path.join(LIB, "beispiele", name), encoding="utf-8") as fh:
        return fh.read()


class Grundlagen(unittest.TestCase):
    def test_umlaute_sind_woerter(self):
        self.assertEqual(words("Für größere Übergaben weiß ich Bescheid."),
                         ["Für", "größere", "Übergaben", "weiß", "ich", "Bescheid"])

    def test_abkuerzungen_trennen_keine_saetze(self):
        s = sentences("Das gilt z. B. für Nachtdienste ab ca. 22 Uhr im Objekt. "
                      "Am 3. März war es anders als sonst. Danach lief alles wieder normal.")
        self.assertEqual(len(s), 3)


class Typografie(unittest.TestCase):
    def test_geviertstrich_wird_gedankenstrich(self):
        self.assertEqual(clean("Sicherheit—das ist Arbeit."), "Sicherheit – das ist Arbeit.")

    def test_geviertstrich_als_komma(self):
        self.assertEqual(clean("Sicherheit — das ist Arbeit.", striche="komma"),
                         "Sicherheit, das ist Arbeit.")

    def test_deutsche_anfuehrung_bleibt(self):
        t = "Er sagte: „Das passt schon.“ – und ging."
        self.assertEqual(clean(t), t)

    def test_englische_anfuehrung_wird_deutsch(self):
        self.assertEqual(clean("Er sagte “Nein” und ging."), "Er sagte „Nein“ und ging.")

    def test_bis_strich_bleibt(self):
        self.assertEqual(clean("Dienst von 6–14 Uhr."), "Dienst von 6–14 Uhr.")

    def test_unsichtbare_zeichen_weg(self):
        self.assertEqual(clean("Schicht​plan fertig"), "Schichtplan fertig")


class Floskeln(unittest.TestCase):
    def test_endung_bleibt_erhalten(self):
        self.assertEqual(clean("Wir sorgen für eine nahtlose Übergabe und nahtlosen Ablauf."),
                         "Wir sorgen für eine reibungslose Übergabe und reibungslosen Ablauf.")

    def test_grossschreibung_am_satzanfang(self):
        self.assertEqual(clean("Innovative Konzepte helfen."), "Neue Konzepte helfen.")

    def test_kein_treffer_in_laengeren_woertern(self):
        self.assertEqual(clean("Die Nahtlosigkeit ist ein Wort."), "Die Nahtlosigkeit ist ein Wort.")

    def test_loeschen_mitten_im_satz(self):
        self.assertEqual(clean("Das ist zweifellos wichtig."), "Das ist wichtig.")

    def test_kein_loeschen_im_vorfeld(self):
        t = "Zweifellos ist das wichtig."
        text, report = humanize.humanize(t, LEX)
        self.assertEqual(text.strip(), t)
        self.assertTrue(any(f["find"] == "zweifellos" for f in report["flagged_lexical"]))

    def test_nur_markieren_aendert_nichts(self):
        t = "Das war eine spannende Woche im Objektschutz."
        text, report = humanize.humanize(t, LEX)
        self.assertEqual(text.strip(), t)
        self.assertTrue(report["flagged_lexical"])

    def test_phrase_ueber_zeilenumbruch(self):
        self.assertEqual(clean("Das ist von entscheidender\nBedeutung."), "Das ist wichtig.")

    def test_urls_bleiben_unberuehrt(self):
        t = "Mehr unter https://example.com/nahtlos-innovativ dazu."
        self.assertEqual(clean(t), t)


class Erkennung(unittest.TestCase):
    def test_schlechter_text_faellt_auf(self):
        _, overall, verdict = detect.run(beispiel("schlecht.txt"), LEX)
        self.assertEqual(verdict, "AUFFÄLLIG")
        self.assertLess(overall, 50)

    def test_guter_text_besteht(self):
        results, overall, verdict = detect.run(beispiel("gut.txt"), LEX)
        self.assertEqual(verdict, "OK", f"{overall:.1f} {results}")

    def test_humanize_verbessert(self):
        roh = beispiel("schlecht.txt")
        _, vorher, _ = detect.run(roh, LEX)
        _, nachher, _ = detect.run(clean(roh), LEX)
        self.assertGreater(nachher, vorher)

    def test_typischer_ki_post_faellt_auf(self):
        results, _, verdict = detect.run(beispiel("ki-typisch.txt"), LEX)
        self.assertEqual(verdict, "AUFFÄLLIG")
        self.assertIn("kein-x-sondern", results["STIMME"][1])
        self.assertIn("engagement-koeder", results["STIMME"][1])

    def test_sie_form_wird_nicht_bestraft(self):
        results, overall, _ = detect.run(beispiel("sie-form.txt"), LEX)
        self.assertGreaterEqual(results["STIMME"][0], 80)
        self.assertIn("Sie-Form", results["STIMME"][1])
        self.assertGreater(overall, 65)

    def test_koeder_mit_emoji_am_ende(self):
        flags = humanize.scan_structures("Wie seht ihr das? 👇", LEX)
        self.assertTrue(any(f["id"] == "engagement-koeder" for f in flags))


class Kommandozeile(unittest.TestCase):
    def _run(self, script, stdin, *args):
        import subprocess
        return subprocess.run([sys.executable, "-I", os.path.join(LIB, script), "-", *args],
                              input=stdin, capture_output=True, text=True)

    def test_leere_eingabe(self):
        self.assertNotEqual(self._run("humanize.py", "  ").returncode, 0)

    def test_zu_kurz_exit_2(self):
        self.assertEqual(self._run("detect.py", "Hallo Welt.").returncode, 2)

    def test_json_ausgabe(self):
        import json
        out = json.loads(self._run("humanize.py", "Ein nahtloser Ablauf.", "--json").stdout)
        self.assertEqual(out["text"].strip(), "Ein reibungsloser Ablauf.")


if __name__ == "__main__":
    unittest.main()
