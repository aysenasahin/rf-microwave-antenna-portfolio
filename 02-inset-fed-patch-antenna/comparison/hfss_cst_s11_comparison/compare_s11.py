#!/usr/bin/env python3
"""Compare two one-port Touchstone exports at their original sample grids.

Requires Python 3, NumPy and Matplotlib. Run from this folder:
    python compare_s11.py
"""

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator


@dataclass
class Network:
    label: str
    path: Path
    freq: np.ndarray  # GHz
    s11: np.ndarray
    zref: float
    encoding: str

    @property
    def db(self):
        return 20 * np.log10(np.abs(self.s11))


def read_s1p(path, label):
    """Read standard one-port RI, MA or DB data, including inline comments."""
    option = None
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = line.split("!", 1)[0].strip()
        if not line:
            continue
        if line.startswith("#"):
            option = line[1:].upper().split()
            continue
        values = line.replace("D", "E").replace("d", "e").split()
        if len(values) != 3:
            raise ValueError(f"{path.name}:{number}: expected one-port, three-column data")
        rows.append([float(value) for value in values])
    if option is None or len(option) != 5 or option[1] != "S" or option[3] != "R":
        raise ValueError(f"{path.name}: unsupported or missing Touchstone option line")
    scale = {"HZ": 1e-9, "KHZ": 1e-6, "MHZ": 1e-3, "GHZ": 1.0}[option[0]]
    data = np.asarray(rows, dtype=float)
    if len(data) < 2 or not np.isfinite(data).all():
        raise ValueError(f"{path.name}: invalid numeric data")
    freq = data[:, 0] * scale
    if not np.all(np.diff(freq) > 0):
        raise ValueError(f"{path.name}: frequencies must increase strictly")
    fmt = option[2]
    if fmt == "RI":
        s11 = data[:, 1] + 1j * data[:, 2]
    elif fmt in ("MA", "DB"):
        magnitude = data[:, 1] if fmt == "MA" else 10 ** (data[:, 1] / 20)
        s11 = magnitude * np.exp(1j * np.deg2rad(data[:, 2]))
    else:
        raise ValueError(f"{path.name}: unsupported format {fmt}")
    zref = float(option[4])
    if zref <= 0 or np.any(np.abs(s11) >= 1) or np.any(np.abs(s11) <= 0):
        raise ValueError(f"{path.name}: invalid reference impedance or reflection magnitude")
    return Network(label, path, freq, s11, zref, fmt)


def crossing(f0, d0, f1, d1, threshold=-10.0):
    return float(f0 + (threshold - d0) * (f1 - f0) / (d1 - d0))


def metrics(net, target, bounds):
    hits = np.flatnonzero(np.isclose(net.freq, target, rtol=0, atol=1e-9))
    if len(hits) != 1:
        raise ValueError(f"{net.label}: target must be an exported frequency sample")
    it = int(hits[0])
    mask = (net.freq >= bounds[0]) & (net.freq <= bounds[1])
    imin = int(np.argmin(np.where(mask, net.db, np.inf)))
    if net.db[imin] >= -10:
        raise ValueError(f"{net.label}: no -10 dB band around sampled minimum")
    left, right = imin, imin
    while left > 0 and net.db[left] <= -10:
        left -= 1
    while right < len(net.freq) - 1 and net.db[right] <= -10:
        right += 1
    if net.db[left] <= -10 or net.db[right] <= -10:
        raise ValueError(f"{net.label}: sweep does not bracket both -10 dB crossings")
    f_low = crossing(net.freq[left], net.db[left], net.freq[left + 1], net.db[left + 1])
    f_high = crossing(net.freq[right - 1], net.db[right - 1], net.freq[right], net.db[right])
    s = net.s11[it]
    z = net.zref * (1 + s) / (1 - s)
    return {
        "solver": net.label,
        "source_file": net.path.name,
        "encoding": net.encoding,
        "reference_impedance_ohm": net.zref,
        "exported_samples": len(net.freq),
        "export_start_GHz": float(net.freq[0]),
        "export_end_GHz": float(net.freq[-1]),
        "export_step_MHz": float(np.median(np.diff(net.freq)) * 1000),
        "target_frequency_GHz": target,
        "s11_at_target_dB": float(net.db[it]),
        "vswr_at_target": float((1 + abs(s)) / (1 - abs(s))),
        "zin_real_at_target_ohm": float(z.real),
        "zin_imag_at_target_ohm": float(z.imag),
        "reflected_power_at_target_percent": float(abs(s) ** 2 * 100),
        "sampled_minimum_frequency_GHz": float(net.freq[imin]),
        "sampled_minimum_s11_dB": float(net.db[imin]),
        "minus10_lower_GHz": f_low,
        "minus10_upper_GHz": f_high,
        "minus10_bandwidth_MHz": (f_high - f_low) * 1000,
        "fractional_bandwidth_percent_at_target": (f_high - f_low) / target * 100,
    }


