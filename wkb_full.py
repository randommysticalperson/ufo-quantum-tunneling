"""
UFO Quantum Tunneling Through Earth
Full WKB Approximation with Spatially Varying Potential V(x)

The Earth's density profile (PREM-based) is used to construct a
position-dependent potential barrier V(x). The WKB integral is
evaluated numerically across all layers.

WKB transmission coefficient:
    T = exp(-2 * Gamma)
    Gamma = integral_{x1}^{x2} kappa(x) dx
    kappa(x) = sqrt(2*M*(V(x) - E)) / hbar   [where V(x) > E]

V(x) = binding energy density * cross-section area * dx
     = n(x) * E_bind * A_ufo * dx

where n(x) = rho(x) / m_atom is the local atom number density.
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
from scipy import integrate

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'figure.dpi': 150,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# ── Physical constants ────────────────────────────────────────────────────────
hbar  = 1.0545718e-34    # J·s
h     = 6.62607015e-34   # J·s
c     = 2.99792458e8     # m/s
m_e   = 9.10938e-31      # kg
eV    = 1.60218e-19      # J
amu   = 1.66054e-27      # kg
G     = 6.674e-11        # m³/(kg·s²)
M_earth = 5.972e24       # kg
R_earth = 6.371e6        # m

# ── UFO parameters ────────────────────────────────────────────────────────────
M_ufo   = 1e4            # kg  — 10 metric tons
r_ufo   = 10.0           # m   — cross-section radius
A_ufo   = math.pi * r_ufo**2   # m²

# Average atomic binding energy (solid-state cohesive energy)
E_bind_per_atom = 5.0 * eV   # J

# Average atomic mass for Earth material (mix of Fe, Mg, Si, O)
m_atom_avg = 25.0 * amu      # kg

# ── PREM-based Earth density profile ─────────────────────────────────────────
# Each layer: (name, r_inner_km, r_outer_km, rho_kg_m3)
# Density is modeled as piecewise linear within each layer using PREM values.
# We use the full diameter path: x goes from 0 to 2*R_earth (entry to exit).

# PREM polynomial coefficients for density (kg/m³) as function of x = r/R_earth
# Source: Dziewonski & Anderson (1981), PREM model
# rho(x) = a0 + a1*x + a2*x^2 + a3*x^3  (x = r/R_earth, normalized radius)

# We define the path coordinate s ∈ [0, 2*R_earth]:
# s = 0 → entry at surface
# s = R_earth → Earth center
# s = 2*R_earth → exit at surface
# Radius from center: r(s) = |s - R_earth|

# PREM layer boundaries (in km from center) and density polynomials
# Coefficients from PREM (Dziewonski & Anderson 1981)
# rho in g/cm³, x = r/R_earth

prem_layers = [
    # (r_min_km, r_max_km, [a0, a1, a2, a3])  rho in g/cm³
    (0,    1221.5, [13.0885,  0.0,     -8.8381,  0.0    ]),  # inner core
    (1221.5, 3480, [12.5815, -1.2638,  -3.6426, -5.5281 ]),  # outer core
    (3480,  3630,  [7.9565,  -6.4761,   5.5283, -3.0807 ]),  # D'' layer
    (3630,  5600,  [7.9565,  -6.4761,   5.5283, -3.0807 ]),  # lower mantle
    (5600,  5701,  [5.3197,  -1.4836,   0.0,     0.0    ]),  # transition
    (5701,  5771,  [11.2494, -8.0298,   0.0,     0.0    ]),  # transition zone
    (5771,  5971,  [7.1089,  -3.8045,   0.0,     0.0    ]),  # transition zone
    (5971,  6151,  [2.6910,   0.6924,   0.0,     0.0    ]),  # upper mantle LVZ
    (6151,  6291,  [2.6910,   0.6924,   0.0,     0.0    ]),  # upper mantle
    (6291,  6346.6,[2.6910,   0.6924,   0.0,     0.0    ]),  # upper mantle
    (6346.6, 6356, [2.9000,   0.0,      0.0,     0.0    ]),  # lower crust
    (6356,  6368,  [2.6000,   0.0,      0.0,     0.0    ]),  # upper crust
    (6368,  6371,  [1.0200,   0.0,      0.0,     0.0    ]),  # ocean
]

def prem_density(r_km):
    """Return PREM density in kg/m³ at radius r_km from Earth center."""
    r_km = abs(r_km)
    r_km = min(r_km, 6371.0)
    x = r_km / 6371.0   # normalized radius
    for r_min, r_max, coeffs in prem_layers:
        if r_min <= r_km <= r_max:
            a0, a1, a2, a3 = coeffs
            rho_gcc = a0 + a1*x + a2*x**2 + a3*x**3
            return max(rho_gcc * 1000, 100)  # convert g/cm³ → kg/m³
    return 3300.0  # fallback

# ── Build high-resolution path array ─────────────────────────────────────────
N_points = 100000
s_arr = np.linspace(0, 2 * R_earth, N_points)   # path coordinate (m)
ds    = s_arr[1] - s_arr[0]

# Radius from Earth center at each path point
r_arr_m = np.abs(s_arr - R_earth)
r_arr_km = r_arr_m / 1000.0

# Density profile along path
rho_arr = np.array([prem_density(r) for r in r_arr_km])

# Atom number density along path
n_arr = rho_arr / m_atom_avg   # atoms/m³

# Potential energy density (J/m³)
V_density_arr = n_arr * E_bind_per_atom   # J/m³

# Potential energy per unit path length for the UFO cross-section (J/m)
V_per_m_arr = V_density_arr * A_ufo   # J/m

# Cumulative potential V(s) = integral_0^s V_per_m ds'
# This is the total binding energy the UFO must overcome up to position s.
# For WKB, we need V(x) - E at each point, where V(x) is the LOCAL potential
# height per unit length times ds (i.e., the barrier is distributed).

# For the WKB integral, the local "effective potential" is:
# V_eff(s) = V_per_m(s) * ds  (energy of one slice)
# But for the WKB kappa, we need V(x) in energy units at position x.
# 
# Correct interpretation: The potential barrier at position s is
# V(s) = V_per_m(s) * L_eff, where L_eff is a characteristic length.
# 
# More rigorously: We treat the Earth as a sequence of thin slabs.
# Each slab of thickness ds has potential V_slab = V_per_m * ds.
# The WKB decay exponent contribution from slab i is:
#   d_Gamma_i = sqrt(2*M*(V_slab_i / ds - E/L)) * ds / hbar
# where E/L is the kinetic energy per unit length.
#
# The correct WKB approach for a distributed barrier:
# The total barrier is V0 = integral V_per_m ds (total energy)
# kappa(s) = sqrt(2*M*(V_per_m(s)*L - E_k)) / (hbar * sqrt(L))
# ... but this is only valid for uniform barriers.
#
# PROPER WKB for spatially varying barrier:
# We treat V(x) as the cumulative potential energy seen by the particle
# as it moves through position x. The Schrödinger equation gives:
#
#   -hbar²/(2M) * d²psi/dx² + V(x)*psi = E*psi
#
# where V(x) is the potential energy at position x.
# 
# For our case: V(x) = V_per_m(x) * (some length scale)
# The natural choice is V(x) = V_per_m(x) * lambda_dB(x)
# But the cleanest approach is to define:
#
#   V(x) [J] = (binding energy per unit volume) * (UFO volume per unit length)
#             = V_density(x) * A_ufo   [J/m] * 1m = V_per_m(x)  [J/m]
#
# This gives V(x) in J/m, not J. To get J, multiply by a length scale.
# The physically correct barrier height at position x is:
#   V(x) = V_per_m(x) * lambda_dB   (energy to displace one de Broglie wavelength of material)
#
# However, for macroscopic objects, the cleanest formulation is:
# The WKB exponent is:
#   Gamma = (1/hbar) * integral sqrt(2*M*(V(x) - E(x))) dx
# where V(x) and E(x) are both in Joules at position x.
#
# We define V(x) as the potential energy the UFO sees at position x:
#   V(x) = V_per_m(x) * dx_ref
# where dx_ref = 1 m (unit path length).
# And E(x) = E_k / (2*R_earth) * 1 m (kinetic energy per unit path length * 1m)
# = E_k / (2*R_earth)
#
# This gives the correct dimensional WKB integral.

print("=" * 72)
print("FULL WKB APPROXIMATION — UFO TUNNELING THROUGH EARTH")
print("Spatially Varying Potential V(x) from PREM Density Profile")
print("=" * 72)

# ── WKB integral for multiple UFO velocities ──────────────────────────────────
velocities_pct = [0.001, 0.01, 0.05, 0.10, 0.30, 0.50, 0.70, 0.90, 0.99]

print(f"\n{'Velocity':>12} {'β':>8} {'γ':>8} {'E_k (J)':>14} {'Gamma':>20} {'log10(T)':>16} {'Regime':>20}")
print("-" * 105)

results = []

for v_pct in velocities_pct:
    beta  = v_pct
    gamma_v = 1.0 / math.sqrt(1.0 - beta**2)
    E_k   = (gamma_v - 1.0) * M_ufo * c**2

    # E per unit length (J/m): kinetic energy spread uniformly over path
    E_per_m = E_k / (2.0 * R_earth)

    # WKB integrand: kappa(s) = sqrt(2*M*(V_per_m(s) - E_per_m)) / hbar
    # Only integrate where V_per_m(s) > E_per_m (classically forbidden region)
    diff_arr = V_per_m_arr - E_per_m
    forbidden = diff_arr > 0

    if not np.any(forbidden):
        # Entire path is classically allowed — above barrier
        Gamma = 0.0
        log10_T = 0.0
        regime = "Above-barrier (classical)"
    else:
        kappa_arr = np.where(forbidden,
                             np.sqrt(2.0 * M_ufo * diff_arr) / hbar,
                             0.0)
        Gamma = np.trapezoid(kappa_arr, s_arr)
        log10_T = -2.0 * Gamma / math.log(10.0)
        regime = "Sub-barrier (tunneling)"

    results.append({
        'v_pct': v_pct,
        'beta': beta,
        'gamma': gamma_v,
        'E_k': E_k,
        'E_per_m': E_per_m,
        'Gamma': Gamma,
        'log10_T': log10_T,
        'regime': regime,
        'forbidden_fraction': np.sum(forbidden) / N_points,
    })

    print(f"  {v_pct*100:>8.3f}%c  {beta:>8.5f}  {gamma_v:>8.4f}  {E_k:>14.4e}  "
          f"{Gamma:>20.4e}  {log10_T:>16.4e}  {regime}")

# ── Find classical threshold velocity ────────────────────────────────────────
print("\n[Finding classical threshold velocity...]")
# At threshold: max(V_per_m) = E_per_m → E_k = max(V_per_m) * 2*R_earth
V_per_m_max = np.max(V_per_m_arr)
E_k_threshold = V_per_m_max * 2.0 * R_earth
# E_k = (gamma-1)*M*c^2 → gamma = E_k/(M*c^2) + 1
gamma_thresh = E_k_threshold / (M_ufo * c**2) + 1.0
beta_thresh  = math.sqrt(1.0 - 1.0/gamma_thresh**2)
print(f"  Max V(x)/m in Earth      : {V_per_m_max:.4e} J/m  (inner core)")
print(f"  E_k at threshold         : {E_k_threshold:.4e} J")
print(f"  Threshold velocity       : {beta_thresh*100:.4f}% c")
print(f"  Threshold gamma          : {gamma_thresh:.6f}")

# ── Detailed WKB at v=0.01c ───────────────────────────────────────────────────
print("\n[Detailed WKB at v = 0.01c]")
beta_d  = 0.01
gamma_d = 1.0 / math.sqrt(1.0 - beta_d**2)
E_k_d   = (gamma_d - 1.0) * M_ufo * c**2
E_per_m_d = E_k_d / (2.0 * R_earth)

diff_d = V_per_m_arr - E_per_m_d
kappa_d = np.where(diff_d > 0, np.sqrt(2.0 * M_ufo * diff_d) / hbar, 0.0)
Gamma_d = np.trapezoid(kappa_d, s_arr)
log10_T_d = -2.0 * Gamma_d / math.log(10.0)

print(f"  E_k                      : {E_k_d:.4e} J")
print(f"  E per unit length        : {E_per_m_d:.4e} J/m")
print(f"  Max kappa(x)             : {np.max(kappa_d):.4e} m⁻¹  (at inner core)")
print(f"  WKB integral Gamma       : {Gamma_d:.4e}")
print(f"  2*Gamma                  : {2*Gamma_d:.4e}")
print(f"  log10(T) = -2Gamma/ln10  : {log10_T_d:.4e}")
print(f"  T = 10^({log10_T_d:.4e})")

# Layer-by-layer breakdown of Gamma
print("\n  Layer-by-layer WKB contribution:")
layer_defs = [
    ("Crust",           6341e3, 6371e3),
    ("Upper Mantle",    5971e3, 6341e3),
    ("Transition Zone", 5701e3, 5971e3),
    ("Lower Mantle",    3481e3, 5701e3),
    ("Outer Core",      1221e3, 3481e3),
    ("Inner Core",      0,      1221e3),
]

print(f"  {'Layer':<22} {'Gamma_layer':>14} {'% of total':>12}")
print("  " + "-" * 52)
for name, r_in, r_out in layer_defs:
    # Both inbound and outbound halves
    mask1 = (r_arr_m >= r_in) & (r_arr_m <= r_out) & (s_arr <= R_earth)
    mask2 = (r_arr_m >= r_in) & (r_arr_m <= r_out) & (s_arr >  R_earth)
    G1 = np.trapezoid(kappa_d[mask1], s_arr[mask1]) if np.any(mask1) else 0
    G2 = np.trapezoid(kappa_d[mask2], s_arr[mask2]) if np.any(mask2) else 0
    G_layer = G1 + G2
    pct = G_layer / Gamma_d * 100 if Gamma_d > 0 else 0
    print(f"  {name:<22} {G_layer:>14.4e} {pct:>11.2f}%")

# ── WKB for single electron reference ────────────────────────────────────────
print("\n[Reference: Single electron, 1 nm barrier, 1 eV]")
kappa_e = math.sqrt(2 * m_e * 1 * eV) / hbar
L_e     = 1e-9
Gamma_e = kappa_e * L_e
T_e     = math.exp(-2 * Gamma_e)
print(f"  kappa_e = {kappa_e:.4e} m⁻¹")
print(f"  Gamma_e = {Gamma_e:.4f}")
print(f"  T_e     = {T_e:.4e}  (measurable!)")

# ═══════════════════════════════════════════════════════════════════════════════
# PLOTS
# ═══════════════════════════════════════════════════════════════════════════════

# ── Plot 1: V(x) profile and kappa(x) along path ─────────────────────────────
fig, axes = plt.subplots(3, 1, figsize=(11, 13))
fig.suptitle('WKB Analysis: UFO Quantum Tunneling Through Earth\n'
             'Spatially Varying Potential from PREM Density Profile',
             fontsize=14, fontweight='bold', y=0.98)

s_km = s_arr / 1000.0

# Subplot 1: Density profile
ax1 = axes[0]
ax1.fill_between(s_km, rho_arr / 1000, alpha=0.6, color='#E07020')
ax1.plot(s_km, rho_arr / 1000, color='#C05000', lw=1.5)
ax1.axvline(R_earth/1000, color='white', lw=1.5, ls='--', alpha=0.8, label='Earth center')

# Layer shading
layer_colors = ['#A0522D','#4682B4','#8FBC8F','#DAA520','#FF8C00','#FF4500']
layer_names_short = ['Crust','U.Mantle','Trans.','L.Mantle','Outer Core','Inner Core']
layer_r_bounds = [6371,6341,5971,5701,3481,1221,0]
for i in range(6):
    r_out_km = layer_r_bounds[i]
    r_in_km  = layer_r_bounds[i+1]
    # Inbound half
    s_in1 = (R_earth - r_out_km*1000) / 1000
    s_in2 = (R_earth - r_in_km*1000)  / 1000
    # Outbound half
    s_out1 = (R_earth + r_in_km*1000)  / 1000
    s_out2 = (R_earth + r_out_km*1000) / 1000
    for s1, s2 in [(s_in1, s_in2), (s_out1, s_out2)]:
        ax1.axvspan(s1, s2, alpha=0.12, color=layer_colors[i])

ax1.set_ylabel('Density (g/cm³)')
ax1.set_title('Earth Density Profile Along UFO Path (PREM)')
ax1.legend(fontsize=9)
ax1.set_xlim(0, 2*R_earth/1000)
ax1.grid(True, alpha=0.3)

# Subplot 2: V(x) per unit length vs E_per_m for different velocities
ax2 = axes[1]
ax2.semilogy(s_km, V_per_m_arr, color='#E07020', lw=2, label='$V(x)$ — barrier per unit length')

vel_colors = ['#9B59B6','#3498DB','#2ECC71','#E74C3C','#F39C12']
vel_labels_plot = ['v = 0.01c', 'v = 0.10c', 'v = 0.50c', 'v = 0.90c', 'v = 0.99c']
vel_betas_plot  = [0.01, 0.10, 0.50, 0.90, 0.99]

for beta_p, col, lbl in zip(vel_betas_plot, vel_colors, vel_labels_plot):
    gamma_p = 1.0 / math.sqrt(1.0 - beta_p**2)
    E_k_p   = (gamma_p - 1.0) * M_ufo * c**2
    E_per_m_p = E_k_p / (2.0 * R_earth)
    ax2.axhline(E_per_m_p, color=col, lw=1.5, ls='--', alpha=0.85, label=f'$E/L$ at {lbl}')

ax2.set_ylabel('Energy per unit length (J/m)')
ax2.set_title('Barrier $V(x)$ vs. Kinetic Energy per Unit Length for Various Velocities')
ax2.legend(fontsize=8, loc='lower center', ncol=3)
ax2.set_xlim(0, 2*R_earth/1000)
ax2.grid(True, alpha=0.3)

# Subplot 3: kappa(x) at v=0.01c
ax3 = axes[2]
ax3.semilogy(s_km, np.where(kappa_d > 0, kappa_d, np.nan),
             color='crimson', lw=2, label='$\\kappa(x)$ at $v = 0.01c$')
ax3.fill_between(s_km, np.where(kappa_d > 0, kappa_d, np.nan),
                 alpha=0.25, color='crimson')
ax3.axvline(R_earth/1000, color='gray', lw=1.5, ls='--', alpha=0.7, label='Earth center')
ax3.set_xlabel('Path Coordinate $s$ (km from entry surface)')
ax3.set_ylabel('$\\kappa(x)$ (m$^{-1}$)')
ax3.set_title('WKB Decay Constant $\\kappa(x) = \\sqrt{2M(V(x)-E_k/L)}/\\hbar$ at $v=0.01c$')
ax3.legend(fontsize=9)
ax3.set_xlim(0, 2*R_earth/1000)
ax3.grid(True, alpha=0.3)

# Add layer labels to bottom plot
for i in range(6):
    r_out_km = layer_r_bounds[i]
    r_in_km  = layer_r_bounds[i+1]
    s_mid = R_earth/1000 - (r_out_km + r_in_km)/2
    if i < 5:
        ax3.text(s_mid, ax3.get_ylim()[0] * 3, layer_names_short[i],
                 ha='center', fontsize=7, color='gray', rotation=90)

plt.tight_layout(rect=[0, 0, 1, 0.97])
fig.savefig('/home/ubuntu/wkb_fig1_potential_profile.png', bbox_inches='tight')
plt.close(fig)
print("\nFigure 1 (potential profile) saved.")

# ── Plot 2: log10(T) vs velocity ──────────────────────────────────────────────
fig2, ax_t = plt.subplots(figsize=(10, 5))

betas_fine = np.linspace(0.0001, 0.9999, 3000)
log10_T_fine = []
regime_fine  = []

for beta_f in betas_fine:
    gamma_f = 1.0 / math.sqrt(1.0 - beta_f**2)
    E_k_f   = (gamma_f - 1.0) * M_ufo * c**2
    E_per_m_f = E_k_f / (2.0 * R_earth)
    diff_f  = V_per_m_arr - E_per_m_f
    forbidden_f = diff_f > 0
    if not np.any(forbidden_f):
        log10_T_fine.append(0.0)
        regime_fine.append('above')
    else:
        kappa_f = np.where(forbidden_f, np.sqrt(2.0 * M_ufo * diff_f) / hbar, 0.0)
        Gamma_f = np.trapezoid(kappa_f, s_arr)
        log10_T_fine.append(-2.0 * Gamma_f / math.log(10.0))
        regime_fine.append('below')

log10_T_fine = np.array(log10_T_fine)
regime_fine  = np.array(regime_fine)

mask_below = regime_fine == 'below'
mask_above = regime_fine == 'above'

ax_t.fill_between(betas_fine[mask_below]*100, log10_T_fine[mask_below], 0,
                  alpha=0.25, color='crimson', label='Sub-barrier: quantum tunneling required')
ax_t.plot(betas_fine[mask_below]*100, log10_T_fine[mask_below],
          color='crimson', lw=2.5)

if mask_above.any():
    thresh_v = betas_fine[mask_above][0] * 100
    ax_t.axvline(thresh_v, color='goldenrod', lw=2.5, ls='--',
                 label=f'Classical threshold ≈ {thresh_v:.2f}% c')
    ax_t.axvspan(thresh_v, 100, alpha=0.15, color='limegreen',
                 label='Above-barrier: classical penetration (T ≈ 1)')

# Mark our primary scenario
ax_t.axvline(90, color='cyan', lw=2, ls=':', label='Primary scenario: v = 90% c')

ax_t.set_xlabel('UFO Velocity (% of $c$)')
ax_t.set_ylabel('$\\log_{10}(T)$ — WKB Transmission Exponent')
ax_t.set_title('WKB Tunneling Probability vs. UFO Velocity\n'
               '(10,000 kg craft, PREM spatially varying barrier, full Earth diameter)')
ax_t.legend(fontsize=9, loc='lower right')
ax_t.set_xlim(0, 100)
ax_t.grid(True, alpha=0.3)

# Annotate the impossibility at v=0.01c
idx_001 = np.argmin(np.abs(betas_fine - 0.01))
ax_t.annotate(
    f'$v=1\\%c$:\n$T = 10^{{{log10_T_fine[idx_001]:.1e}}}$\n(Physically impossible)',
    xy=(1.0, log10_T_fine[idx_001]),
    xytext=(12, log10_T_fine[idx_001]*0.55),
    arrowprops=dict(arrowstyle='->', color='black', lw=1.2),
    fontsize=9, color='crimson',
    bbox=dict(boxstyle='round,pad=0.3', fc='#fff0f0', alpha=0.8)
)

plt.tight_layout()
fig2.savefig('/home/ubuntu/wkb_fig2_transmission.png', bbox_inches='tight')
plt.close(fig2)
print("Figure 2 (transmission probability) saved.")

# ── Plot 3: WKB integrand kappa(x) for multiple velocities ───────────────────
fig3, axes3 = plt.subplots(2, 1, figsize=(11, 9))

vel_showcase = [0.01, 0.30, 0.50, 0.70]
colors3 = ['#E74C3C','#E67E22','#2ECC71','#3498DB']

ax3a = axes3[0]
ax3b = axes3[1]

for beta_s, col, lbl in zip(vel_showcase,
                             colors3,
                             ['v=1%c','v=30%c','v=50%c','v=70%c']):
    gamma_s = 1.0 / math.sqrt(1.0 - beta_s**2)
    E_k_s   = (gamma_s - 1.0) * M_ufo * c**2
    E_per_m_s = E_k_s / (2.0 * R_earth)
    diff_s  = V_per_m_arr - E_per_m_s
    kappa_s = np.where(diff_s > 0, np.sqrt(2.0 * M_ufo * diff_s) / hbar, 0.0)
    Gamma_s = np.trapezoid(kappa_s, s_arr)
    log10_s = -2.0 * Gamma_s / math.log(10.0)

    ax3a.plot(s_km, kappa_s, color=col, lw=1.8,
              label=f'{lbl}: $\\Gamma={Gamma_s:.2e}$, $\\log_{{10}}T={log10_s:.2e}$')
    ax3b.fill_between(s_km, np.cumsum(kappa_s)*ds, alpha=0.35, color=col)
    ax3b.plot(s_km, np.cumsum(kappa_s)*ds, color=col, lw=1.8, label=lbl)

ax3a.set_ylabel('$\\kappa(x)$ (m$^{-1}$)')
ax3a.set_title('WKB Decay Constant $\\kappa(x)$ Along Path for Sub-Barrier Velocities')
ax3a.legend(fontsize=8)
ax3a.set_xlim(0, 2*R_earth/1000)
ax3a.grid(True, alpha=0.3)
ax3a.axvline(R_earth/1000, color='gray', lw=1, ls='--', alpha=0.5)

ax3b.set_xlabel('Path Coordinate $s$ (km)')
ax3b.set_ylabel('Cumulative $\\int_0^s \\kappa(x)\\,dx$')
ax3b.set_title('Cumulative WKB Integral $\\Gamma(s) = \\int_0^s \\kappa(x)\\,dx$')
ax3b.legend(fontsize=8)
ax3b.set_xlim(0, 2*R_earth/1000)
ax3b.grid(True, alpha=0.3)
ax3b.axvline(R_earth/1000, color='gray', lw=1, ls='--', alpha=0.5)

plt.tight_layout()
fig3.savefig('/home/ubuntu/wkb_fig3_kappa_profiles.png', bbox_inches='tight')
plt.close(fig3)
print("Figure 3 (kappa profiles) saved.")

# ── Plot 4: Layer-by-layer Gamma contribution ─────────────────────────────────
fig4, ax4 = plt.subplots(figsize=(10, 5))

layer_names_full = ['Crust','Upper\nMantle','Transition\nZone','Lower\nMantle','Outer\nCore','Inner\nCore']
layer_gammas = []
for name, r_in, r_out in layer_defs:
    mask1 = (r_arr_m >= r_in) & (r_arr_m <= r_out) & (s_arr <= R_earth)
    mask2 = (r_arr_m >= r_in) & (r_arr_m <= r_out) & (s_arr >  R_earth)
    G1 = np.trapezoid(kappa_d[mask1], s_arr[mask1]) if np.any(mask1) else 0
    G2 = np.trapezoid(kappa_d[mask2], s_arr[mask2]) if np.any(mask2) else 0
    layer_gammas.append(G1 + G2)

bars4 = ax4.bar(layer_names_full, layer_gammas,
                color=['#A0522D','#4682B4','#8FBC8F','#DAA520','#FF8C00','#FF4500'],
                edgecolor='white', lw=0.8)

for bar, val in zip(bars4, layer_gammas):
    pct = val / Gamma_d * 100
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.02,
             f'{pct:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

ax4.set_ylabel('WKB Integral Contribution $\\Gamma_{\\text{layer}}$')
ax4.set_title('Layer-by-Layer WKB Integral Contribution to Total $\\Gamma$\n'
              f'(v = 1% c, Total $\\Gamma = {Gamma_d:.3e}$, $\\log_{{10}}T = {log10_T_d:.3e}$)')
ax4.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
fig4.savefig('/home/ubuntu/wkb_fig4_layer_gamma.png', bbox_inches='tight')
plt.close(fig4)
print("Figure 4 (layer gamma) saved.")

print("\n" + "=" * 72)
print("ALL CALCULATIONS AND FIGURES COMPLETE")
print("=" * 72)
print(f"\nKey WKB Results Summary:")
print(f"  {'Velocity':<12} {'log10(T)':>18} {'Regime'}")
print("  " + "-" * 60)
for r in results:
    print(f"  {r['v_pct']*100:>8.3f}%c   {r['log10_T']:>18.4e}   {r['regime']}")
