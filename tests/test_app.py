"""Sicherheits-Regressionstests für app.py.

Läuft ohne echten API-Key und ohne Netz: anthropic.Anthropic wird durch eine
Attrappe ersetzt, die nur mitschreibt, mit welchem Key und welchen Werkzeugen
sie aufgerufen wurde.

Aufruf:  python -m pytest tests/   (oder python -m unittest discover tests)
"""
import os
import tempfile
import unittest
from contextlib import contextmanager
from unittest import mock

from streamlit.testing.v1 import AppTest

APP = os.path.join(os.path.dirname(__file__), "..", "app.py")


class FakeStream:
    text_stream = iter(["| Plattform | Preis |"])

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class FakeClient:
    calls = []

    def __init__(self, api_key):
        self.api_key = api_key
        self.messages = self

    def stream(self, **kwargs):
        FakeClient.calls.append({"api_key": self.api_key, **kwargs})
        return FakeStream()


@contextmanager
def umgebung(env_key=None):
    """Leeres HOME, kein Secret, optional ein Betreiber-Key in der Umgebung."""
    FakeClient.calls = []
    with tempfile.TemporaryDirectory() as home:
        env = {"HOME": home}
        if env_key:
            env["ANTHROPIC_API_KEY"] = env_key
        with mock.patch.dict(os.environ, env, clear=False), \
                mock.patch("anthropic.Anthropic", FakeClient):
            if not env_key:
                os.environ.pop("ANTHROPIC_API_KEY", None)
            yield home


def neue_sitzung():
    at = AppTest.from_file(APP, default_timeout=30)
    at.run()
    return at


def suchen_knopf(at):
    return next(b for b in at.button if "Suchen" in b.label)


class KeyIsolation(unittest.TestCase):
    """Audit-Fall 1: Ein Besucher-Key darf nie bei anderen Sitzungen landen."""

    def test_besucher_key_bleibt_in_eigener_sitzung(self):
        with umgebung() as home:
            a = neue_sitzung()
            a.text_input[0].input("sk-ant-dummy-A").run()
            suchen_knopf(a).click().run()
            self.assertEqual(FakeClient.calls[-1]["api_key"], "sk-ant-dummy-A")

            b = neue_sitzung()
            self.assertTrue(suchen_knopf(b).disabled, "Sitzung B darf keinen Key haben")
            self.assertIn("API Key", b.text_input[0].label)
            self.assertFalse(os.path.exists(os.path.join(home, ".anthropic_key")),
                             "Key darf nicht auf die Platte geschrieben werden")

    def test_alte_key_datei_wird_ignoriert(self):
        with umgebung() as home:
            with open(os.path.join(home, ".anthropic_key"), "w") as fh:
                fh.write("sk-ant-fremder-key")
            at = neue_sitzung()
            self.assertTrue(suchen_knopf(at).disabled)

    def test_ungueltiger_key_wird_abgelehnt(self):
        with umgebung():
            at = neue_sitzung()
            at.text_input[0].input("kein-key").run()
            self.assertTrue(suchen_knopf(at).disabled)
            self.assertTrue(at.error)

    def test_betreiber_key_aus_umgebung(self):
        with umgebung(env_key="sk-ant-dummy-betreiber"):
            at = neue_sitzung()
            self.assertNotIn("API Key", " ".join(t.label for t in at.text_input))
            suchen_knopf(at).click().run()
            self.assertEqual(FakeClient.calls[-1]["api_key"], "sk-ant-dummy-betreiber")


class Kostenbremse(unittest.TestCase):
    """Audit-Fall 2: Kosten pro Sitzung und pro Suche begrenzen."""

    def test_sitzungslimit(self):
        with umgebung(env_key="sk-ant-dummy"):
            at = neue_sitzung()
            for _ in range(7):
                if suchen_knopf(at).disabled:
                    break
                suchen_knopf(at).click().run()
            self.assertEqual(len(FakeClient.calls), 5, "mehr als 5 Suchen pro Sitzung")
            self.assertTrue(suchen_knopf(at).disabled)
            self.assertTrue(at.warning)

    def test_limit_greift_auch_ohne_neu_zeichnen(self):
        # Simuliert einen Klick, der beim Stand 5 ankommt (z. B. veraltete UI).
        with umgebung(env_key="sk-ant-dummy"):
            at = neue_sitzung()
            at.session_state["suchen"] = 5
            suchen_knopf(at).click().run()
            self.assertEqual(FakeClient.calls, [])

    def test_web_werkzeuge_haben_max_uses(self):
        with umgebung(env_key="sk-ant-dummy"):
            at = neue_sitzung()
            suchen_knopf(at).click().run()
            for tool in FakeClient.calls[-1]["tools"]:
                self.assertIn("max_uses", tool)
                self.assertLessEqual(tool["max_uses"], 5)

    def test_ungueltige_flughafen_codes_kosten_nichts(self):
        with umgebung(env_key="sk-ant-dummy"):
            at = neue_sitzung()
            at.text_input[0].input("B1").run()
            suchen_knopf(at).click().run()
            self.assertEqual(FakeClient.calls, [])
            self.assertTrue(at.error)
            self.assertEqual(at.session_state["suchen"], 0)

    def test_eingabefelder_begrenzt(self):
        with umgebung(env_key="sk-ant-dummy"):
            at = neue_sitzung()
            self.assertEqual([t.max_chars for t in at.text_input], [3, 3])


class Devcontainer(unittest.TestCase):
    """Audit-Fall 3: CORS/XSRF-Schutz darf nicht abgeschaltet werden."""

    def test_keine_schutz_abschaltung(self):
        path = os.path.join(os.path.dirname(__file__), "..", ".devcontainer", "devcontainer.json")
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        self.assertNotIn("enableCORS false", text)
        self.assertNotIn("enableXsrfProtection false", text)


if __name__ == "__main__":
    unittest.main()
