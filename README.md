# Habit-Tracker (PWA)

Einzelne `index.html`, Daten im `localStorage`, installierbar auf iOS, offline nutzbar.

## Dateien
- `index.html` – App, iOS-Meta-Tags, SW-Registrierung, Backup (JSON)
- `manifest.webmanifest` – relative `start_url`/`scope` (funktioniert unter `/repo-name/`)
- `sw.js` – Cache-First App-Shell. **Bei jeder Änderung `CACHE_VERSION` erhöhen.**
- `icons/` – 180/192/512 px, erzeugt mit `python3 tools/make_icons.py`

## Deployment auf GitHub Pages
1. Branch nach `main` mergen (oder Pages auf diesen Branch stellen).
2. Repo → **Settings → Pages** → *Build and deployment*: Source **Deploy from a branch**, Branch `main`, Ordner `/ (root)` → Save.
3. Nach ca. 1 Minute erreichbar unter `https://<user>.github.io/<repo-name>/` (HTTPS automatisch).
4. Updates: pushen, `CACHE_VERSION` in `sw.js` erhöhen. Installierte App holt die neue Version beim nächsten Start (ggf. einmal schließen und neu öffnen).

Lokal testen: `python3 -m http.server 8000` → `http://localhost:8000` (Service Worker laufen auf `localhost`, nicht auf `file://`).

## iOS-Testcheckliste
- [ ] Seite in **Safari** (nicht Chrome-iOS) per HTTPS-URL öffnen, lädt ohne Fehler
- [ ] Teilen → **Zum Home-Bildschirm**: Icon (Haken-Logo) und Name „Habits“ stimmen
- [ ] Start vom Home-Bildschirm: öffnet ohne Safari-Leiste (standalone), Inhalt nicht unter Notch/Home-Indikator
- [ ] Gewohnheit anlegen, Tage abhaken, Streak aktualisiert sich
- [ ] App komplett schließen (App-Switcher), neu öffnen: Daten noch da
- [ ] **Flugmodus** an, App neu starten: lädt und funktioniert
- [ ] Backup exportieren (Share-Sheet → „In Dateien sichern“), Gewohnheit löschen, Backup importieren: Daten wieder da
- [ ] Privater Safari-Tab: roter Hinweis „Speichern nicht möglich“ erscheint, App läuft trotzdem
- [ ] Update: `CACHE_VERSION` erhöhen, pushen, App 2× neu starten: neue Version aktiv

## Bekannte iOS-Eigenheiten
- Safari-Tab und Home-Bildschirm-App haben **getrennten** localStorage – Daten per Backup übertragen.
- iOS kann Website-Daten nach ca. 7 Tagen ohne Nutzung löschen (im Safari-Tab); installierte Home-Bildschirm-Apps sind davon ausgenommen. Regelmäßige Backups bleiben sinnvoll.
