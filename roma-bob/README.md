# ROMA + BOB

A neon-themed settings dashboard for Free Fire and Free Fire MAX. It is a standalone web UI with a desktop Tkinter version; it does not modify game files, automate gameplay, or change aim/recoil.

## Web app

Open `index.html` directly in a modern browser, or serve this folder locally:

```powershell
python -m http.server 8000
```

Then visit <http://127.0.0.1:8000/>.

The web app stores preferences in the browser's `localStorage`. On iPhone, use Safari's **Share → Add to Home Screen** to install it as a web app. A browser page cannot create a system overlay above other apps, so the floating R button is available only while this web app is open. Safari may block game URL schemes; when that happens, launch the game manually.

## Desktop app

Requires Python 3 with Tkinter available:

```powershell
python ffmax_python_app.py
```

The legacy desktop version is also included as `roma_bob_aim_pro.py`.

## Features

- Neon blue settings UI with live crosshair preview, colors, size, and opacity controls.
- Six selectable sensitivity profiles and individual sensitivity sliders.
- Floating R control inside the web page, with drag, position freeze, and button settings.
- Settings persistence in localStorage (web) and a JSON file in the user's home directory (desktop).
- Free Fire / Free Fire MAX launch buttons report platform limitations rather than claiming success.

All sensitivity and headshot values are local profile settings only; they do not affect gameplay.

## Project files

- `index.html`, `styles.css`, `app.js` — browser app.
- `ffmax_python_app.py` — desktop Tkinter app.
- `roma_bob_aim_pro.py` — earlier desktop version.
