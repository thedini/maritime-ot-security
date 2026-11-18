#!/usr/bin/env python3
"""make_figures.py - Regenerates the course diagrams (CC BY-SA 4.0, drawn for this course)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

OUT = os.path.dirname(os.path.abspath(__file__))
NAVY = "#1E3A5F"; ORANGE = "#C0561B"; GREY = "#555555"

def step(ax, bits, hi, lo, color, label):
    xs, ys = [], []
    for i, b in enumerate(bits):
        v = hi if b else lo
        xs += [i, i + 1]; ys += [v, v]
    ax.step(xs, ys, where="post", color=color, lw=2, label=label)

def can_physical():
    bits = [1, 0, 0, 1, 0, 1, 1, 0]            # 0 = dominant, 1 = recessive
    fig, (a, b) = plt.subplots(2, 1, figsize=(7.5, 4.8), sharex=True,
                               gridspec_kw={"height_ratios": [3, 2]})
    ch = [2.5 if x else 3.5 for x in bits]
    cl = [2.5 if x else 1.5 for x in bits]
    for i, x in enumerate(bits):
        a.axvspan(i, i + 1, color="#e8eef5" if x else "#f7e6dc", alpha=0.7, lw=0)
        a.text(i + 0.5, 4.2, "1" if x else "0", ha="center", fontsize=12, color=GREY)
    step(a, bits, 2.5, 3.5, NAVY, "CAN_H")
    step(a, bits, 2.5, 1.5, ORANGE, "CAN_L")
    a.set_ylim(1, 4.6); a.set_ylabel("Bus voltage (V)")
    a.set_title("CAN physical layer: differential signaling (nominal levels)")
    a.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=True)
    diff = [0 if x else 2 for x in bits]
    b.step(range(len(bits) + 1), diff + [diff[-1]], where="post", color="#222222", lw=2)
    b.set_ylim(-0.4, 2.6); b.set_ylabel("CAN_H - CAN_L (V)")
    b.set_xlabel("Bit time   (shaded orange = dominant 0, blue = recessive 1)")
    b.set_yticks([0, 2]); b.set_xlim(0, len(bits))
    for ax in (a, b):
        ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(f"{OUT}/can_physical.png", dpi=200); plt.close(fig)

def can_arbitration():
    A = [0, 1, 0, 0, 1, 1, 0, 1]; B = [0, 1, 0, 1, 0, 0, 1, 1]
    lose = next(i for i, (a, b) in enumerate(zip(A, B)) if a != b and b == 1)
    Bsent = B[:lose + 1] + [1] * (len(B) - lose - 1)      # B stops driving: recessive
    bus = [a & b for a, b in zip(A, Bsent)]
    fig, axs = plt.subplots(3, 1, figsize=(7.5, 5.4), sharex=True)
    rows = [("Node A  (lower ID, wins)", A, NAVY), ("Node B  (higher ID, loses)", Bsent, ORANGE),
            ("Bus level  (dominant 0 overrides 1)", bus, "#222222")]
    for ax, (name, bits, c) in zip(axs, rows):
        ax.step(range(len(bits) + 1), bits + [bits[-1]], where="post", color=c, lw=2)
        ax.set_ylim(-0.3, 1.5); ax.set_yticks([0, 1]); ax.set_ylabel(name, fontsize=8, rotation=0,
                                                                     ha="right", va="center")
        ax.grid(alpha=0.25)
    axs[1].axvspan(lose + 1, len(B), color="#dddddd", alpha=0.6, lw=0)
    axs[1].text((lose + 1 + len(B)) / 2, 0.5, "B has stopped transmitting", ha="center",
                color=GREY, fontsize=8)
    axs[1].axvline(lose + 0.5, color="red", ls="--", lw=1.3)
    axs[1].annotate("B sends 1 but reads 0:\nB loses arbitration and stops",
                    xy=(lose + 0.5, 0.5), xytext=(lose + 0.7, 1.18), color="red", fontsize=9,
                    arrowprops=dict(arrowstyle="->", color="red"))
    axs[0].set_title("CAN arbitration: lower identifier wins")
    axs[2].set_xlabel("Identifier bits, most significant first (A wins and keeps transmitting)")
    fig.tight_layout(); fig.savefig(f"{OUT}/can_arbitration.png", dpi=200); plt.close(fig)

def defense_in_depth():
    layers = ["Perimeter\nsatellite / shore links", "Network\nsegmentation, firewalls",
              "System\nhardening, patching", "Application\nsecure protocols",
              "Data\nintegrity, encryption", "Detection\nanomaly detection"]
    shades = ["#dfe7f1", "#c5d3e6", "#a9bdd9", "#8aa5cb", "#6b8cbb", ORANGE]
    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    radii = [6.0, 5.0, 4.0, 3.0, 2.2, 1.3]
    for i, (name, c, r) in enumerate(zip(layers, shades, radii)):
        ax.add_patch(Circle((0, 0), r, facecolor=c, edgecolor="white", lw=2))
        if i < len(layers) - 1:
            ax.text(0, r - 0.5, name, ha="center", va="center", fontsize=8.5,
                    color="white" if i >= 4 else "#102030")
        else:
            ax.text(0, 0, name, ha="center", va="center", fontsize=7.5, color="white",
                    fontweight="bold")
    ax.set_xlim(-6.2, 6.2); ax.set_ylim(-6.2, 6.2); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Defense in depth for a vessel network (outside in)", fontsize=11)
    fig.tight_layout(); fig.savefig(f"{OUT}/defense_in_depth.png", dpi=200); plt.close(fig)

if __name__ == "__main__":
    can_physical(); can_arbitration(); defense_in_depth()
