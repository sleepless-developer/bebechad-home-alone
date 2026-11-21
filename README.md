# Bebechad: Home Alone (GameMaker LTS 2026 + Web Preview)

A top-down roguelite built for **GameMaker LTS 2026** (`gm-project/BebechadHomeAlone.yyp`) with a synced 1:1 browser preview (`web-preview/index.html`) where housecat **Bebechad** is left home alone and defends a 4-room house from mouse hordes led by crowned **Rat Bosses**.

## Quick Start

### Option 1 — GameMaker LTS 2026
Open `gm-project/BebechadHomeAlone.yyp` in GameMaker LTS 2026 and press **F5 (Run)**.

### Option 2 — Instant Browser Preview
```bash
python -m http.server 8766 --directory web-preview
# Play:            http://127.0.0.1:8766/
# 10 UI Themes:    http://127.0.0.1:8766/ui-themes.html
```

## Features

- **4 Interconnected House Rooms (`1920×1280`)**:
  - **Гостиная (Living Room)**: staggered oak floorboards, tasseled rug, plush sofa with pillow/blanket, cyan-glowing TV console, cat scratching tree, bookshelf, corner plants, and 3-bowl pet feeding mat (`Миска Мяты`).
  - **Кухня (Kitchen)**: checkered tiles, sunlit window shafts, stove with simmering pot & sink, fridge with magnets, butcher-block island with Swiss cheese wheel, and mousetraps.
  - **Подвал (Basement)**: slate stone floor, puddles, floor drain grate, copper pipes with valves, crates, oak barrels, warm hanging bulb glow, and mossy brick walls with blinking rat burrows.
  - **Задний двор (Backyard)**: grass tiles with swaying interactive tall-grass clumps, curved stepping-stone path, garden pond with lily pads, shingled shed, raised Catnip planter, flowers, and lanterns.
- **Megabonk / Vampire Survivors Auto-Combat + Manual Skills**:
  - Auto-attacks: `Царапки` (claw arc), `Клубок-Рикошет` (bouncing yarn), `Рыбьи Кости` (piercing fan), `Мятная Бомба` (AoE catnip cloud).
  - Active skills: `[Shift]` Pounce Dash and `[F]` Gigachad Ultimate.
- **Catnip Upgrade Shop (`Кошачья Мята`)**:
  - Press `[B]` / `[Tab]` (or `[E]` near the Catnip Bowl) to spend collected Catnip on 8 scaling upgrades (`[1–8]`).
- **Rat Boss Fights with 2-Stage Timing Bar + QTE Combo Mini-Game**:
  - Bosses (*Сэр Сырогрыз*, *Крысиный Барон*, *Император Подвала*) raise a Cheese Shield at 66% and 33% HP (or press `[M]` to test), triggering a slow-mo Timing Bar (`Space`) → QTE Combo (`W/A/S/D`) duel for a massive **Гигачад-Удар**.
- **Dialogue & Monologue System**:
  - Opening monologue, first-visit room reactions, 3 unique Rat Boss banters, and rotating monologues using `bebechad.aseprite` (Gigachad), `catttt.aseprite` (outraged), and `rat1.aseprite` (Rat Boss) portraits.
- **Cozy Pixel-Wood & Parchment UI (Stardew Valley Theme #3)** locked as default across both GameMaker (`scr_ui_draw_wood_panel`) and Web Preview, plus an interactive 10-theme gallery (`web-preview/ui-themes.html`).

## Controls

| Key | Action |
|---|---|
| `WASD` / Arrows | Move across all 4 rooms |
| `Shift` | Cat Pounce Dash |
| `F` | Gigachad-Meow Ultimate |
| `B` / `Tab` / `E` (at bowl) | Open Catnip Upgrade Shop (`1–8` to buy) |
| `T` | Summon Rat Boss immediately |
| `M` | Trigger Boss Timing Bar + QTE Mini-Game |
| `Space` / Click | Advance Dialogue / Hit Timing Bar |
