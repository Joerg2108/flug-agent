import os
import re

import anthropic
import streamlit as st

# Höchstzahl an Suchen pro Browser-Sitzung. Schützt vor versehentlichem
# Dauerklicken; gegen gezielten Missbrauch helfen nur Zugriffsschutz
# (App privat stellen) und ein Ausgabenlimit in der Anthropic Console.
MAX_SUCHEN_PRO_SITZUNG = 5
# Obergrenze für Web-Werkzeug-Aufrufe pro Suche (begrenzt die Kosten).
MAX_WEB_AUFRUFE = 5
IATA_RE = re.compile(r"[A-Z]{3}")

st.set_page_config(page_title="Safari & Adventure Tour — Flugsuche", page_icon="🦁", layout="wide")

col_logo, col_title = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=150)
    elif os.path.exists(os.path.expanduser("~/flug-agent/logo.png")):
        st.image(os.path.expanduser("~/flug-agent/logo.png"), width=150)
    else:
        st.markdown("## 🦁")
with col_title:
    st.title("✈️ Flugpreis-Agent")
    st.caption("Safari & Adventure Tour · Sucht Google Flights, Skyscanner, Kayak, Kiwi & Airlines")


def get_key():
    """API-Key des Betreibers: Streamlit-Secret oder Umgebungsvariable.

    Der Key wird nie aus einer Datei gelesen, die Besucher beschreiben können,
    und nie auf die Festplatte geschrieben.
    """
    try:
        k = st.secrets["ANTHROPIC_API_KEY"]
        if k:
            return str(k).strip()
    except (KeyError, FileNotFoundError):
        pass  # kein Secret hinterlegt -> Umgebungsvariable versuchen
    return os.environ.get("ANTHROPIC_API_KEY", "").strip()


key = get_key()
if not key.startswith("sk-ant-"):
    # Kein Betreiber-Key: Der Besucher nutzt seinen eigenen Key, aber NUR in
    # seiner eigenen Sitzung. Er wird nicht gespeichert und von keiner anderen
    # Sitzung gesehen.
    eingabe = st.text_input("🔑 Anthropic API Key (nur für diese Sitzung)",
                            type="password", placeholder="sk-ant-api03-...")
    key = eingabe.strip() if eingabe and eingabe.strip().startswith("sk-ant-") else ""
    if eingabe and not key:
        st.error("Das sieht nicht nach einem Anthropic API Key aus (sk-ant-...).")

# Eingaben
col1, col2, col3, col4 = st.columns(4)
with col1:
    fly_from = st.text_input("Von", value="BER", max_chars=3).strip().upper()
with col2:
    fly_to = st.text_input("Nach", value="MBA", max_chars=3).strip().upper()
with col3:
    dep_date = st.date_input("Abflug")
with col4:
    ret_date = st.date_input("Rückflug")

one_way = st.checkbox("Nur Hinflug")

st.session_state.setdefault("suchen", 0)
limit_erreicht = st.session_state["suchen"] >= MAX_SUCHEN_PRO_SITZUNG
if limit_erreicht:
    st.warning(f"Limit von {MAX_SUCHEN_PRO_SITZUNG} Suchen für diese Sitzung erreicht.")

if st.button("🔍 Suchen", type="primary", disabled=not key or limit_erreicht):
    # Zweite Prüfung direkt vor dem kostenpflichtigen Aufruf: Der Knopf wird
    # gezeichnet, bevor der Zähler steigt, darf also nicht die einzige Sperre sein.
    if not key or st.session_state["suchen"] >= MAX_SUCHEN_PRO_SITZUNG:
        st.stop()
    if not (IATA_RE.fullmatch(fly_from) and IATA_RE.fullmatch(fly_to)):
        st.error("Bitte 3-stellige Flughafen-Codes eingeben (z. B. BER, MBA).")
        st.stop()
    if not one_way and ret_date < dep_date:
        st.error("Der Rückflug liegt vor dem Abflug.")
        st.stop()

    st.session_state["suchen"] += 1
    trip = (f"Hin- und Rückflug (zurück: {ret_date:%Y-%m-%d})"
            if not one_way else "Einfacher Flug")
    prompt = f"""Suche die günstigsten Flüge:
- Von: {fly_from} → Nach: {fly_to}
- Abflug: {dep_date:%Y-%m-%d} | {trip}

Plattformen: Google Flights, Skyscanner, Kayak, Kiwi.com, Airlines direkt (KQ, TK, Condor, KLM).

Ausgabe als Markdown-Tabelle:
| Plattform | Preis | Airline | Route | Dauer | Gepäck | Link |

Dann: 🏆 GÜNSTIGSTER LEGITIMER TARIF mit Buchungslink.
⚠️ Virtual Interlining Warnung wenn relevant."""

    client = anthropic.Anthropic(api_key=key)
    output = st.empty()
    full = ""

    with client.messages.stream(
        model="claude-opus-4-8",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        tools=[
            {"type": "web_search_20260209", "name": "web_search", "max_uses": MAX_WEB_AUFRUFE},
            {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": MAX_WEB_AUFRUFE},
        ],
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            full += text
            output.markdown(full + "▌")
    # unsafe_allow_html bleibt bewusst aus: Die Ausgabe enthält Inhalte fremder Webseiten.
    output.markdown(full)
    st.caption("Links stammen aus Websuchen. Vor dem Buchen prüfen, ob die Seite echt ist.")
