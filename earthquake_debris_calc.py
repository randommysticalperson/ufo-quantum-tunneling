"""
Earthquake Generation: UFO vs Meteorite
+ Quantum Tunneling of Space Garbage (WKB)
All physics calculations for the analysis document.
"""

import numpy as np

print("=" * 70)
print("EARTHQUAKE: UFO vs METEORITE | SPACE GARBAGE WKB TUNNELING")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
c = 3.0e8          # m/s
hbar = 1.055e-34   # J·s
G = 6.674e-11      # m³/(kg·s²)
R_earth = 6.371e6  # m
M_earth = 5.972e24 # kg

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: SEISMIC ENERGY FROM UFO PASSAGE
# ─────────────────────────────────────────────────────────────────────────────
print("\n[1] UFO SEISMIC ENERGY")
print("-" * 50)

# UFO parameters
m_ufo = 1e4          # kg
v_ufo = 0.90 * c
beta = v_ufo / c
gamma_rel = 1 / np.sqrt(1 - beta**2)
KE_ufo = (gamma_rel - 1) * m_ufo * c**2  # J

# Energy deposited into Earth during transit
# Fraction of KE converted to seismic waves: ~1e-4 (like nuclear explosions)
# For a relativistic plasma channel, seismic coupling is higher: ~1e-2
seismic_efficiency_ufo = 1e-2
E_seismic_ufo = KE_ufo * seismic_efficiency_ufo

# Moment magnitude: Mw = (2/3) * log10(M0) - 6.07
# Seismic moment M0 ≈ E_seismic / (3e-5) [rough conversion]
M0_ufo = E_seismic_ufo / 3e-5
Mw_ufo = (2/3) * np.log10(M0_ufo) - 6.07

# Also use Gutenberg-Richter energy relation: log10(E) = 1.5*Ms + 4.8
# Solve for Ms: Ms = (log10(E_seismic) - 4.8) / 1.5
Ms_ufo = (np.log10(E_seismic_ufo) - 4.8) / 1.5

print(f"  UFO KE:                {KE_ufo:.3e} J")
print(f"  Seismic efficiency:    {seismic_efficiency_ufo*100:.1f}%")
print(f"  Seismic energy:        {E_seismic_ufo:.3e} J")
print(f"  Moment magnitude Mw:   {Mw_ufo:.2f}")
print(f"  Surface magnitude Ms:  {Ms_ufo:.2f}")

# Comparison: Great earthquakes
print(f"\n  Reference earthquakes:")
print(f"    Tohoku 2011:         Mw 9.1  (E ~ 2e17 J seismic)")
print(f"    Sumatra 2004:        Mw 9.2  (E ~ 4e17 J seismic)")
print(f"    Valdivia 1960:       Mw 9.5  (E ~ 1e18 J seismic)")
print(f"    UFO passage:         Mw {Mw_ufo:.1f}  (E ~ {E_seismic_ufo:.1e} J seismic)")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: SEISMIC ENERGY FROM METEORITE IMPACTS
# ─────────────────────────────────────────────────────────────────────────────
print("\n[2] METEORITE IMPACT SEISMIC ENERGY")
print("-" * 50)

# Meteorite catalog
meteorites = {
    "Chelyabinsk (2013)":    {"mass": 1.2e7,  "v": 19e3,  "type": "airburst"},
    "Tunguska (1908)":       {"mass": 1e8,    "v": 27e3,  "type": "airburst"},
    "Chicxulub (66 Ma)":     {"mass": 2.3e17, "v": 20e3,  "type": "impact"},
    "Barringer (50 ka)":     {"mass": 3e8,    "v": 12e3,  "type": "impact"},
    "Vredefort (2 Ga)":      {"mass": 1e16,   "v": 15e3,  "type": "impact"},
}

print(f"  {'Object':<25} {'KE (J)':>14} {'Seismic E (J)':>14} {'Mw':>6} {'Ms':>6}")
print(f"  {'-'*70}")

seismic_eff_impact = 1e-4   # 0.01% for airburst/surface impact
seismic_eff_deep   = 1e-3   # 0.1% for deep penetrating impactor

