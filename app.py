import streamlit as st
import anthropic
import os

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

# API Key
def get_key():
    try:                                          # Streamlit Cloud secrets
        k = st.secrets["ANTHROPIC_API_KEY"]
        if k: return k.strip()
    except: pass
    k = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if k: return k
    f = os.path.expanduser("~/.anthropic_key")   # lokale Datei
    if os.path.exists(f): return open(f).read().strip()
    return ""

key = get_key()
if not key or not key.startswith("sk-ant-"):
    key = st.text_input("🔑 Anthropic API Key", type="password", placeholder="sk-ant-api03-...")
    if key:
        open(os.path.expanduser("~/.anthropic_key"), "w").write(key)
        os.chmod(os.path.expanduser("~/.anthropic_key"), 0o600)
        st.success("✓ Gespeichert")

# Eingaben
col1, col2, col3, col4 = st.columns(4)
with col1:
    fly_from = st.text_input("Von", value="BER").upper()
with col2:
    fly_to = st.text_input("Nach", value="MBA").upper()
with col3:
    dep_date = st.date_input("Abflug").strftime("%Y-%m-%d")
with col4:
    ret_date = st.date_input("Rückflug").strftime("%Y-%m-%d")

one_way = st.checkbox("Nur Hinflug")

if st.button("🔍 Suchen", type="primary", disabled=not key):
    trip = f"Hin- und Rückflug (zurück: {ret_date})" if not one_way else "Einfacher Flug"
    prompt = f"""Suche die günstigsten Flüge:
- Von: {fly_from} → Nach: {fly_to}
- Abflug: {dep_date} | {trip}

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
            {"type": "web_search_20260209", "name": "web_search"},
            {"type": "web_fetch_20260209", "name": "web_fetch"},
        ],
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            full += text
            output.markdown(full + "▌")
    output.markdown(full)
