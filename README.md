# 🥪 OVER-SCOPED SANDWICH SIMULATOR

> A chaotic, over-engineered sandwich shop management game built in Python.

![Version](https://img.shields.io/badge/version-v0.0.1--alpha-orange)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎮 About

**Over-Scoped Sandwich Simulator** is a feature-packed sandwich shop simulator where you build sandwiches, satisfy increasingly impatient customers, manage your shop across multiple locations, and uncover secret recipes — all wrapped in a juicy PyQt6 UI.

The name is self-aware: this game has *way* more features than a sandwich game has any right to have.

---

## ✨ Features

- 🧱 **Visual Sandwich Builder** — Stack ingredients in real time with animated rendering
- 👥 **Customer Orders** — Fulfill orders before patience runs out
- 🏪 **Upgrade Shop** — Invest your earnings into shop upgrades
- 📅 **Day Progression System** — Manage your shop day by day with escalating difficulty
- 📖 **Branching Story Events** — Make choices that shape your sandwich empire
- ⚡ **Market Events** — Dynamic events that shake up ingredient prices and demand
- 🌍 **Multiple Locations** — Unlock and operate across different venues
- 🔎 **Secret Recipes** — Discover hidden combinations for bonus rewards
- 🏆 **Achievements** — Unlock milestones as you grow your business
- 🎁 **Collectibles System** — Collect rare items dropped during service
- 💾 **Save Slots with Difficulty** — Multiple save files, each with its own challenge level
- 🎵 **Music & SFX** — Full soundtrack and sound effect system
- ☣️ **Environmental Hazards** — Random chaos to keep you on your toes

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| UI Framework | PyQt6 |
| Packaging | PyInstaller |
| Installer | Inno Setup |
| Data | JSON (save data, collectibles) |

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install PyQt6
```

### Run from source

```bash
python "OVER-SCOPED SANDWICH SIMULATOR.py"
```

### Install via Installer

Download the latest installer from the [Releases](https://github.com/Dyvorn/Overscoped_Sandwich_Simulator/releases) page and run the setup executable.

---

## 📁 Project Structure

├── OVER-SCOPED SANDWICH SIMULATOR.py # Main game file
├── collectibles.json # Collectible item definitions
├── save_data.json # Save file data
├── storry.md # In-game story/lore notes
├── images/ # Game sprites and backgrounds
├── sounds/ # Music and SFX files
├── build/ # PyInstaller build output
├── dist/ # Distributable build
├── installer/ # Inno Setup installer files
└── build.py # Build automation script





---

## 📦 Building

To package the game into a standalone executable:

```bash
python build.py
```

This uses PyInstaller with the included `.spec` file. The Inno Setup script (`.iss`) can then be used to generate a Windows installer.

---

## 🗺️ Roadmap

Check the [Milestones](https://github.com/Dyvorn/Overscoped_Sandwich_Simulator/milestones) and [Issues](https://github.com/Dyvorn/Overscoped_Sandwich_Simulator/issues) for planned features and known bugs.

---

## 👤 Author

**Dyvorn** — [@Dyvorn](https://github.com/Dyvorn)

---

## 📄 License

This project is licensed under the MIT License.

