"""
Visualizations for:
1. Cherenkov Radiation in the Deep Ocean / Kraken
2. Radiation and Origin of Life
3. WKB Tunneling of Space Debris and Meteorites
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch, Arc, Wedge, Circle, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'figure.dpi': 150,
    'axes.grid': True,
    'grid.alpha': 0.3,
})

c = 2.998e8
n_sea = 1.340
eV = 1.602e-19
hbar = 1.055e-34
amu = 1.661e-27
m_p = 1.673e-27

# ============================================================
# FIGURE 1: Cherenkov Angle vs Velocity — Multiple Media
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Cherenkov Radiation in the Deep Ocean", fontsize=15, fontweight='bold')

ax1, ax2 = axes

media = {
    "Seawater (n=1.340)":   {"n": 1.340, "color": "#0077b6", "ls": "-"},
    "Freshwater (n=1.333)": {"n": 1.333, "color": "#00b4d8", "ls": "--"},
    "Ice (n=1.310)":        {"n": 1.310, "color": "#90e0ef", "ls": "-."},
    "Dense glass (n=1.500)":{"n": 1.500, "color": "#023e8a", "ls": ":"},
}

betas = np.linspace(0.60, 1.0, 1000)

for label, props in media.items():
    n = props["n"]
    thresh = 1.0 / n
    angles = []
    valid_betas = []
    for b in betas:
        cos_t = 1.0 / (n * b)
        if cos_t <= 1.0:
            angles.append(np.degrees(np.arccos(cos_t)))
            valid_betas.append(b)
    ax1.plot(valid_betas, angles, color=props["color"], ls=props["ls"],
             linewidth=2, label=label)
    ax1.axvline(thresh, color=props["color"], alpha=0.3, linewidth=1)

# Mark key particles
particles = {
    "K-40 β (0.8c)": 0.80,
    "Cosmic μ (0.99c)": 0.99,
    "UFO (0.90c)": 0.90,
}
for pname, pb in particles.items():
    cos_t = 1.0 / (n_sea * pb)
    if cos_t <= 1.0:
        angle = np.degrees(np.arccos(cos_t))
        ax1.scatter([pb], [angle], s=80, zorder=5, color='red')
        ax1.annotate(pname, (pb, angle), textcoords="offset points",
                    xytext=(5, 5), fontsize=8, color='red')

ax1.set_xlabel("Particle velocity (β = v/c)")
ax1.set_ylabel("Cherenkov angle θ_C (degrees)")
ax1.set_title("Cherenkov Angle vs. Particle Velocity")
ax1.legend(fontsize=9)
ax1.set_xlim(0.60, 1.0)
ax1.set_ylim(0, 50)

# Panel 2: Frank-Tamm photon yield
def photons_per_cm(beta, n, l1=400e-9, l2=700e-9):
    alpha = 1/137.036
    cos_t = 1.0 / (n * beta)
    if cos_t >= 1.0:
        return 0
    sin2 = 1 - cos_t**2
    return 2 * np.pi * alpha * sin2 * (1/l1 - 1/l2) / 100

for label, props in media.items():
    n = props["n"]
    yields = [photons_per_cm(b, n) for b in betas]
    ax2.plot(betas, yields, color=props["color"], ls=props["ls"],
             linewidth=2, label=label)

ax2.set_xlabel("Particle velocity (β = v/c)")
ax2.set_ylabel("Visible photons per cm of path")
ax2.set_title("Frank-Tamm Photon Yield (400–700 nm)")
ax2.legend(fontsize=9)
ax2.set_xlim(0.60, 1.0)
ax2.set_ylim(0, 40)

# Shade K-40 electron range
ax2.axvspan(0.746, 0.98, alpha=0.08, color='blue', label='K-40 β range')
ax2.annotate("K-40 β electrons\n(0.75–0.98c)", xy=(0.86, 15),
            fontsize=8, color='#0077b6', ha='center')

plt.tight_layout()
plt.savefig("/home/ubuntu/kraken_fig1_cherenkov_angle.png", bbox_inches='tight', dpi=150)
plt.close()
print("Figure 1 saved.")

# ============================================================
# FIGURE 2: Deep Ocean Cherenkov Scenario — The Kraken
# ============================================================
fig, ax = plt.subplots(figsize=(12, 9))
ax.set_facecolor('#001f3f')
fig.patch.set_facecolor('#001f3f')

# Ocean depth gradient
gradient = np.linspace(0, 1, 300).reshape(300, 1)
ocean_cmap = LinearSegmentedColormap.from_list('ocean',
    ['#001f3f', '#003366', '#004080', '#005599', '#0077b6'])
ax.imshow(gradient, extent=[0, 10, 0, 10], aspect='auto',
          cmap=ocean_cmap, alpha=0.8, zorder=0)

# Draw the kraken (simplified)
from matplotlib.patches import Ellipse
kraken_x, kraken_y = 5.0, 4.5
# Body
body = Ellipse((kraken_x, kraken_y), 3.5, 1.8, color='#4a1942', zorder=3, alpha=0.9)
ax.add_patch(body)
# Tentacles
for i, (dx, dy_end) in enumerate([(-1.5,-2),(-0.8,-2.5),(0,-2.8),(0.8,-2.5),(1.5,-2),
                                    (-1.2,-1.8),(1.2,-1.8),(-0.4,-2.2),(0.4,-2.2)]):
    ax.plot([kraken_x + dx*0.3, kraken_x + dx],
            [kraken_y - 0.8, kraken_y + dy_end],
            color='#6b2d6b', linewidth=3, zorder=2, alpha=0.8,
            solid_capstyle='round')
# Eye
eye = Circle((kraken_x + 0.6, kraken_y + 0.2), 0.18, color='#ff6b35', zorder=4)
ax.add_patch(eye)
pupil = Circle((kraken_x + 0.65, kraken_y + 0.2), 0.08, color='black', zorder=5)
ax.add_patch(pupil)

ax.text(kraken_x, kraken_y + 1.5, "KRAKEN\n(Hypothetical, ~50m)", color='white',
        fontsize=9, ha='center', va='bottom', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#4a1942', alpha=0.7))

# Draw Cherenkov cone from a cosmic ray muon
muon_start = (1.0, 9.5)
muon_end = (9.0, 0.5)
dx = muon_end[0] - muon_start[0]
dy = muon_end[1] - muon_start[1]
ax.annotate("", xy=muon_end, xytext=muon_start,
            arrowprops=dict(arrowstyle='->', color='#ff9f1c', lw=2.5))
ax.text(1.2, 9.2, "Cosmic ray μ\n(v = 0.99c)", color='#ff9f1c',
        fontsize=9, fontweight='bold')

# Cherenkov cone (34° half-angle in seawater)
theta_C = 34.0  # degrees
cone_length = 3.0
# Draw cone lines along muon path
muon_angle = np.degrees(np.arctan2(dy, dx))
for side in [+1, -1]:
    cone_angle = muon_angle + side * theta_C
    cx = muon_start[0] + cone_length * np.cos(np.radians(cone_angle))
    cy = muon_start[1] + cone_length * np.sin(np.radians(cone_angle))
    ax.plot([muon_start[0], cx], [muon_start[1], cy],
            color='#00f5ff', alpha=0.6, linewidth=1.5, linestyle='--')

# Cherenkov glow along path
for t in np.linspace(0.1, 0.9, 20):
    px = muon_start[0] + t * dx
    py = muon_start[1] + t * dy
    glow = Circle((px, py), 0.15, color='#00f5ff', alpha=0.15, zorder=1)
    ax.add_patch(glow)

ax.text(3.5, 7.5, f"Cherenkov cone\nθ_C = {theta_C:.0f}°\n(seawater, n=1.34)",
        color='#00f5ff', fontsize=9, ha='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#001f3f', alpha=0.8))

# K-40 background glow
for _ in range(40):
    rx = np.random.uniform(0.5, 9.5)
    ry = np.random.uniform(0.5, 8.5)
    rg = Circle((rx, ry), 0.05, color='#7ec8e3', alpha=0.4, zorder=1)
    ax.add_patch(rg)

ax.text(0.3, 0.5, "K-40 background Cherenkov\n(~12,500 photon events/L/s)",
        color='#7ec8e3', fontsize=8,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#001f3f', alpha=0.8))

# Depth label
ax.text(9.5, 9.0, "Surface", color='white', fontsize=9, ha='right', alpha=0.7)
ax.text(9.5, 0.5, "~3,000 m depth", color='white', fontsize=9, ha='right', alpha=0.7)

ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Cherenkov Radiation in the Deep Ocean: The Kraken's World",
             color='white', fontsize=13, fontweight='bold', pad=10)

plt.tight_layout()
plt.savefig("/home/ubuntu/kraken_fig2_deep_ocean_scene.png", bbox_inches='tight',
            dpi=150, facecolor='#001f3f')
plt.close()
print("Figure 2 saved.")

# ============================================================
# FIGURE 3: Origin of Life — Radiation Timeline
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Radiation and the Origin of Life on Early Earth", fontsize=15, fontweight='bold')

# Panel A: Isotope abundance over time
ax = axes[0, 0]
times = np.linspace(0, 4.5, 500)  # Ga ago
K40 = 2**(times / 1.25)
U238 = 2**(times / 4.47)
U235 = 2**(times / 0.704)
Th232 = 2**(times / 14.0)

ax.semilogy(times, K40, 'b-', linewidth=2, label='K-40 (t½=1.25 Ga)')
ax.semilogy(times, U238, 'r-', linewidth=2, label='U-238 (t½=4.47 Ga)')
ax.semilogy(times, U235, 'g-', linewidth=2, label='U-235 (t½=0.704 Ga)')
ax.semilogy(times, Th232, 'm-', linewidth=2, label='Th-232 (t½=14.0 Ga)')
ax.axvline(4.0, color='orange', linestyle='--', linewidth=1.5, label='4.0 Ga (early life)')
ax.axvline(3.5, color='red', linestyle=':', linewidth=1.5, label='3.5 Ga (first fossils)')
ax.set_xlabel("Time before present (Ga)")
ax.set_ylabel("Relative abundance (today = 1)")
ax.set_title("Radioactive Isotope Abundance Over Time")
ax.legend(fontsize=8)
ax.invert_xaxis()

# Panel B: Dose rate over time
ax = axes[0, 1]
dose_modern = 2.4e-3  # Gy/year
dose_over_time = dose_modern * (K40 * 0.4 + U238 * 0.3 + U235 * 0.1 + Th232 * 0.2)
ax.semilogy(times, dose_over_time * 1000, 'darkred', linewidth=2.5)
ax.axvline(4.0, color='orange', linestyle='--', linewidth=1.5)
ax.axhline(2.4, color='gray', linestyle=':', linewidth=1.5, label='Modern dose (2.4 mGy/yr)')
ax.fill_between(times, dose_over_time * 1000, alpha=0.2, color='red')
ax.set_xlabel("Time before present (Ga)")
ax.set_ylabel("Estimated dose rate (mGy/year)")
ax.set_title("Natural Background Radiation Dose Rate")
ax.legend(fontsize=9)
ax.invert_xaxis()
ax.annotate("~10x higher\nat 4.0 Ga", xy=(4.0, 23.1), xytext=(3.0, 50),
            arrowprops=dict(arrowstyle='->', color='darkred'),
            fontsize=9, color='darkred')

# Panel C: UV radiation penetration depth in early ocean
ax = axes[1, 0]
depths = np.linspace(0, 100, 500)  # meters
# UV-C (254nm) attenuation in water: ~0.1 m^-1
# UV-B (300nm): ~0.05 m^-1
mu_UVC = 0.1   # m^-1
mu_UVB = 0.05  # m^-1
mu_UVA = 0.01  # m^-1

I0_early = 100  # relative units (early Earth, no ozone)
I0_modern = 1   # relative units

for label, mu, I0, color, ls in [
    ("UV-C 254nm (early)", mu_UVC, I0_early, 'purple', '-'),
    ("UV-B 300nm (early)", mu_UVB, I0_early, 'blue', '-'),
    ("UV-A 360nm (early)", mu_UVA, I0_early, 'cyan', '-'),
    ("UV-B 300nm (modern)", mu_UVB, I0_modern, 'blue', '--'),
]:
    I = I0 * np.exp(-mu * depths)
    ax.semilogy(depths, I, color=color, ls=ls, linewidth=2, label=label)

ax.axhline(1.0, color='gray', linestyle=':', linewidth=1, label='Modern UV-B surface level')
ax.set_xlabel("Ocean depth (m)")
ax.set_ylabel("Relative UV intensity")
ax.set_title("UV Penetration in Early Earth Ocean")
ax.legend(fontsize=8)
ax.set_xlim(0, 100)

# Panel D: Prebiotic molecule production
ax = axes[1, 1]
categories = ['HCN\n(ionizing rad)', 'Amino acid\nprecursors\n(ionizing rad)',
              'Amino acids\n(meteorites)', 'Nucleobases\n(UV photochem)']
values = [1.48e20, 1.48e19, 5e12, 1e18]  # per m² per year (normalized estimates)
colors = ['#e63946', '#457b9d', '#2a9d8f', '#e9c46a']

bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=0.8)
ax.set_yscale('log')
ax.set_ylabel("Molecules produced per m² per year")
ax.set_title("Prebiotic Molecule Production Rates")
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, val * 1.5,
            f'{val:.1e}', ha='center', va='bottom', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig("/home/ubuntu/kraken_fig3_origin_of_life.png", bbox_inches='tight', dpi=150)
plt.close()
print("Figure 3 saved.")

# ============================================================
# FIGURE 4: WKB Tunneling — Space Debris and Meteorites
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.suptitle("WKB Quantum Tunneling of Space Debris and Meteorites Through Earth",
             fontsize=14, fontweight='bold')

# Panel A: Tunneling exponent comparison
ax = axes[0]
objects = {
    "Paint fleck\n(1mm, 1μg)":     {"log10_T": -5.21e40, "color": "#e63946"},
    "Bolt\n(10g)":                  {"log10_T": -1.04e44, "color": "#f4a261"},
    "Satellite\n(1 tonne)":         {"log10_T": -3.30e48, "color": "#e9c46a"},
    "Chondrite\n(10 kg)":           {"log10_T": -3.96e46, "color": "#2a9d8f"},
    "Iron meteorite\n(1 tonne)":    {"log10_T": -1.12e48, "color": "#264653"},
    "Chelyabinsk\n(12,000 t)":      {"log10_T": -1.14e53, "color": "#6d2b3d"},
    "UFO\n(10,000 kg, 0.9c)":       {"log10_T": -1.04e50, "color": "#7209b7"},
}

names = list(objects.keys())
exponents = [abs(v["log10_T"]) for v in objects.values()]
colors = [v["color"] for v in objects.values()]

bars = ax.barh(names, np.log10(exponents), color=colors, edgecolor='black', linewidth=0.8)
ax.set_xlabel("log₁₀(|log₁₀(T)|) — Impossibility Scale")
ax.set_title("Tunneling Impossibility\n(larger = more impossible)")
for bar, exp in zip(bars, exponents):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
            f'10^({exp:.1e})', va='center', fontsize=7)
ax.set_xlim(0, 60)

# Panel B: Velocity needed for classical penetration
ax = axes[1]
obj_names = ["Paint fleck\n(1mm)", "Bolt\n(10g)", "Chondrite\n(10kg)",
             "Satellite\n(1t)", "Iron met.\n(1t)", "Chelyabinsk\n(12kt)"]
thresh_betas = [0.9994, 0.8823, 0.5092, 0.4381, 0.1597, 0.00137]
thresh_colors = ['#e63946', '#f4a261', '#2a9d8f', '#e9c46a', '#264653', '#6d2b3d']

bars2 = ax.bar(obj_names, thresh_betas, color=thresh_colors, edgecolor='black', linewidth=0.8)
ax.axhline(1.0, color='gray', linestyle='--', linewidth=1, label='Speed of light')
ax.set_ylabel("Threshold velocity (β = v/c)")
ax.set_title("Minimum Velocity for\nClassical Earth Penetration")
ax.set_ylim(0, 1.1)
for bar, beta in zip(bars2, thresh_betas):
    ax.text(bar.get_x() + bar.get_width()/2, beta + 0.02,
            f'{beta:.3f}c', ha='center', va='bottom', fontsize=8, fontweight='bold')
ax.tick_params(axis='x', labelsize=8)

# Panel C: Impact energy comparison
ax = axes[2]
impact_names = ["LEO bolt\n(10g)", "Iron met.\n(1t)", "Chelyabinsk\n(2013)",
                "Tunguska\n(1908)", "Chicxulub\n(66 Ma)"]
impact_TNT = [7.27e-3, 74.7, 5.18e8, 8.71e6, 9.56e13]
impact_colors = ['#f4a261', '#264653', '#e63946', '#e9c46a', '#6d2b3d']

bars3 = ax.bar(impact_names, impact_TNT, color=impact_colors, edgecolor='black', linewidth=0.8)
ax.set_yscale('log')
ax.set_ylabel("Impact energy (tonnes TNT equivalent)")
ax.set_title("Meteorite/Debris Impact Energies")
for bar, tnt in zip(bars3, impact_TNT):
    ax.text(bar.get_x() + bar.get_width()/2, tnt * 1.5,
            f'{tnt:.1e}', ha='center', va='bottom', fontsize=8, fontweight='bold')
ax.tick_params(axis='x', labelsize=8)

# Reference lines
ax.axhline(1.5e7, color='red', linestyle='--', linewidth=1, alpha=0.7)
ax.text(4.3, 2e7, 'Tsar Bomba\n(50 Mt)', fontsize=7, color='red', ha='right')
ax.axhline(1.5e4, color='orange', linestyle='--', linewidth=1, alpha=0.7)
ax.text(4.3, 2e4, 'Hiroshima\n(15 kt)', fontsize=7, color='orange', ha='right')

plt.tight_layout()
plt.savefig("/home/ubuntu/kraken_fig4_debris_tunneling.png", bbox_inches='tight', dpi=150)
plt.close()
print("Figure 4 saved.")

# ============================================================
# FIGURE 5: Cherenkov Cone Geometry in Ocean
# ============================================================
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_facecolor('#001a33')
fig.patch.set_facecolor('#001a33')

# Draw particle track
ax.annotate("", xy=(9, 5), xytext=(1, 5),
            arrowprops=dict(arrowstyle='->', color='#ff9f1c', lw=3))
ax.text(0.8, 5.3, "Particle\n(v = 0.99c)", color='#ff9f1c', fontsize=10, fontweight='bold')

# Cherenkov cone
theta_C_rad = np.radians(34.0)
cone_x = np.linspace(1, 9, 200)
upper = 5 + (cone_x - 1) * np.tan(theta_C_rad)
lower = 5 - (cone_x - 1) * np.tan(theta_C_rad)
ax.fill_between(cone_x, lower, upper, alpha=0.15, color='#00f5ff')
ax.plot(cone_x, upper, color='#00f5ff', linewidth=2, linestyle='--', label=f'Cherenkov cone (θ_C = 34°)')
ax.plot(cone_x, lower, color='#00f5ff', linewidth=2, linestyle='--')

# Wavefronts (Huygens construction)
for x0 in [2, 3, 4, 5, 6, 7, 8]:
    r = (9 - x0) * np.tan(theta_C_rad)
    circle = Circle((x0, 5), r, fill=False, color='#00f5ff', alpha=0.25, linewidth=1)
    ax.add_patch(circle)

# Angle annotation
ax.annotate("", xy=(3, 5 + 2*np.tan(theta_C_rad)), xytext=(3, 5),
            arrowprops=dict(arrowstyle='->', color='white', lw=1.5))
ax.text(3.2, 5 + np.tan(theta_C_rad), f'θ_C = 34°\n(seawater)', color='white', fontsize=9)

# Kraken silhouette (simplified)
kraken_body = Ellipse((5.5, 2.5), 2.5, 1.2, color='#4a1942', alpha=0.8, zorder=5)
ax.add_patch(kraken_body)
for tx, ty in [(-0.8,-0.8),(-0.4,-1.1),(0,-1.2),(0.4,-1.1),(0.8,-0.8)]:
    ax.plot([5.5+tx*0.4, 5.5+tx], [2.5-0.5, 2.5+ty], color='#6b2d6b', lw=2, zorder=4)
ax.text(5.5, 1.0, "Kraken", color='white', fontsize=9, ha='center', fontweight='bold')

# Radiation hitting kraken
ax.annotate("", xy=(5.5, 2.5), xytext=(5.5, 5 - (5.5-1)*np.tan(theta_C_rad)),
            arrowprops=dict(arrowstyle='->', color='#ff6b35', lw=2, linestyle='dashed'))
ax.text(5.8, 3.8, "Cherenkov\nphotons\n(UV-blue)", color='#ff6b35', fontsize=9)

ax.set_xlim(0, 10)
ax.set_ylim(0, 9)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Cherenkov Cone Geometry in Seawater\n(Huygens wavefront construction)",
             color='white', fontsize=12, fontweight='bold')
ax.legend(loc='upper right', fontsize=9, facecolor='#001a33', labelcolor='white',
          edgecolor='white')

plt.tight_layout()
plt.savefig("/home/ubuntu/kraken_fig5_cherenkov_cone.png", bbox_inches='tight',
            dpi=150, facecolor='#001a33')
plt.close()
print("Figure 5 saved.")

# ============================================================
# FIGURE 6: Meteorite WKB potential profile
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("WKB Potential Profile: Meteorite vs UFO Through Earth", fontsize=14, fontweight='bold')

R_earth = 6.371e6
N = 10000
s = np.linspace(0, 2*R_earth, N)

def prem_density(r_frac):
    x = r_frac
    if x <= 0.192:
        return 1000 * (13.0885 - 8.8381 * x**2)
    elif x <= 0.546:
        return 1000 * (12.5815 - 1.2638*x - 3.6426*x**2 - 5.5281*x**3)
    elif x <= 0.895:
        return 1000 * (7.9565 - 6.4761*x + 5.5283*x**2 - 3.0807*x**3)
    elif x <= 0.937:
        return 1000 * (5.3197 - 1.4836*x)
    elif x <= 0.965:
        return 1000 * (11.2494 - 8.0298*x)
    elif x <= 0.996:
        return 1000 * 2.9
    else:
        return 1000 * 2.6

density = np.array([prem_density(min(s_i, 2*R_earth-s_i)/R_earth) for s_i in s])
s_km = s / 1e3

E_bind = 5.0 * 1.602e-19
m_atom = 25.0 * 1.661e-27
hbar = 1.055e-34

# Objects to compare
compare_objects = {
    "Iron meteorite (1t, 25 km/s)": {"mass": 1000, "radius": 0.34, "velocity": 25000, "color": "#e63946"},
    "Chondrite (10kg, 20 km/s)":    {"mass": 10,   "radius": 0.12, "velocity": 20000, "color": "#f4a261"},
    "UFO (10t, 0.9c)":              {"mass": 10000,"radius": 10.0, "velocity": 0.9*2.998e8, "color": "#7209b7"},
}

ax = axes[0]
for name, obj in compare_objects.items():
    A = np.pi * obj["radius"]**2
    V = (density / m_atom) * E_bind * A
    ax.semilogy(s_km, V, color=obj["color"], linewidth=2, label=name)

    # KE per unit length
    m = obj["mass"]
    v = obj["velocity"]
    beta = v / 2.998e8
    gamma = 1.0 / np.sqrt(1 - beta**2)
    KE = (gamma - 1) * m * (2.998e8)**2
    KE_per_L = KE / (2 * R_earth)
    ax.axhline(KE_per_L, color=obj["color"], linestyle='--', linewidth=1.5, alpha=0.7)

ax.set_xlabel("Distance along path (km)")
ax.set_ylabel("Potential barrier V(x) or KE/L (J/m)")
ax.set_title("Barrier V(x) vs Kinetic Energy/Length\n(solid = barrier, dashed = KE/L)")
ax.legend(fontsize=8)
ax.set_xlim(0, 2*R_earth/1e3)

# Shade layers
layer_boundaries_km = [0, 20, 670, 2891, 5150, 6371, 7901, 11521, 12371, 12742]
layer_names = ['Crust', 'Upper\nMantle', 'Lower\nMantle', 'Outer\nCore', 'Inner\nCore',
               'Inner\nCore', 'Outer\nCore', 'Lower\nMantle', 'Crust']
layer_colors = ['#8B7355', '#CD853F', '#8B4513', '#708090', '#C0C0C0',
                '#C0C0C0', '#708090', '#8B4513', '#8B7355']
for i in range(len(layer_names)):
    if i < len(layer_boundaries_km) - 1:
        ax.axvspan(layer_boundaries_km[i], layer_boundaries_km[i+1],
                   alpha=0.05, color=layer_colors[i])

# Panel B: κ(x) profile for meteorite vs UFO
ax = axes[1]
for name, obj in compare_objects.items():
    A = np.pi * obj["radius"]**2
    V = (density / m_atom) * E_bind * A
    m = obj["mass"]
    v = obj["velocity"]
    beta = v / 2.998e8
    gamma = 1.0 / np.sqrt(1 - beta**2)
    KE = (gamma - 1) * m * (2.998e8)**2
    KE_per_L = KE / (2 * R_earth)
    kappa = np.where(V > KE_per_L, np.sqrt(2 * m * (V - KE_per_L)) / hbar, 0)
    # Normalize for display
    kappa_norm = kappa / (kappa.max() + 1e-300)
    ax.plot(s_km, kappa_norm, color=obj["color"], linewidth=2, label=name)

ax.set_xlabel("Distance along path (km)")
ax.set_ylabel("Normalized κ(x) (WKB decay rate)")
ax.set_title("Normalized WKB Decay Constant κ(x)\nalong Earth Transit Path")
ax.legend(fontsize=8)
ax.set_xlim(0, 2*R_earth/1e3)

plt.tight_layout()
plt.savefig("/home/ubuntu/kraken_fig6_meteorite_wkb.png", bbox_inches='tight', dpi=150)
plt.close()
print("Figure 6 saved.")

print("\nAll figures saved successfully!")