meteor_results = {}
for name, data in meteorites.items():
    KE = 0.5 * data["mass"] * data["v"]**2
    eff = seismic_eff_impact if data["type"] == "airburst" else seismic_eff_deep
    E_s = KE * eff
    M0 = E_s / 3e-5
    Mw = (2/3) * np.log10(M0) - 6.07
    Ms = (np.log10(E_s) - 4.8) / 1.5
    meteor_results[name] = {"KE": KE, "E_s": E_s, "Mw": Mw, "Ms": Ms}
    print(f"  {name:<25} {KE:>14.3e} {E_s:>14.3e} {Mw:>6.1f} {Ms:>6.1f}")

print(f"\n  UFO (0.90c):              {KE_ufo:>14.3e} {E_seismic_ufo:>14.3e} {Mw_ufo:>6.1f} {Ms_ufo:>6.1f}")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: SEISMIC SIGNATURE COMPARISON
# ─────────────────────────────────────────────────────────────────────────────
print("\n[3] SEISMIC SIGNATURE COMPARISON")
print("-" * 50)

# Key differences between UFO and meteorite seismic signatures
print("  UFO Seismic Signature:")
print("    - Linear source: energy deposited along 12,742 km path")
print("    - Duration: ~47 ms (transit time)")
print("    - Frequency: ultra-broadband (plasma channel collapse)")
print("    - P-wave: cylindrical wavefront from entire path")
print("    - No surface crater (passes through)")
print("    - Entry + exit shockwaves (two distinct events)")

print("\n  Meteorite Seismic Signature:")
print("    - Point source: energy deposited at impact/airburst point")
print("    - Duration: seconds to minutes (depending on size)")
print("    - Frequency: dominated by Rayleigh/Love surface waves")
print("    - P-wave: spherical wavefront from single point")
print("    - Surface crater (for impactors)")
print("    - Single event")

# Peak ground acceleration comparison
# PGA ~ (E_seismic / (2*pi*rho*v_s^2*r^2))^0.5 at distance r
rho_crust = 2700  # kg/m^3
v_s = 3500        # m/s (S-wave speed in crust)
r_dist = 1000e3   # 1000 km from source

print(f"\n  Peak Ground Acceleration at {r_dist/1e3:.0f} km:")
print(f"  {'Object':<25} {'PGA (g)':>10}")
print(f"  {'-'*40}")

for name, res in meteor_results.items():
    E_s = res["E_s"]
    PGA = np.sqrt(E_s / (2 * np.pi * rho_crust * v_s**2 * r_dist**2)) / 9.81
    print(f"  {name:<25} {PGA:>10.3e}")

PGA_ufo = np.sqrt(E_seismic_ufo / (2 * np.pi * rho_crust * v_s**2 * r_dist**2)) / 9.81
print(f"  {'UFO (0.90c)':<25} {PGA_ufo:>10.3e}")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: WKB TUNNELING OF SPACE GARBAGE
# ─────────────────────────────────────────────────────────────────────────────
print("\n[4] WKB QUANTUM TUNNELING OF SPACE GARBAGE")
print("-" * 50)

# Earth potential barrier (binding energy per unit length)
# Total gravitational binding energy of Earth: ~2.5e32 J
# Effective barrier over Earth diameter (12,742 km): V0 = E_bind / L
E_bind_earth = 2.5e32   # J (gravitational binding energy)
L_earth = 2 * R_earth   # m (Earth diameter)
V0_per_m = E_bind_earth / L_earth  # J/m (potential energy density)
V0_total = E_bind_earth  # J (total barrier)

print(f"  Earth gravitational binding energy: {E_bind_earth:.3e} J")
print(f"  Earth diameter (barrier width):     {L_earth/1e6:.3f} Mm")
print(f"  Effective barrier height V0:        {V0_total:.3e} J")

