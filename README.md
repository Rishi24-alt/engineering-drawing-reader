<div align="center">

<img src="https://img.shields.io/badge/Draft_AI-v1.0-f97316?style=for-the-badge&labelColor=0b0b0b" alt="version"/>
<img src="https://img.shields.io/badge/SolidWorks-2020+-f97316?style=for-the-badge&labelColor=0b0b0b" alt="solidworks"/>
<img src="https://img.shields.io/badge/.NET-4.8-f97316?style=for-the-badge&labelColor=0b0b0b" alt="dotnet"/>
<img src="https://img.shields.io/badge/GPT--4o-Vision-f97316?style=for-the-badge&labelColor=0b0b0b" alt="gpt4o"/>
<img src="https://img.shields.io/badge/Windows-Only-f97316?style=for-the-badge&labelColor=0b0b0b" alt="windows"/>

<br/><br/>

```
██████╗ ██████╗  █████╗ ███████╗████████╗     █████╗ ██╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝╚══██╔══╝    ██╔══██╗██║
██║  ██║██████╔╝███████║█████╗     ██║       ███████║██║
██║  ██║██╔══██╗██╔══██║██╔══╝     ██║       ██╔══██║██║
██████╔╝██║  ██║██║  ██║██║        ██║       ██║  ██║██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝       ╚═╝  ╚═╝╚═╝
```

### **AI-Powered SolidWorks Sketch Analyzer**
*Press `Ctrl+Shift+A` inside any sketch. Get instant feedback on what's missing.*

<br/>