def make_figure(networks, stats, target, bounds, outdir):
    colors = ("#1769aa", "#d86b20")
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10.5,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "svg.fonttype": "none"})
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 6.2), sharey=True)
    fig.subplots_adjust(left=.065, right=.975, bottom=.19, top=.755, wspace=.11)
    fig.suptitle("HFSS–CST S11 comparison", fontsize=19, weight="bold", y=.965)
    fig.text(.5, .902, "2.45 GHz inset-fed microstrip patch antenna  ·  50 Ω reference impedance",
             ha="center", color="#4b5563", fontsize=11.5)
    handles = []
    for ax in axes:
        for net, m, color in zip(networks, stats, colors):
            line, = ax.plot(net.freq, net.db, color=color, lw=2.05,
                            label=f"{net.label} ({m['export_step_MHz']:.0f} MHz export grid)")
            if ax is axes[0]:
                handles.append(line)
            ax.scatter(m["sampled_minimum_frequency_GHz"], m["sampled_minimum_s11_dB"],
                       color=color, marker="o", s=40, edgecolor="white", linewidth=.8, zorder=6)
        ax.axhline(-10, color="#6b7280", ls=(0, (5, 3)), lw=1.0)
        ax.axvline(target, color="#737373", ls=(0, (1, 3)), lw=1.2)
        ax.set_ylim(-40, 0)
        ax.set_xlabel("Frequency (GHz)", labelpad=8)
        ax.yaxis.set_major_locator(MultipleLocator(10))
        ax.yaxis.set_minor_locator(MultipleLocator(5))
        ax.grid(axis="both", color="#d8dde3", linewidth=.7)
        ax.grid(which="minor", axis="y", color="#eef0f3", linewidth=.6)
        ax.spines[["left", "bottom"]].set_color("#c4cad2")
        ax.tick_params(length=4, color="#9ca3af")
    axes[0].set_xlim(*bounds)
    axes[0].xaxis.set_major_locator(MultipleLocator(.2))
    axes[0].set_ylabel("S11 (dB)", labelpad=8)
    axes[0].set_title("Common frequency range", loc="left", fontsize=12.5, pad=14)
    axes[1].set_xlim(2.38, 2.52)
    axes[1].xaxis.set_major_locator(MultipleLocator(.02))
    axes[1].set_title("Resonance detail", loc="left", fontsize=12.5, pad=14)
    hfss, cst = stats
    axes[1].plot(networks[0].freq, networks[0].db, linestyle="none", marker=".",
                 markersize=4, color=colors[0], alpha=.9)
    axes[1].scatter(target, cst["s11_at_target_dB"], marker="s", color=colors[1],
                    edgecolor="white", linewidth=.8, s=40, zorder=6)
    annotation_style = {"fontsize": 9.6, "bbox": {"facecolor": "white", "edgecolor": "none",
                                                   "alpha": .95, "pad": 3}}
    axes[1].annotate(f"HFSS @ 2.450 GHz\n{hfss['s11_at_target_dB']:.2f} dB", xy=(target, hfss["s11_at_target_dB"]),
                     xytext=(2.486, -29), color=colors[0],
                     arrowprops={"arrowstyle": "-", "color": colors[0], "lw": .85}, **annotation_style)
    axes[1].annotate(f"CST @ 2.450 GHz\n{cst['s11_at_target_dB']:.2f} dB", xy=(target, cst["s11_at_target_dB"]),
                     xytext=(2.389, -18), color=colors[1],
                     arrowprops={"arrowstyle": "-", "color": colors[1], "lw": .85}, **annotation_style)
    axes[1].annotate(f"CST sampled minimum\n{cst['sampled_minimum_frequency_GHz']:.3f} GHz · {cst['sampled_minimum_s11_dB']:.2f} dB",
                     xy=(cst["sampled_minimum_frequency_GHz"], cst["sampled_minimum_s11_dB"]),
                     xytext=(2.385, -35.8), color=colors[1],
                     arrowprops={"arrowstyle": "-", "color": colors[1], "lw": .85}, **annotation_style)
    axes[0].text(2.014, -9.1, "−10 dB threshold", color="#5f6774", fontsize=9.4,
                 bbox={"facecolor": "white", "edgecolor": "none", "alpha": .9, "pad": 2})
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(.5, .874),
               ncol=2, frameon=False, handlelength=2.6, columnspacing=3)
    fig.text(.5, .088, f"−10 dB bandwidth: HFSS ≈ {hfss['minus10_bandwidth_MHz']:.1f} MHz   |   "
             f"CST ≈ {cst['minus10_bandwidth_MHz']:.1f} MHz", ha="center", fontsize=11.1, weight="medium")
    fig.text(.5, .038, "Curves connect original exported samples. Band edges use linear interpolation in dB; "
             "minimum markers identify sampled minima.", ha="center", fontsize=9.3, color="#5f6774")
    fig.savefig(outdir / "hfss_cst_s11_comparison.png", dpi=200, facecolor="white")
    fig.savefig(outdir / "hfss_cst_s11_comparison.svg", facecolor="white")
    plt.close(fig)


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hfss", type=Path, default=root / "data/hfss_s11.s1p")
    parser.add_argument("--cst", type=Path, default=root / "data/cst_s11.s1p")
    parser.add_argument("--outdir", type=Path, default=root / "results")
    parser.add_argument("--target", type=float, default=2.45)
    args = parser.parse_args()
    networks = (read_s1p(args.hfss, "HFSS"), read_s1p(args.cst, "CST TD"))
    if not all(np.isclose(net.zref, 50, rtol=0, atol=1e-9) for net in networks):
        raise ValueError("This comparison requires both exports to use a 50 Ω reference")
    bounds = (max(net.freq[0] for net in networks), min(net.freq[-1] for net in networks))
    if not bounds[0] <= args.target <= bounds[1]:
        raise ValueError("Target is outside the common frequency range")
    stats = [metrics(net, args.target, bounds) for net in networks]
    args.outdir.mkdir(parents=True, exist_ok=True)
    with (args.outdir / "hfss_cst_s11_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=stats[0].keys())
        writer.writeheader()
        writer.writerows(stats)
    make_figure(networks, stats, args.target, bounds, args.outdir)
    for m in stats:
        print(f"{m['solver']}: S11({args.target:g} GHz) = {m['s11_at_target_dB']:.5f} dB; "
              f"sampled minimum = {m['sampled_minimum_frequency_GHz']:.3f} GHz; "
              f"-10 dB bandwidth ≈ {m['minus10_bandwidth_MHz']:.3f} MHz")


if __name__ == "__main__":
    main()
