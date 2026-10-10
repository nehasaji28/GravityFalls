"""Makes the starter visuals for the data jam.
Run:  python make_visuals.py
Outputs: frame_onball.png, frame_offball.png, gravity_vs_ppg.png, gravity_scale.csv
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from wnba_court import draw_court

s = pd.read_csv("wnba_gravity_sample.csv", index_col=0)
p = pd.read_csv("wnba_player_lookup.csv").set_index("playerId")
g = s[s.hasGravity].copy()
g["name"] = g.playerId.map(p.Full_Name)
g["team"] = g.playerId.map(p.Team_Abbreviation)
g[["px", "py"]] = g.playerCentroid.str.strip("[]").str.split(expand=True).astype(float).values
g[["bx", "by"]] = g.ballCentroid.str.strip("[]").str.split(expand=True).iloc[:, :2].astype(float).values

bh = g[g.ballHandler].set_index("frameId").playerGravity


def pick(player, on_ball):
    d = g[(g["name"] == player) & (g.ballHandler == on_ball)].copy()
    if not on_ball:
        d["bhG"] = d.frameId.map(bh)
        d = d[d.bhG < 10]                       # ball handler is NOT the one pulling
    d = d[d.px.abs() > 20]                      # in the half court, not in transition
    return d.sort_values("playerGravity", ascending=False).iloc[0].frameId


def plot_frame(frame_id, star, title, fname):
    f = g[g.frameId == frame_id]
    fig, ax = plt.subplots(figsize=(9, 8))
    draw_court(ax, lw=1.2)
    side = np.sign(f.px.mean())
    ax.set_xlim(0, 49) if side > 0 else ax.set_xlim(-49, 0)
    for _, r in f.iterrows():
        val = r.playerGravity
        hot = val > 0
        if hot:  # glow rings: bigger and more of them = more pull
            for k in range(3):
                ax.add_patch(Circle((r.px, r.py), 1.5 + val / 100 * 7 * (k + 1) / 3,
                                    color="#e8590c", alpha=0.18, lw=0, zorder=3))
        ax.scatter(r.px, r.py, s=180, zorder=5,
                   c="#e8590c" if hot else "#5c7cfa", ec="black" if r.name_ == star else "white",
                   lw=2.5 if r.name_ == star else 1)
        lbl = f"{r.name_.split()[-1]}\n{val:+.0f}" + ("  (ball)" if r.ballHandler else "")
        ax.annotate(lbl, (r.px, r.py), xytext=(8, 8), textcoords="offset points",
                    fontsize=10, weight="bold" if r.name_ == star else "normal", zorder=6)
    ax.scatter(f.bx.iloc[0], f.by.iloc[0], s=60, c="#fab005", ec="black", zorder=7, marker="o")
    r0 = f.iloc[0]

    ax.set_title(f"{title}\nQ{r0.period}, {r0.gameClockTime} left  |  orange glow = Gravity (defense pulled in)",
                 fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    plt.tight_layout(); plt.savefig(fname, dpi=180); plt.close()
    print(fname, "frame", frame_id)
    print(f[["name", "team", "ballHandler", "playerGravity"]].to_string(index=False))


g = g.rename(columns={"name": "name_"})
g["name"] = g["name_"]
plot_frame(pick("Caitlin Clark", True), "Caitlin Clark",
           "ON-BALL Gravity: Caitlin Clark has the ball", "frame_onball.png")
plot_frame(pick("Caitlin Clark", False), "Caitlin Clark",
           "OFF-BALL Gravity: Clark doesn't have the ball, the defense still leans her way",
           "frame_offball.png")

# ---- Leaderboard: Gravity vs points ----
lb = pd.read_csv("wnba_gravity_season_leaderboards.csv")
lb["name"] = lb.First_Name + " " + lb.Last_name
lb = lb[lb.GP >= 15]
lb.sort_values("Gravity", ascending=False)[
    ["name", "Team_Abbreviation", "Gravity", "offBallPerimeter_Gravity", "offBallInterior_Gravity", "PPG", "GP"]
].round(1).to_csv("gravity_scale.csv", index=False)

fig, ax = plt.subplots(figsize=(10, 7))
ax.scatter(lb.PPG, lb.Gravity, c="#adb5bd", s=40)
fit = np.polyfit(lb.PPG, lb.Gravity, 1)
xs = np.linspace(lb.PPG.min(), lb.PPG.max(), 10)
ax.plot(xs, np.polyval(fit, xs), "--", c="#868e96", lw=1)
lb["resid"] = lb.Gravity - np.polyval(fit, lb.PPG)
lab = pd.concat([lb.nlargest(6, "Gravity"), lb.nlargest(4, "resid")]).drop_duplicates("name")
for _, r in lab.iterrows():
    ax.scatter(r.PPG, r.Gravity, c="#e8590c", s=60)
    ax.annotate(r["name"], (r.PPG, r.Gravity), xytext=(5, 4), textcoords="offset points", fontsize=9)
ax.axhline(0, c="black", lw=0.6)
ax.set_xlabel("Points per game"); ax.set_ylabel("Season Gravity (defensive pull)")
ax.set_title("Who pulls the defense? Above the dashed line = more pull than her points suggest")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig("gravity_vs_ppg.png", dpi=180); plt.close()
print(lab[["name", "Team_Abbreviation", "Gravity", "PPG", "resid"]].round(1).to_string(index=False))
