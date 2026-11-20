# flug-agent

Flugpreis-Agent für Safari & Adventure Tour: Streamlit-App, die mit Claude und Websuche die günstigsten Flüge sucht.

## Starten

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # oder als Streamlit-Secret, siehe unten
streamlit run app.py
```

## Sicherheit und Kosten

- **API-Key nur als Secret oder Umgebungsvariable.** In Streamlit Community Cloud unter
  *App → Settings → Secrets* `ANTHROPIC_API_KEY = "sk-ant-..."` eintragen. Ohne Betreiber-Key
  kann ein Besucher seinen eigenen Key eingeben; der gilt nur für seine Sitzung und wird
  nirgends gespeichert.
- **Nicht ohne Zugriffsschutz veröffentlichen.** Jede Suche läuft auf Kosten des hinterlegten
  Keys. App in Streamlit Cloud auf „privat“ stellen und Betrachter einzeln freigeben.
- **Ausgabenlimit setzen:** in der Anthropic Console unter *Limits*. Das ist die wirksamste
  Absicherung gegen Missbrauch.
- In der App begrenzt: max. 5 Suchen pro Sitzung, max. 5 Websuchen/Abrufe pro Suche,
  nur gültige 3-stellige Flughafen-Codes.
- Buchungslinks stammen aus Websuchen. Vor dem Buchen prüfen, ob die Seite echt ist.

## Tests

```bash
pip install -r requirements.txt
python -m unittest discover tests
```

Die Tests laufen ohne echten API-Key und ohne Netz (der Anthropic-Client wird nachgebaut).