[![Download](https://img.shields.io/badge/⬇_Download_Add--in_v1.0-f97316?style=for-the-badge&labelColor=0b0b0b)](https://github.com/Rishi24-alt/DraftAI-Addin/releases/download/v1/DraftAI_Addin_V1.0.zip)
[![Website](https://img.shields.io/badge/🌐_draftai.cloud-ffffff?style=for-the-badge&labelColor=0b0b0b)](https://draftai.cloud)
[![App](https://img.shields.io/badge/🚀_Launch_App-ffffff?style=for-the-badge&labelColor=0b0b0b)](https://draftaii.streamlit.app)

</div>

---

## What is Draft AI?

Draft AI is a **SolidWorks add-in** that tells you exactly what's missing in your sketch — instantly.

No more hunting through blue lines trying to figure out why your sketch is underdefined. No more failed extrudes because you missed one relation. Just press **Ctrl+Shift+A** and Draft AI tells you what to fix.

```
You press Ctrl+Shift+A
         ↓
Draft AI reads your sketch via SolidWorks API
         ↓
Toast notification appears in SolidWorks
         ↓
"⚠️ Sketch is UNDERDEFINED — 3 of 5 entities need constraints.
 • Lines: 4
 • Arcs / Circles: 1

 3 entities shown in BLUE need dimensions or constraints.
 Tip: Add dimensions, fix points to origin, or add geometric relations."
```

---

## Features

| Feature | Description |
|---------|-------------|
| ⚡ **Ctrl+Shift+A Hotkey** | Global hotkey works even when SolidWorks has focus |
| 🔍 **Sketch Analyzer** | Reads segment types, underdefined count directly from SW API |
| ✅ **Fully Defined Detection** | Instantly detects when sketch is fully defined — no false alerts |
| 🔔 **Toast Notifications** | Hover-to-pause, auto-dismiss, scrollable for long messages |
| 🌐 **HTTP API** | Local server on port 7432 — integrate with your own tools |
| 📐 **3D → 2D Export** | Export STEP files to front/top/side/isometric views via SolidWorks |
| 🚫 **Zero API Key Required** | Powered by Draft AI cloud proxy — no OpenAI key needed |

---

## Installation

### Requirements
- Windows 10 / 11
- SolidWorks 2020 or later
- .NET Framework 4.8

### Steps

**1.** Download the latest release

```
https://github.com/Rishi24-alt/DraftAI-Addin/releases/latest
```

**2.** Extract `DraftAI_Addin_V1.0.zip` to any **permanent** folder

**3.** Right-click `install.bat` → **Run as Administrator**

```batch
# install.bat does this automatically:
RegAsm.exe DraftAI_Addin.dll /codebase
# Creates DraftAI_Output folder
# Writes proxy URL to openai_key.txt
```

**4.** Open SolidWorks → **Tools → Add-Ins** → check **Draft AI** → OK

**5.** Look for the toast notification:
```
Draft AI · Add-in loaded · Press Ctrl+Shift+A to analyze sketch
```

---

## Usage

```
1. Open any Part file in SolidWorks
2. Double-click a sketch face to enter Edit Sketch mode
3. Press Ctrl+Shift+A
4. Read the toast notification
```

### Example Output

**Underdefined sketch:**
```
⚠️ Sketch is UNDERDEFINED — 2 of 4 entities need constraints.

• Lines: 3
• Arcs / Circles: 1

2 entities shown in BLUE need dimensions or constraints.
Tip: Add dimensions, fix points to origin, or add geometric relations.
```

**Fully defined sketch:**
```
✅ Sketch is fully defined! No missing constraints or dimensions.
```

---

## HTTP API

The add-in runs a local HTTP server on `localhost:7432`. You can call it from any tool.

```bash
# Check if add-in is running
GET http://localhost:7432/ping

# Trigger sketch analysis
POST http://localhost:7432/sketch_analyze

# Start/stop auto-watcher
POST http://localhost:7432/sketch_watch
{"enable": true}

# Export STEP file views
POST http://localhost:7432/export
{"file_path": "C:/path/to/file.step", "output_dir": "C:/output"}
```

---

## Project Structure

```
DraftAI_Addin/
├── DraftAIAddin.cs        # Main add-in — all logic lives here
├── DraftAI_Addin.csproj   # Project file
├── install.bat            # One-click installer
├── uninstall.bat          # One-click uninstaller
└── Newtonsoft.Json.dll    # JSON dependency
```

---

## How It Works

```
SolidWorks (your sketch)
        ↓
DraftAIAddin.cs reads ISketch via SW API
  - GetSketchSegments()
  - ISketchSegment.Status
  - ISketchSegment.ConstructionGeometry
        ↓
Counts underdefined entities (Status != 0)
        ↓
Builds human-readable report
        ↓
ShowToast() — WinForms overlay in SolidWorks
```

---

## Roadmap

- [x] Ctrl+Shift+A hotkey
- [x] Segment type detection (lines, arcs, circles, splines)
- [x] Fully defined detection
- [x] Toast notification with hover-to-pause
- [x] HTTP API on port 7432
- [x] 3D → 2D view export
- [ ] Gemini + Claude vision pipeline for smarter analysis
- [ ] Per-entity constraint suggestions
- [ ] Auto-fix suggestions
- [ ] SolidWorks Marketplace listing

---

## Web App

Draft AI also has a full web application for engineering drawing analysis:

🌐 **[draftaii.streamlit.app](https://draftaii.streamlit.app)**

Features include dimension detection, GD&T analysis, standards compliance (ASME Y14.5 / ISO GPS / BS 8888), BOM generation, cost estimation, manufacturability scoring and more.

---

## Built By

**Rishi Raj** — Mechanical Engineering Student

> *Built because I was tired of hunting through blue lines every time a sketch was underdefined.*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Rishi_Raj-0077b5?style=flat-square&logo=linkedin)](https://linkedin.com/in/rishi24-alt)
[![Website](https://img.shields.io/badge/Website-draftai.cloud-f97316?style=flat-square)](https://draftai.cloud)

---

<div align="center">

**Made with ♥ · Powered by SolidWorks API + GPT-4o Vision**

<sub>If this saved you time, consider giving it a ⭐</sub>

</div>