# Space garbage catalog
debris_objects = {
    "Paint fleck (0.1mm, 0.1μg)":  {"mass": 1e-10, "v": 7.8e3,  "desc": "Most common LEO debris"},
    "Paint chip (1mm, 1mg)":        {"mass": 1e-6,  "v": 7.8e3,  "desc": "Sandblasting threat"},
    "Bolt fragment (10g)":          {"mass": 1e-2,  "v": 7.8e3,  "desc": "Hypervelocity threat"},
    "Dead CubeSat (1kg)":           {"mass": 1.0,   "v": 7.8e3,  "desc": "Small satellite"},
    "Rocket stage (1 tonne)":       {"mass": 1e3,   "v": 7.8e3,  "desc": "Fengyun-1C debris"},
    "Dead satellite (10 tonnes)":   {"mass": 1e4,   "v": 7.8e3,  "desc": "Envisat-class"},
    "Chelyabinsk (12,000 t)":       {"mass": 1.2e7, "v": 19e3,   "desc": "Meteorite reference"},
    "Tunguska (100,000 t)":         {"mass": 1e8,   "v": 27e3,   "desc": "Meteorite reference"},
}

print(f"\n  WKB Tunneling Analysis (T = exp(-2*Gamma)):")
print(f"  {'Object':<35} {'Mass (kg)':>10} {'v (km/s)':>9} {'KE (J)':>12} {'log10(T)':>12} {'Classical?':>12}")
print(f"  {'-'*95}")

debris_results = {}
for name, data in debris_objects.items():
    m = data["mass"]
    v = data["v"]
    KE = 0.5 * m * v**2  # non-relativistic for LEO debris

    if KE >= V0_total:
        log10_T = 0
        classical = "YES (above barrier)"
        kappa_L = 0
    else:
        # WKB: kappa = sqrt(2*m*(V0-KE)) / hbar
        # Gamma = kappa * L (rectangular barrier approximation)
        kappa = np.sqrt(2 * m * (V0_total - KE)) / hbar
        Gamma = kappa * L_earth
        log10_T = -2 * Gamma / np.log(10)
        classical = "no"

    debris_results[name] = {"mass": m, "v": v, "KE": KE, "log10_T": log10_T}
    print(f"  {name:<35} {m:>10.2e} {v/1e3:>9.1f} {KE:>12.3e} {log10_T:>12.3e} {classical:>12}")

# Classical threshold velocity for each object
print(f"\n  Classical threshold velocities (v needed to punch through Earth):")
print(f"  {'Object':<35} {'Mass (kg)':>10} {'v_threshold (km/s)':>20} {'v_threshold / c':>16}")
print(f"  {'-'*85}")

for name, data in debris_objects.items():
    m = data["mass"]
    # KE = V0 => 0.5*m*v^2 = V0 => v = sqrt(2*V0/m)
    v_thresh = np.sqrt(2 * V0_total / m)
    v_thresh_c = v_thresh / c
    if v_thresh > c:
        v_thresh_str = f">c (impossible)"
        v_thresh_c_str = f">1.0"
    else:
        v_thresh_str = f"{v_thresh/1e3:.2f}"
        v_thresh_c_str = f"{v_thresh_c:.4f}"
    print(f"  {name:<35} {m:>10.2e} {v_thresh_str:>20} {v_thresh_c_str:>16}")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: COMPARISON TABLE
# ─────────────────────────────────────────────────────────────────────────────
print("\n[5] FINAL COMPARISON: UFO vs METEORITE EARTHQUAKE")
print("-" * 50)

print(f"""
  Property                    UFO (0.90c)          Chelyabinsk (2013)   Chicxulub (66 Ma)
  ─────────────────────────── ──────────────────── ──────────────────── ────────────────────
  Mass                        10,000 kg            12,000,000 kg        2.3e17 kg
  Velocity                    0.90c = 2.7e8 m/s    19 km/s              20 km/s
  Kinetic Energy              1.16e21 J            2.17e15 J            4.6e28 J
  Seismic Energy              1.16e19 J            2.17e11 J            4.6e25 J
  Moment Magnitude Mw         {Mw_ufo:.1f}                  ~5.0                 ~13.0
  Source Type                 Linear (12,742 km)   Point (airburst)     Point (surface)
  Duration                    47 ms                ~30 s                minutes
  Crater                      None (passes thru)   None (airburst)      180 km diameter
  Seismic Waves               Cylindrical P-wave   Spherical all modes  Spherical all modes
  Detectability               Global seismographs  Regional networks    Geological record
""")

print("\nAll calculations complete.")
