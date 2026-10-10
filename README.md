# Gravity Falls 🏀

**Scoring isn't the same as scaring the defense.**
We measured how much each WNBA player pulls defenders toward her (her *Gravity*) and found that some of the league's most valuable players are hiding behind ordinary point totals.

>  **Live demo:** https://nehasaji28.github.io/GravityFalls/

---

## The insight

Points tell you who scores. Gravity tells you who the defense is afraid of. **They are not the same players.**

- Across 69 WNBA players (15+ games, 2026 season), points per game and Gravity are only moderately linked (**correlation 0.44**).
- **Breanna Stewart** scores 20.2 PPG but has **average** Gravity (0.0).
- **Marina Mabrey** scores 19.9 PPG and has the **highest** Gravity in the league (**+13.0**), far more than her scoring predicts.
- Only **3 players** reach the elite zone of +8 or more: Marina Mabrey, Sonia Citron and Rhyne Howard.

## What is Gravity?

Gravity measures how far defenders shift toward a player, compared with how far they'd shift for a typical player standing in the same spot.

| Score | What it means |
| --- | --- |
| **Positive** (e.g. +13.0) | Defenders crowd her and leave their own players, which opens shots for teammates. |
| **Zero** | Average pull for a player in that spot. |
| **Negative** (e.g. −7.1) | The defense relaxes. Her defender backs off and helpers stay home. |

Gravity works **off the ball** too. A great shooter can pull defenders away from a teammate who is driving to the basket, without touching the ball herself.

## Who it's for

- **Coaches and scouts** deciding who to play together and who to sign. Players above the trend line add value the box score can't see.
- **Fans** who want to understand who really makes a team better, not just who scores.

## How we found it

1. **Data:** WNBA player-tracking data, which records every player's position many times per second, and the season Gravity scores built from it.
2. **Filter:** kept players with at least **15 games played**, which leaves 69 players.
3. **Compare:** plotted each player's season Gravity against points per game and fit a straight trend line.
4. **Find the surprises:** looked for players far above or below the line, whose pull doesn't match their scoring.
5. **Visualize:** built court diagrams, a league-wide Gravity scale and a scoring-vs-pull scatter chart.

## The visualizations

| Scene | What it shows |
| --- | --- |
| 1 · On the ball | A shooter with the ball pulls four helpers toward her, leaving teammates open. |
| 2 · Off the ball | Her defender won't leave her, even without the ball, so a driving lane opens. |
| 3 · Below zero | The defense relaxes on a player it doesn't fear. |
| 4 · The scale | All 69 players placed on one Gravity scale. |
| 5 · Scoring vs pull | Gravity vs points per game, with the trend line. **This is the main finding.** |

> Scenes 1–3 are diagrams we drew to explain the idea. They are not tracked game positions. Scenes 4–5 use the real season data.

## Repository contents

| File | Purpose |
| --- | --- |
| `index.html` | Animated explainer: five scenes with play, pause and scene controls. |
| `make_visuals.py` | Builds the starter charts (on-ball and off-ball court frames, Gravity vs PPG) and exports `gravity_scale.csv`. |
| `wnba_court.py` | Draws a regulation WNBA court in matplotlib (94 × 50 ft, 22' 1.75" three-point arc). |
| `gravity_scale.csv` | Season Gravity, off-ball perimeter and interior Gravity, PPG and games played for 69 players. |

## Run it

**View the visuals:** open index.html in any browser. There's nothing to install, and it works offline.

**Rebuild the charts:**

```bash
pip install numpy pandas matplotlib
python make_visuals.py
```
**Draw a blank court:**

```bash
python wnba_court.py -o court.png
```

## Built with

Python (pandas, NumPy, matplotlib) · HTML, CSS and SVG with vanilla JavaScript · no frameworks

## Team

**Gravity Falls**

- Neha Mariya Saji
- Trinity Darbouze
- Eunice Kinmade
- Sifatun Noor

---

*Built for the WNBA Data Jam, 2026.*
