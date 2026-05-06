"""
Visualization script: Earthquake UFO vs Meteorite + Space Garbage WKB Tunneling
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import matplotlib.patheffects as pe

c = 3.0e8
hbar = 1.055e-34
R_earth = 6.371e6
L_earth = 2 * R_earth
V0_total = 2.5e32   # Earth binding energy (J)

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 1: Seismic Magnitude Comparison
# ─────────────────────────────────────────────────────────────────────────────
fig1, axes = plt.subplots(1, 2, figsize=(16, 7))
fig1.suptitle("Earthquake Generation: UFO vs Meteorite Impacts\nSeismic Energy & Magnitude Comparison",
              fontsize=14, fontweight='bold')

# Data
objects = ["Chelyabinsk\n(2013)", "Tunguska\n(1908)", "Barringer\n(50 ka)",
           "UFO\n(0.90c)", "Vredefort\n(2 Ga)", "Chicxulub\n(66 Ma)"]
Mw_vals = [4.5, 5.3, 5.8, 9.7, 11.0, 12.1]
E_seismic = [2.17e11, 3.65e12, 2.16e13, 1.16e19, 1.13e21, 4.6e22]
colors = ['#4488cc', '#4488cc', '#4488cc', '#ff4444', '#cc8800', '#cc0000']
hatches = ['', '', '', '//', '', '//']

ax1 = axes[0]
bars = ax1.bar(objects, Mw_vals, color=colors, edgecolor='white', linewidth=1.5)
for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)

# Reference lines
ax1.axhline(y=9.1, color='orange', linestyle='--', linewidth=1.5, alpha=0.8, label='Tohoku 2011 (Mw 9.1)')
ax1.axhline(y=9.5, color='red', linestyle='--', linewidth=1.5, alpha=0.8, label='Valdivia 1960 (Mw 9.5)')

# Annotate UFO bar
ax1.annotate('UFO: Mw 9.7\n(between Tohoku\nand Valdivia!)',
             xy=(3, 9.7), xytext=(3.5, 8.0),
             arrowprops=dict(arrowstyle='->', color='red', lw=2),
             fontsize=9, color='red', fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='#ffeeee', edgecolor='red', alpha=0.9))

ax1.set_ylabel('Moment Magnitude (Mw)', fontsize=12)
ax1.set_title('Moment Magnitude by Object', fontsize=12, fontweight='bold')
ax1.legend(fontsize=9)
ax1.set_ylim(0, 14)
ax1.grid(True, alpha=0.3, axis='y')

# Color legend
meteor_patch = mpatches.Patch(color='#4488cc', label='Meteorite/Asteroid')
ufo_patch = mpatches.Patch(color='#ff4444', label='UFO (0.90c)')
ancient_patch = mpatches.Patch(color='#cc8800', label='Ancient impact')
ax1.legend(handles=[meteor_patch, ufo_patch, ancient_patch], fontsize=9, loc='upper left')

# Plot 2: Seismic energy log scale
ax2 = axes[1]
y_pos = np.arange(len(objects))
bars2 = ax2.barh(y_pos, np.log10(E_seismic), color=colors, edgecolor='white', linewidth=1.5)
for bar, hatch in zip(bars2, hatches):
    bar.set_hatch(hatch)

ax2.set_yticks(y_pos)
ax2.set_yticklabels(objects, fontsize=10)
ax2.set_xlabel('log10(Seismic Energy) [J]', fontsize=12)
ax2.set_title('Seismic Energy (log scale)', fontsize=12, fontweight='bold')

# Reference lines
ax2.axvline(x=np.log10(2e17), color='orange', linestyle='--', linewidth=1.5, alpha=0.8, label='Tohoku 2011')
ax2.axvline(x=np.log10(1e18), color='red', linestyle='--', linewidth=1.5, alpha=0.8, label='Valdivia 1960')

ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (E, bar) in enumerate(zip(E_seismic, bars2)):
    ax2.text(np.log10(E) + 0.2, i, f'{np.log10(E):.1f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('/home/ubuntu/eq_fig1_magnitude.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 1 saved.")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 2: Seismic Waveform Schematic
# ─────────────────────────────────────────────────────────────────────────────
fig2, axes2 = plt.subplots(2, 2, figsize=(16, 10))
fig2.suptitle("Seismic Signature Comparison: UFO vs Meteorite\nSchematic Waveforms and Source Geometry",
              fontsize=14, fontweight='bold')
fig2.patch.set_facecolor('#0d1117')
for ax in axes2.flat:
    ax.set_facecolor('#0d1117')

# Panel 1: UFO waveform (schematic)
ax = axes2[0, 0]
t = np.linspace(0, 300, 3000)
# UFO: two sharp spikes (entry + exit), very short duration
ufo_wave = np.zeros_like(t)
# Entry shock at t=10s (seismic wave travel time from entry point)
entry_idx = np.argmin(np.abs(t - 10))
exit_idx = np.argmin(np.abs(t - 57))   # 47ms transit + travel time
for i in range(len(t)):
    ufo_wave[i] += 9.7 * np.exp(-((t[i]-10)/0.5)**2) * np.sin(2*np.pi*t[i]*2)
    ufo_wave[i] += 9.7 * np.exp(-((t[i]-57)/0.5)**2) * np.sin(2*np.pi*t[i]*2)
    ufo_wave[i] += 2.0 * np.exp(-((t[i]-80)/15)**2) * np.sin(2*np.pi*t[i]*0.1)  # coda

ax.plot(t, ufo_wave, color='#ff4444', linewidth=1.2)
ax.axvline(x=10, color='cyan', linestyle='--', linewidth=1.5, label='Entry shock')
ax.axvline(x=57, color='lime', linestyle='--', linewidth=1.5, label='Exit shock')
ax.set_title('UFO Seismic Waveform (Schematic)', fontsize=11, fontweight='bold', color='white')
ax.set_xlabel('Time (s)', fontsize=10, color='white')
ax.set_ylabel('Ground velocity (arb.)', fontsize=10, color='white')
ax.tick_params(colors='white')
ax.legend(fontsize=9)
ax.text(10, 8, 'Entry\nshock', fontsize=8, color='cyan', ha='center')
ax.text(57, 8, 'Exit\nshock', fontsize=8, color='lime', ha='center')
ax.text(150, 5, 'Mw 9.7\nLinear source\n47 ms transit', fontsize=9, color='#ff8888',
        bbox=dict(boxstyle='round', facecolor='#220000', edgecolor='#ff4444', alpha=0.8))
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')

# Panel 2: Meteorite waveform (Chelyabinsk-style)
ax = axes2[0, 1]
t2 = np.linspace(0, 300, 3000)
meteor_wave = np.zeros_like(t2)
for i in range(len(t2)):
    # Airburst: single event, longer duration
    meteor_wave[i] += 4.5 * np.exp(-((t2[i]-30)/8)**2) * np.sin(2*np.pi*t2[i]*0.5)
    meteor_wave[i] += 1.5 * np.exp(-((t2[i]-80)/20)**2) * np.sin(2*np.pi*t2[i]*0.2)
    meteor_wave[i] += 0.5 * np.exp(-((t2[i]-150)/30)**2) * np.sin(2*np.pi*t2[i]*0.1)

ax.plot(t2, meteor_wave, color='#4488cc', linewidth=1.2)
ax.axvline(x=30, color='yellow', linestyle='--', linewidth=1.5, label='Airburst')
ax.set_title('Chelyabinsk-type Waveform (Schematic)', fontsize=11, fontweight='bold', color='white')
ax.set_xlabel('Time (s)', fontsize=10, color='white')
ax.set_ylabel('Ground velocity (arb.)', fontsize=10, color='white')
ax.tick_params(colors='white')
ax.legend(fontsize=9)
ax.text(30, 3.5, 'Airburst', fontsize=8, color='yellow', ha='center')
ax.text(150, 2.5, 'Mw 4.5\nPoint source\nSingle event', fontsize=9, color='#88aaff',
        bbox=dict(boxstyle='round', facecolor='#000022', edgecolor='#4488cc', alpha=0.8))
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')

# Panel 3: Source geometry comparison
ax = axes2[1, 0]
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')

# Earth circle
earth_circle = plt.Circle((0, 0), 1.0, color='#1a3a5c', fill=True, linewidth=2, edgecolor='#4488cc')
ax.add_patch(earth_circle)

# UFO path (straight line through Earth)
ax.annotate('', xy=(1.3, 0), xytext=(-1.3, 0),
            arrowprops=dict(arrowstyle='->', color='#ff4444', lw=3))
ax.plot([-1.0, 1.0], [0, 0], 'r-', linewidth=4, alpha=0.8, label='UFO path (linear source)')
ax.plot(-1.0, 0, 'r^', markersize=12, label='Entry point')
ax.plot(1.0, 0, 'rv', markersize=12, label='Exit point')

# Seismic waves from UFO (cylindrical)
for x_src in np.linspace(-0.8, 0.8, 5):
    circle = plt.Circle((x_src, 0), 0.3, color='#ff4444', fill=False, linewidth=0.8, alpha=0.4, linestyle='--')
    ax.add_patch(circle)

ax.set_title('UFO: Linear Source Geometry', fontsize=11, fontweight='bold', color='white')
ax.legend(fontsize=8, loc='upper right')
ax.set_xlabel('Earth cross-section', fontsize=10, color='white')
ax.tick_params(colors='white')
ax.text(0, -1.3, 'Cylindrical wavefront\n(multiple source points)', fontsize=9,
        ha='center', color='#ff8888')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')

# Panel 4: Meteorite point source geometry
ax = axes2[1, 1]
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')

earth_circle2 = plt.Circle((0, 0), 1.0, color='#1a3a5c', fill=True, linewidth=2, edgecolor='#4488cc')
ax.add_patch(earth_circle2)

# Meteorite impact at top
ax.plot(0, 1.0, 'b^', markersize=15, color='yellow', label='Impact/airburst point')
ax.annotate('', xy=(0, 1.0), xytext=(0, 1.4),
            arrowprops=dict(arrowstyle='->', color='yellow', lw=2))

# Spherical seismic waves
for r in [0.3, 0.6, 0.9, 1.2]:
    circle = plt.Circle((0, 1.0), r, color='#4488cc', fill=False, linewidth=0.8, alpha=0.5, linestyle='--')
    ax.add_patch(circle)

ax.set_title('Meteorite: Point Source Geometry', fontsize=11, fontweight='bold', color='white')
ax.legend(fontsize=8, loc='upper right')
ax.set_xlabel('Earth cross-section', fontsize=10, color='white')
ax.tick_params(colors='white')
ax.text(0, -1.3, 'Spherical wavefront\n(single source point)', fontsize=9,
        ha='center', color='#88aaff')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')

plt.tight_layout()
plt.savefig('/home/ubuntu/eq_fig2_waveforms.png', dpi=150, bbox_inches='tight',
            facecolor='#0d1117')
plt.close()
print("Figure 2 saved.")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 3: Space Garbage WKB Tunneling
# ─────────────────────────────────────────────────────────────────────────────
fig3, axes3 = plt.subplots(1, 2, figsize=(16, 7))
fig3.suptitle("WKB Quantum Tunneling of Space Garbage Through Earth\nlog10(T) = -2Γ/ln(10), Γ = κL",
              fontsize=14, fontweight='bold')

# Panel 1: Tunneling probability vs mass
ax = axes3[0]
masses = np.logspace(-10, 8, 500)  # 0.1 μg to 100,000 tonnes
v_leo = 7.8e3  # m/s

log10_T_vals = []
for m in masses:
    KE = 0.5 * m * v_leo**2
    if KE >= V0_total:
        log10_T_vals.append(0)
    else:
        kappa = np.sqrt(2 * m * (V0_total - KE)) / hbar
        Gamma = kappa * L_earth
        log10_T_vals.append(-2 * Gamma / np.log(10))

log10_T_vals = np.array(log10_T_vals)

ax.semilogx(masses, log10_T_vals, 'b-', linewidth=2.5, label='LEO debris (v=7.8 km/s)')

# Mark specific objects
debris_marks = {
    "Paint fleck\n(0.1 μg)":   (1e-10, -2.346e52, 'cyan'),
    "Paint chip\n(1 mg)":      (1e-6,  -2.346e54, 'lime'),
    "Bolt\n(10 g)":            (1e-2,  -2.346e56, 'yellow'),
    "CubeSat\n(1 kg)":         (1.0,   -2.346e57, 'orange'),
    "Rocket\nstage (1t)":      (1e3,   -7.418e58, 'tomato'),
    "Dead satellite\n(10t)":   (1e4,   -2.346e59, 'red'),
}

for label, (m, log10T, color) in debris_marks.items():
    ax.plot(m, log10T, 'o', color=color, markersize=10, zorder=5)
    ax.annotate(label, xy=(m, log10T), xytext=(m*3, log10T*0.85),
                fontsize=7.5, color=color,
                arrowprops=dict(arrowstyle='->', color=color, lw=1))

ax.set_xlabel('Object Mass (kg)', fontsize=12)
ax.set_ylabel('log₁₀(Tunneling Probability T)', fontsize=12)
ax.set_title('WKB Tunneling Probability vs Mass\n(All space debris at LEO velocity 7.8 km/s)', fontsize=11, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
ax.text(1e-8, -1e61, 'All values are\neffectively ZERO\n(T ≈ 10^(-10^50))', fontsize=10,
        color='red', fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='#fff0f0', edgecolor='red', alpha=0.9))

# Panel 2: Debris size spectrum
ax2 = axes3[1]
categories = ['Paint flecks\n(<1mm)', 'Fragments\n(1-10cm)', 'Tracked objects\n(>10cm)',
              'Dead satellites', 'Rocket bodies', 'UFO\n(reference)']
counts = [1e8, 1e6, 2.7e4, 3e3, 2e3, 1]
log10_T_cats = [-2.3e52, -2.3e56, -2.3e58, -2.3e59, -2.3e59, 0]
colors_cat = ['#88ccff', '#4488cc', '#2255aa', '#ff8800', '#cc4400', '#ff0000']

# Bar chart of object count
ax2_twin = ax2.twinx()
bars = ax2.bar(categories, np.log10(counts), color=colors_cat, alpha=0.7, edgecolor='white', linewidth=1.5)
ax2.set_ylabel('log₁₀(Number of Objects in LEO)', fontsize=11, color='steelblue')
ax2.tick_params(axis='y', labelcolor='steelblue')
ax2.set_ylim(0, 12)

# Overlay tunneling probability as line (normalized for display)
log10_T_display = [-52, -54, -58, -59, -59, 0]  # simplified for display
ax2_twin.plot(categories, log10_T_display, 'r-o', linewidth=2.5, markersize=8,
              label='log₁₀(T) (simplified)', color='red')
ax2_twin.set_ylabel('log₁₀(Tunneling Probability) [simplified]', fontsize=11, color='red')
ax2_twin.tick_params(axis='y', labelcolor='red')
ax2_twin.set_ylim(-65, 5)
ax2_twin.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax2_twin.text(4.5, 1, 'Classical\nthreshold', fontsize=8, color='red', ha='center')

ax2.set_title('Space Debris Population vs Tunneling Probability\n(ESA Space Debris Report 2023)', fontsize=11, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

lines, labels = ax2_twin.get_legend_handles_labels()
bars_legend = mpatches.Patch(color='steelblue', alpha=0.7, label='Object count (log10)')
ax2.legend(handles=[bars_legend] + lines, labels=['Object count (log10)'] + labels, fontsize=9)

plt.tight_layout()
plt.savefig('/home/ubuntu/eq_fig3_debris_tunneling.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 3 saved.")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 4: PGA Distance Map
# ─────────────────────────────────────────────────────────────────────────────
fig4, ax4 = plt.subplots(figsize=(12, 7))

distances = np.logspace(2, 7, 500)  # 100m to 10,000 km
rho_crust = 2700
v_s = 3500

E_seismic_data = {
    "Chelyabinsk (Mw 4.5)":  (2.17e11, '#4488cc', '-'),
    "Tunguska (Mw 5.3)":     (3.65e12, '#2266aa', '--'),
    "Barringer (Mw 5.8)":    (2.16e13, '#0044aa', ':'),
    "UFO 0.90c (Mw 9.7)":    (1.16e19, '#ff4444', '-'),
    "Vredefort (Mw 11.0)":   (1.13e21, '#cc8800', '--'),
    "Chicxulub (Mw 12.1)":   (4.6e22,  '#cc0000', ':'),
}

for label, (E_s, color, ls) in E_seismic_data.items():
    PGA = np.sqrt(E_s / (2 * np.pi * rho_crust * v_s**2 * distances**2)) / 9.81
    ax4.loglog(distances / 1e3, PGA, color=color, linewidth=2.5, linestyle=ls, label=label)

# Reference lines
ax4.axhline(y=1.0, color='orange', linestyle='--', linewidth=1.5, alpha=0.8, label='PGA = 1g (catastrophic damage)')
ax4.axhline(y=0.1, color='yellow', linestyle='--', linewidth=1.5, alpha=0.8, label='PGA = 0.1g (severe damage)')
ax4.axhline(y=0.01, color='lime', linestyle='--', linewidth=1.5, alpha=0.8, label='PGA = 0.01g (moderate damage)')

ax4.set_xlabel('Distance from Source (km)', fontsize=12)
ax4.set_ylabel('Peak Ground Acceleration (g)', fontsize=12)
ax4.set_title('Peak Ground Acceleration vs Distance\nUFO vs Historical Meteorite Impacts',
              fontsize=13, fontweight='bold')
ax4.legend(fontsize=9, loc='upper right')
ax4.grid(True, alpha=0.3, which='both')
ax4.set_xlim([0.1, 1e4])

# Shade damage zones
ax4.axhspan(1.0, 1e5, alpha=0.08, color='red', label='Catastrophic zone')
ax4.axhspan(0.1, 1.0, alpha=0.06, color='orange')
ax4.axhspan(0.01, 0.1, alpha=0.04, color='yellow')

plt.tight_layout()
plt.savefig('/home/ubuntu/eq_fig4_pga.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 4 saved.")

print("\nAll figures saved successfully!")
