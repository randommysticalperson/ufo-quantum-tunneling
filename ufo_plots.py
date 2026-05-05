"""
UFO Quantum Tunneling Through Earth — Visualizations
Generates 5 publication-quality figures.
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Arc, Wedge
import matplotlib.gridspec as gridspec

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'figure.dpi': 150,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# ── Constants ─────────────────────────────────────────────────────────────────
hbar = 1.0545718e-34
h    = 6.62607015e-34
c    = 2.99792458e8
m_e  = 9.10938e-31
eV   = 1.60218e-19
M_ufo = 1e4
R_earth = 6.371e6
L_barrier = 2 * R_earth

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1: Tunneling Probability vs. UFO Velocity
# ══════════════════════════════════════════════════════════════════════════════
# V0 = 4.26e20 J (material barrier for full Earth diameter)
V0 = 4.26e20

velocities_frac = np.linspace(0.001, 0.999, 2000)
log10_T_vals = []

for beta in velocities_frac:
    gamma = 1 / math.sqrt(1 - beta**2)
    KE = (gamma - 1) * M_ufo * c**2
    if KE < V0:
        kappa = math.sqrt(2 * M_ufo * (V0 - KE)) / hbar
        log10_T = -2 * kappa * L_barrier / math.log(10)
        log10_T_vals.append(log10_T)
    else:
        log10_T_vals.append(0)  # above barrier: T ≈ 1

log10_T_arr = np.array(log10_T_vals)

fig1, ax1 = plt.subplots(figsize=(9, 5))

# Split into tunneling and above-barrier regions
mask_tunnel = log10_T_arr < 0
mask_above  = log10_T_arr == 0

# Find crossover velocity
crossover_beta = velocities_frac[np.where(mask_above)[0][0]] if mask_above.any() else None

ax1.fill_between(velocities_frac[mask_tunnel] * 100,
                 log10_T_arr[mask_tunnel], 0,
                 alpha=0.25, color='crimson', label='Sub-barrier (quantum tunneling)')
ax1.plot(velocities_frac[mask_tunnel] * 100,
         log10_T_arr[mask_tunnel],
         color='crimson', lw=2)

if crossover_beta is not None:
    ax1.axvline(crossover_beta * 100, color='goldenrod', lw=2, ls='--',
                label=f'Classical threshold: v ≈ {crossover_beta*100:.1f}% c')
    ax1.axvspan(crossover_beta * 100, 100, alpha=0.12, color='limegreen',
                label='Above-barrier (classical punch-through, T ≈ 1)')

ax1.set_xlabel('UFO Velocity (% of speed of light $c$)')
ax1.set_ylabel('$\\log_{10}(T)$ — Tunneling Probability Exponent')
ax1.set_title('WKB Tunneling Probability vs. UFO Velocity\n(10,000 kg craft, Earth-diameter barrier)')
ax1.legend(loc='lower right', fontsize=9)
ax1.set_xlim(0, 100)
ax1.set_ylim(log10_T_arr[mask_tunnel].min() * 1.05, 5)

# Annotate the impossibility
ax1.annotate(
    f'At v = 1% c:\nT = $10^{{-3 \\times 10^{{53}}}}$\n(Effectively zero)',
    xy=(1, log10_T_arr[0]), xytext=(15, log10_T_arr[0] * 0.5),
    arrowprops=dict(arrowstyle='->', color='black'),
    fontsize=9, color='crimson'
)

plt.tight_layout()
fig1.savefig('/home/ubuntu/fig1_tunneling_probability.png', bbox_inches='tight')
plt.close(fig1)
print("Figure 1 saved.")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2: Earth Cross-Section with UFO Path and Layer Labels
# ══════════════════════════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(8, 8))
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_xlim(-1.3, 1.3)
ax2.set_ylim(-1.3, 1.3)

# Layer radii (normalized to R_earth = 1)
layers_norm = [
    ("Inner Core",      1221/6371, '#FF4500'),
    ("Outer Core",      3481/6371, '#FF8C00'),
    ("Lower Mantle",    5701/6371, '#DAA520'),
    ("Transition Zone", 5971/6371, '#8FBC8F'),
    ("Upper Mantle",    6341/6371, '#4682B4'),
    ("Crust",           6371/6371, '#A0522D'),
]

for name, r, color in reversed(layers_norm):
    circle = plt.Circle((0, 0), r, color=color, ec='white', lw=0.5)
    ax2.add_patch(circle)

# Labels with lines
label_positions = [
    ("Inner Core",      0.12,  0.0,   0.55,  0.25),
    ("Outer Core",      0.35,  0.0,   0.65,  0.40),
    ("Lower Mantle",    0.72,  0.0,   0.85,  0.55),
    ("Transition Zone", 0.86,  0.0,   0.92,  0.65),
    ("Upper Mantle",    0.91,  0.0,   0.95,  0.75),
    ("Crust",           0.995, 0.0,   1.05,  0.85),
]
for name, x0, y0, xt, yt in label_positions:
    ax2.annotate(name, xy=(x0, y0), xytext=(xt, yt),
                 arrowprops=dict(arrowstyle='->', color='white', lw=1),
                 color='white', fontsize=8.5, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.2', fc='#111111', alpha=0.7))

# UFO path — straight vertical line through Earth
ax2.annotate('', xy=(0, -1.25), xytext=(0, 1.25),
             arrowprops=dict(arrowstyle='<->', color='cyan', lw=2.5))
ax2.text(0.07, 1.18, 'UFO Path\n(12,742 km)', color='cyan', fontsize=9,
         fontweight='bold')

# UFO icons (triangles)
ax2.plot(0, 1.22, marker='^', ms=14, color='cyan', zorder=10)
ax2.plot(0, -1.22, marker='v', ms=14, color='cyan', zorder=10)

# Cherenkov cone at entry (top)
cone_angle_deg = 40.44  # degrees from path direction
cone_angle_rad = math.radians(cone_angle_deg)
for sign in [-1, 1]:
    dx = sign * math.sin(cone_angle_rad) * 0.35
    dy = -math.cos(cone_angle_rad) * 0.35
    ax2.annotate('', xy=(0 + dx, 1.22 + dy), xytext=(0, 1.22),
                 arrowprops=dict(arrowstyle='->', color='yellow', lw=1.5))
ax2.text(0.42, 1.05, 'Cherenkov\ncone\n(40.4°)', color='yellow', fontsize=8)

ax2.set_title("UFO Straight-Through Path — Earth Cross-Section\n"
              "with Cherenkov Radiation Cone at Entry", color='white', fontsize=12, pad=10)
fig2.patch.set_facecolor('#0a0a1a')
ax2.set_facecolor('#0a0a1a')
plt.tight_layout()
fig2.savefig('/home/ubuntu/fig2_earth_crosssection.png', bbox_inches='tight',
             facecolor='#0a0a1a')
plt.close(fig2)
print("Figure 2 saved.")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3: Cherenkov Angle vs. UFO Velocity for Sand and Water
# ══════════════════════════════════════════════════════════════════════════════
n_sand  = 1.46
n_water = 1.34

betas = np.linspace(0.001, 0.9999, 5000)
theta_sand_arr  = []
theta_water_arr = []

for beta in betas:
    cos_s = 1 / (n_sand  * beta)
    cos_w = 1 / (n_water * beta)
    theta_sand_arr.append(math.degrees(math.acos(min(1.0, cos_s)))  if cos_s <= 1 else float('nan'))
    theta_water_arr.append(math.degrees(math.acos(min(1.0, cos_w))) if cos_w <= 1 else float('nan'))

theta_sand_arr  = np.array(theta_sand_arr,  dtype=float)
theta_water_arr = np.array(theta_water_arr, dtype=float)

fig3, ax3 = plt.subplots(figsize=(9, 5))
ax3.plot(betas * 100, theta_sand_arr,  color='#E8A020', lw=2.5, label='Desert Sand (SiO₂, $n=1.46$)')
ax3.plot(betas * 100, theta_water_arr, color='#2080E8', lw=2.5, label='Ocean Water ($n=1.34$)')

# Threshold lines
thresh_sand  = 1/n_sand  * 100
thresh_water = 1/n_water * 100
ax3.axvline(thresh_sand,  color='#E8A020', ls=':', lw=1.5, alpha=0.7,
            label=f'Sand threshold: {thresh_sand:.1f}% c')
ax3.axvline(thresh_water, color='#2080E8', ls=':', lw=1.5, alpha=0.7,
            label=f'Water threshold: {thresh_water:.1f}% c')

# Mark our UFO velocity
ufo_v = 90.0
ax3.axvline(ufo_v, color='cyan', ls='--', lw=2, label='UFO velocity: 90% c')
ax3.plot(ufo_v, 40.44, 'o', ms=10, color='#E8A020', zorder=5)
ax3.plot(ufo_v, 33.98, 'o', ms=10, color='#2080E8', zorder=5)
ax3.annotate('40.4°', xy=(ufo_v, 40.44), xytext=(ufo_v+3, 44),
             arrowprops=dict(arrowstyle='->', color='gray'), fontsize=9)
ax3.annotate('34.0°', xy=(ufo_v, 33.98), xytext=(ufo_v+3, 30),
             arrowprops=dict(arrowstyle='->', color='gray'), fontsize=9)

ax3.set_xlabel('UFO Velocity (% of $c$)')
ax3.set_ylabel('Cherenkov Emission Angle $\\theta$ (degrees)')
ax3.set_title('Cherenkov Radiation Angle vs. UFO Velocity\nin Desert Sand and Ocean Water')
ax3.legend(fontsize=9)
ax3.set_xlim(0, 100)
ax3.set_ylim(0, 95)
ax3.grid(True, alpha=0.3)
plt.tight_layout()
fig3.savefig('/home/ubuntu/fig3_cherenkov_angle.png', bbox_inches='tight')
plt.close(fig3)
print("Figure 3 saved.")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4: Multi-Scenario Comparison — KE vs. Barrier for Different Masses
# ══════════════════════════════════════════════════════════════════════════════
masses_kg = [1e-3, 1e0, 1e2, 1e4, 1e6]
mass_labels = ['1 g', '1 kg', '100 kg', '10,000 kg\n(our UFO)', '1,000 t']
velocities_scenario = [0.01, 0.10, 0.50, 0.90, 0.999]
vel_labels = ['1% c', '10% c', '50% c', '90% c', '99.9% c']

# For each mass, compute KE at each velocity
# V0 scales with mass (cross-section ~ r^2 ~ m^(2/3) for constant density)
# Assume V0 ∝ M^(2/3) * L (barrier scales with cross-section)
V0_base = 4.26e20   # for 10,000 kg (r=10m)
M_base  = 1e4

fig4, axes4 = plt.subplots(1, 2, figsize=(13, 5))

# Left: KE vs velocity for each mass
ax4a = axes4[0]
colors4 = ['#9B59B6', '#3498DB', '#2ECC71', '#E74C3C', '#F39C12']
for i, (M, label, col) in enumerate(zip(masses_kg, mass_labels, colors4)):
    betas_plot = np.linspace(0.001, 0.9999, 500)
    KEs = []
    for beta in betas_plot:
        gamma = 1 / math.sqrt(1 - beta**2)
        KEs.append((gamma - 1) * M * c**2)
    ax4a.semilogy(betas_plot * 100, KEs, color=col, lw=2, label=label.replace('\n', ' '))

# V0 line for 10,000 kg
ax4a.axhline(V0_base, color='#E74C3C', ls='--', lw=2, alpha=0.6, label='$V_0$ (10,000 kg UFO)')
ax4a.set_xlabel('Velocity (% of $c$)')
ax4a.set_ylabel('Kinetic Energy (J)')
ax4a.set_title('Relativistic Kinetic Energy vs. Velocity\nfor Different UFO Masses')
ax4a.legend(fontsize=8, loc='upper left')
ax4a.grid(True, alpha=0.3)
ax4a.set_xlim(0, 100)

# Right: Barrier vs KE bar chart for our UFO at different velocities
ax4b = axes4[1]
KEs_bar = []
for beta in [b/100 for b in [1, 10, 50, 90, 99]]:
    gamma = 1 / math.sqrt(1 - beta**2)
    KEs_bar.append((gamma - 1) * M_ufo * c**2)

x_pos = np.arange(len(vel_labels))
bar_colors = ['#E74C3C' if ke < V0_base else '#2ECC71' for ke in KEs_bar]
bars = ax4b.bar(x_pos, [math.log10(ke) for ke in KEs_bar],
                color=bar_colors, edgecolor='white', lw=0.8, width=0.6)
ax4b.axhline(math.log10(V0_base), color='goldenrod', lw=2.5, ls='--',
             label=f'Material Barrier $V_0$ = $10^{{{math.log10(V0_base):.1f}}}$ J')
ax4b.set_xticks(x_pos)
ax4b.set_xticklabels(vel_labels, fontsize=9)
ax4b.set_ylabel('$\\log_{10}$(Kinetic Energy) [J]')
ax4b.set_title('UFO Kinetic Energy vs. Barrier\n(10,000 kg craft at various velocities)')
ax4b.legend(fontsize=9)

red_patch  = mpatches.Patch(color='#E74C3C', label='Sub-barrier (tunneling required)')
green_patch = mpatches.Patch(color='#2ECC71', label='Above-barrier (classical)')
ax4b.legend(handles=[red_patch, green_patch,
                     mpatches.Patch(color='goldenrod', label='Material Barrier $V_0$')],
            fontsize=8, loc='upper left')
ax4b.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
fig4.savefig('/home/ubuntu/fig4_scenarios.png', bbox_inches='tight')
plt.close(fig4)
print("Figure 4 saved.")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 5: Energy Deposition Profile Through Earth Layers
# ══════════════════════════════════════════════════════════════════════════════
# Bethe-Bloch dE/dx for each layer (simplified, using layer density)
K_bethe = 0.307075e6 * eV * 1e-4  # J·m²/kg
beta_ufo  = 0.90
gamma_ufo = 1 / math.sqrt(1 - beta_ufo**2)
Z_eff = 1e6
I_avg = 100 * eV  # average mean excitation energy

layers_plot = [
    ("Crust",           30,   2800),
    ("Upper Mantle",    370,  3400),
    ("Trans. Zone",     270,  3700),
    ("Lower Mantle",    2220, 4900),
    ("Outer Core",      2260, 11000),
    ("Inner Core",      1221, 13000),
    ("Lower Mantle*",   2220, 4900),
    ("Trans. Zone*",    270,  3700),
    ("Upper Mantle*",   370,  3400),
    ("Crust*",          30,   2800),
]

ZA_avg = 0.50
Tmax = 2 * m_e * c**2 * beta_ufo**2 * gamma_ufo**2

dEdx_layers = []
for name, thick, rho in layers_plot:
    log_term = 0.5 * math.log(2 * m_e * c**2 * beta_ufo**2 * gamma_ufo**2 * Tmax / I_avg**2)
    dEdx = K_bethe * Z_eff**2 * ZA_avg * rho / beta_ufo**2 * (log_term - beta_ufo**2)
    dEdx_layers.append(dEdx)

depths = []
d = 0
for name, thick, rho in layers_plot:
    depths.append(d + thick / 2)
    d += thick
total_depth = d

layer_colors_plot = [
    '#A0522D', '#4682B4', '#8FBC8F', '#DAA520',
    '#FF8C00', '#FF4500',
    '#DAA520', '#8FBC8F', '#4682B4', '#A0522D'
]

fig5, ax5 = plt.subplots(figsize=(11, 5))
x_centers = np.array(depths)
widths = [t for _, t, _ in layers_plot]

bars5 = ax5.bar(x_centers, dEdx_layers, width=widths,
                color=layer_colors_plot, edgecolor='white', lw=0.5, alpha=0.85)

# Layer boundary lines
d2 = 0
for i, (name, thick, rho) in enumerate(layers_plot):
    ax5.axvline(d2, color='gray', lw=0.5, ls=':')
    d2 += thick
ax5.axvline(total_depth / 2, color='white', lw=2, ls='--', alpha=0.5, label='Earth center')

ax5.set_xlabel('Depth Along Path (km)')
ax5.set_ylabel('Energy Loss $-dE/dx$ (J/m)')
ax5.set_title('Bethe-Bloch Ionization Energy Loss Profile\nThrough Earth Layers (UFO at 0.90c, $Z_{eff}=10^6$)')
ax5.set_xlim(0, total_depth)

# Custom legend for layers
unique_layers = [
    mpatches.Patch(color='#A0522D', label='Crust'),
    mpatches.Patch(color='#4682B4', label='Upper Mantle'),
    mpatches.Patch(color='#8FBC8F', label='Transition Zone'),
    mpatches.Patch(color='#DAA520', label='Lower Mantle'),
    mpatches.Patch(color='#FF8C00', label='Outer Core'),
    mpatches.Patch(color='#FF4500', label='Inner Core'),
]
ax5.legend(handles=unique_layers, fontsize=8, loc='upper right', ncol=2)
ax5.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
fig5.savefig('/home/ubuntu/fig5_energy_deposition.png', bbox_inches='tight')
plt.close(fig5)
print("Figure 5 saved.")

print("\nAll 5 figures saved successfully.")
