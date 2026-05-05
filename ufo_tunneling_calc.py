"""
UFO Quantum Tunneling Through Earth - Mathematical Calculations
All values in SI units unless otherwise noted.
"""

import math

print("=" * 70)
print("UFO QUANTUM TUNNELING THROUGH EARTH — FULL CALCULATIONS")
print("=" * 70)

# ─────────────────────────────────────────────────────────────
# SECTION 0: PHYSICAL CONSTANTS
# ─────────────────────────────────────────────────────────────
hbar = 1.0545718e-34       # J·s  (reduced Planck constant)
h    = 6.62607015e-34      # J·s  (Planck constant)
c    = 2.99792458e8        # m/s  (speed of light)
m_e  = 9.10938e-31         # kg   (electron mass)
m_p  = 1.67262e-27         # kg   (proton mass)
k_B  = 1.380649e-23        # J/K  (Boltzmann constant)
e_c  = 1.60218e-19         # C    (elementary charge)
eps0 = 8.854187817e-12     # F/m  (vacuum permittivity)
G    = 6.674e-11           # m³/(kg·s²)
eV   = 1.60218e-19         # J per eV

print("\n[SECTION 0] Physical Constants loaded.")

# ─────────────────────────────────────────────────────────────
# SECTION 1: UFO PARAMETERS (HYPOTHETICAL)
# ─────────────────────────────────────────────────────────────
# We model the UFO as a macroscopic object of mass M_ufo.
# For the quantum tunneling calculation, we treat it as a single
# quantum entity (a gross simplification, but physically instructive).

M_ufo    = 1e4             # kg  — 10 metric tons (plausible craft mass)
v_ufo    = 0.90 * c        # m/s — 90% speed of light (highly relativistic entry)
# Relativistic kinetic energy: KE = (gamma - 1) * M * c^2
beta_ufo = v_ufo / c
gamma_ufo = 1 / math.sqrt(1 - beta_ufo**2)
KE_ufo   = (gamma_ufo - 1) * M_ufo * c**2   # J  — relativistic kinetic energy

print("\n[SECTION 1] UFO Parameters")
print(f"  Mass of UFO            : {M_ufo:.2e} kg  ({M_ufo/1000:.0f} metric tons)")
print(f"  Entry velocity         : {v_ufo:.4e} m/s  ({v_ufo/c*100:.0f}% c)")
print(f"  Classical kinetic energy: {KE_ufo:.4e} J  ({KE_ufo/eV:.4e} eV)")

# de Broglie wavelength  λ = h / (M·v)
lambda_dB = h / (M_ufo * v_ufo)
print(f"\n  de Broglie wavelength  : λ = h/(Mv) = {lambda_dB:.4e} m")
print(f"  (For comparison, proton diameter ~ 1.7e-15 m)")

# ─────────────────────────────────────────────────────────────
# SECTION 2: EARTH LAYER DATA (PREM model)
# ─────────────────────────────────────────────────────────────
# Layers: [name, outer_radius_km, inner_radius_km, avg_density_kg/m3,
#          avg_pressure_GPa, avg_temp_K]
R_earth = 6.371e6   # m

layers = [
    # name,            r_outer(m),  r_inner(m),  rho(kg/m3), P(GPa), T(K)
    ("Continental Crust",  6.371e6, 6.341e6,  2800,    0.0005,  300),
    ("Upper Mantle",       6.341e6, 5.971e6,  3400,    3.0,     1600),
    ("Transition Zone",    5.971e6, 5.701e6,  3700,    13.0,    1900),
    ("Lower Mantle",       5.701e6, 3.481e6,  4900,    75.0,    3000),
    ("Outer Core",         3.481e6, 1.221e6,  11000,   135.0,   5000),
    ("Inner Core",         1.221e6, 0.0,      13000,   360.0,   6000),
]

print("\n[SECTION 2] Earth Layer Properties (PREM-based)")
print(f"{'Layer':<22} {'Thickness(km)':>14} {'Density(kg/m³)':>16} {'Pressure(GPa)':>14} {'Temp(K)':>9}")
print("-" * 80)
for name, r_out, r_in, rho, P, T in layers:
    thickness_km = (r_out - r_in) / 1000
    print(f"  {name:<20} {thickness_km:>14.0f} {rho:>16} {P:>14.2f} {T:>9}")

total_diameter = 2 * R_earth / 1000
print(f"\n  Total Earth diameter   : {total_diameter:.1f} km = {2*R_earth:.4e} m")

# ─────────────────────────────────────────────────────────────
# SECTION 3: POTENTIAL BARRIER — GRAVITATIONAL + MATERIAL
# ─────────────────────────────────────────────────────────────
# The "barrier" for quantum tunneling is the potential energy the UFO
# must overcome. We compute the gravitational potential energy
# difference (binding energy) and the material compression energy.

# Gravitational potential energy at surface vs center
# U_grav = -3GM²/(5R) for uniform sphere (self-energy)
# For the UFO tunneling through, the relevant barrier is the
# gravitational binding energy of the Earth acting on the UFO:
# V_grav(r) = -G * M_earth * M_ufo / r  (potential at radius r)
# The barrier height is the difference between V at surface and V at center.

M_earth = 5.972e24   # kg
V_surface = -G * M_earth * M_ufo / R_earth
# At center of uniform sphere: V_center = -3/2 * G*M_earth*M_ufo/R_earth
V_center  = -1.5 * G * M_earth * M_ufo / R_earth
delta_V_grav = V_center - V_surface   # This is negative (deeper well)
# The barrier the UFO must tunnel THROUGH is the material barrier.
# We model the Earth as a rectangular potential barrier of height V0
# above the UFO's kinetic energy.

# Estimate material barrier: binding energy of Earth's atoms per unit volume
# Average atomic binding energy ~ 5 eV per atom
# Average atomic mass ~ 25 amu (mix of Fe, Mg, Si, O)
amu = 1.66054e-27   # kg
avg_atomic_mass = 25 * amu
avg_density_earth = 5515   # kg/m3
n_atoms = avg_density_earth / avg_atomic_mass   # atoms/m3
E_bind_per_atom = 5 * eV   # J
V0_material_per_m3 = n_atoms * E_bind_per_atom  # J/m3

# Total material barrier energy for UFO of cross-section A_ufo
# Assume UFO is a disk of radius 10 m
r_ufo = 10.0   # m
A_ufo = math.pi * r_ufo**2
L_barrier = 2 * R_earth   # m — full diameter of Earth

# Total potential barrier energy
V0_total = V0_material_per_m3 * A_ufo * L_barrier
print("\n[SECTION 3] Potential Barrier Estimation")
print(f"  Atom number density    : {n_atoms:.3e} atoms/m³")
print(f"  Binding energy/atom    : 5 eV = {5*eV:.3e} J")
print(f"  Material barrier (V/m³): {V0_material_per_m3:.3e} J/m³")
print(f"  UFO cross-section area : {A_ufo:.3e} m² (r={r_ufo} m)")
print(f"  Barrier length L       : {L_barrier:.4e} m (full Earth diameter)")
print(f"  Total barrier energy V0: {V0_total:.3e} J  ({V0_total/eV:.3e} eV)")
print(f"  UFO kinetic energy KE  : {KE_ufo:.3e} J  ({KE_ufo/eV:.3e} eV)")
print(f"  V0 >> KE by factor     : {V0_total/KE_ufo:.3e}")

# ─────────────────────────────────────────────────────────────
# SECTION 4: WKB TUNNELING PROBABILITY
# ─────────────────────────────────────────────────────────────
# T ≈ exp(-2 * kappa * L)
# where kappa = sqrt(2*M*(V0-E)) / hbar
# For a rectangular barrier with V0 >> E:
# kappa ≈ sqrt(2*M*V0) / hbar

# We use the TOTAL energy of the system (all atoms tunneling together)
# This is the most extreme (and most physically meaningful) case.

# For the WKB calculation we use a LOWER velocity scenario (v = 0.01c)
# to demonstrate tunneling. At v=0.90c the KE exceeds the material barrier,
# so the craft would classically punch through (above-barrier transmission).
# We compute BOTH scenarios.

print("\n[SECTION 4] WKB Tunneling Probability")
print("  --- Scenario A: v = 0.01c (sub-barrier, true tunneling) ---")
v_slow   = 0.01 * c
beta_slow = v_slow / c
gamma_slow = 1 / math.sqrt(1 - beta_slow**2)
KE_slow  = (gamma_slow - 1) * M_ufo * c**2
V0_eff = V0_total   # J
E_eff  = KE_slow

if V0_eff > E_eff:
    kappa = math.sqrt(2 * M_ufo * (V0_eff - E_eff)) / hbar
    log10_T = -2 * kappa * L_barrier / math.log(10)
    print(f"  KE (0.01c)             : {KE_slow:.4e} J")
    print(f"  V0 (material barrier)  : {V0_eff:.4e} J")
    print(f"  κ (decay constant)     : {kappa:.4e} m⁻¹")
    print(f"  2κL (exponent)         : {2*kappa*L_barrier:.4e}")
    print(f"  Exponent in powers of 10: {2*kappa*L_barrier/math.log(10):.4e}")
    print(f"  Tunneling probability T = 10^({log10_T:.4e})")
    print(f"  (For comparison, atoms in observable universe: ~10^80)")
    print(f"  T is effectively ZERO for all physical purposes.")
else:
    log10_T = float('nan')
    print(f"  KE > V0: above-barrier, no tunneling needed.")

print("\n  --- Scenario B: v = 0.90c (above-barrier, classical penetration) ---")
print(f"  KE (0.90c)             : {KE_ufo:.4e} J")
print(f"  V0 (material barrier)  : {V0_total:.4e} J")
print(f"  KE/V0 ratio            : {KE_ufo/V0_total:.4f}")
print(f"  Result: KE > V0 → craft punches through classically (above-barrier).")
print(f"  Above-barrier transmission T ≈ 1 (quantum reflection is small).")
# Store the slow-case log10_T for summary
log10_T_slow = log10_T

# ─────────────────────────────────────────────────────────────
# SECTION 4B: TUNNELING FOR A SINGLE ELECTRON (REFERENCE)
# ─────────────────────────────────────────────────────────────
# For a single electron through a 1 nm barrier with V0-E = 1 eV:
kappa_e = math.sqrt(2 * m_e * 1 * eV) / hbar
L_e = 1e-9   # 1 nm
T_e = math.exp(-2 * kappa_e * L_e)
print(f"\n  [Reference] Single electron, 1 nm barrier, 1 eV:")
print(f"  κ_e = {kappa_e:.4e} m⁻¹,  T_e = {T_e:.4e}")

# ─────────────────────────────────────────────────────────────
# SECTION 5: IF TUNNELING OCCURRED — TRANSIT TIME
# ─────────────────────────────────────────────────────────────
# If the UFO somehow tunneled through, how long would transit take?
# Classical transit time at v_ufo
t_transit_classical = 2 * R_earth / v_ufo
# Quantum tunneling group velocity through barrier (Hartman effect)
# v_tunnel ≈ L / tau_tunnel, where tau_tunnel can be very short
# For WKB: tau_tunnel = hbar / (2 * (V0-E)) * (some factor)
# Use Büttiker-Landauer traversal time: tau = M*L / (hbar*kappa)
tau_BL = M_ufo * L_barrier / (hbar * kappa)

print("\n[SECTION 5] Transit Time Analysis")
print(f"  Classical transit time : {t_transit_classical:.4f} s  ({t_transit_classical*1000:.2f} ms)")
print(f"  Büttiker-Landauer time : {tau_BL:.4e} s")
print(f"  (Tunneling can be superluminal in phase velocity — Hartman effect)")

# ─────────────────────────────────────────────────────────────
# SECTION 6: RADIATION GENERATED — CHERENKOV + IONIZATION
# ─────────────────────────────────────────────────────────────
# As the UFO (or its energy field) passes through matter at v > c/n,
# it generates Cherenkov radiation.

# Cherenkov condition: v > c/n
# Refractive index of desert sand (SiO2) ~ 1.46
# Refractive index of seawater ~ 1.34

n_sand  = 1.46
n_water = 1.34

c_sand  = c / n_sand
c_water = c / n_water

print("\n[SECTION 6] Cherenkov Radiation Analysis")
print(f"  UFO velocity           : {v_ufo:.4e} m/s  ({v_ufo/c*100:.1f}% c)")
print(f"\n  Desert (SiO₂ sand), n = {n_sand}")
print(f"    c/n (threshold)      : {c_sand:.4e} m/s  ({c_sand/c*100:.2f}% c)")
print(f"    v > c/n?             : {v_ufo > c_sand}")

print(f"\n  Ocean (seawater), n = {n_water}")
print(f"    c/n (threshold)      : {c_water:.4e} m/s  ({c_water/c*100:.2f}% c)")
print(f"    v > c/n?             : {v_ufo > c_water}")

# Cherenkov angle: cos(θ) = c/(n*v)
cos_sand  = c / (n_sand  * v_ufo)
cos_water = c / (n_water * v_ufo)
theta_sand  = math.acos(min(1.0, cos_sand))  * 180 / math.pi
theta_water = math.acos(min(1.0, cos_water)) * 180 / math.pi
print(f"\n  Cherenkov angle (sand) : θ = {theta_sand:.4f}°")
print(f"  Cherenkov angle (water): θ = {theta_water:.4f}°")
print(f"  (Cone half-angle measured from direction of motion)")

# Frank-Tamm formula: energy radiated per unit path length per unit frequency
# dE/(dx dω) = (q²/4π) * μ(ω) * (1 - c²/(n²v²))
# Integrated over visible spectrum (ω1 to ω2):
# For a charge q = Z*e traveling at v:
# dE/dx = (Z²e²/4π eps0 c²) * ∫ ω (1 - c²/n²v²) dω

# Approximate: Frank-Tamm for a singly charged particle
# dE/dx ≈ (Z²e²/4πε₀c²) * (1 - 1/β²n²) * ω_max²/2
# where β = v/c

beta = beta_ufo
gamma = gamma_ufo
Z = 1   # effective charge (symbolic; UFO is neutral but generates EM field)

# For visible light: ω_max ~ 4e15 rad/s (UV cutoff)
omega_max = 4e15   # rad/s
omega_min = 3e14   # rad/s (red light)

# Frank-Tamm energy loss per unit length (SI):
# dE/dx = (q²/(4π*eps0*c²)) * ∫[ω_min to ω_max] ω*(1 - 1/(β²n²)) dω
factor_sand  = 1 - 1/(beta**2 * n_sand**2)
factor_water = 1 - 1/(beta**2 * n_water**2)

prefactor = (e_c**2) / (4 * math.pi * eps0 * c**2)
dE_dx_sand  = prefactor * factor_sand  * (omega_max**2 - omega_min**2) / 2
dE_dx_water = prefactor * factor_water * (omega_max**2 - omega_min**2) / 2

print(f"\n  Frank-Tamm dE/dx (sand) : {dE_dx_sand:.4e} J/m  ({dE_dx_sand/eV:.4e} eV/m)")
print(f"  Frank-Tamm dE/dx (water): {dE_dx_water:.4e} J/m  ({dE_dx_water/eV:.4e} eV/m)")

# Scale for UFO: assume effective charge Z_eff ~ 1e6 (ionized plasma sheath)
Z_eff = 1e6
dE_dx_sand_ufo  = Z_eff**2 * dE_dx_sand
dE_dx_water_ufo = Z_eff**2 * dE_dx_water
print(f"\n  Scaled for Z_eff = {Z_eff:.0e} (plasma sheath):")
print(f"  dE/dx (sand) : {dE_dx_sand_ufo:.4e} J/m  ({dE_dx_sand_ufo/1e9:.4e} GJ/m)")
print(f"  dE/dx (water): {dE_dx_water_ufo:.4e} J/m  ({dE_dx_water_ufo/1e9:.4e} GJ/m)")

# ─────────────────────────────────────────────────────────────
# SECTION 7: IONIZATION RADIATION — BETHE-BLOCH ESTIMATE
# ─────────────────────────────────────────────────────────────
# Bethe formula (simplified): -dE/dx = K * Z² * ρ * Z_mat/(A_mat*β²) * [ln(...) - β²]
# K = 0.307075 MeV·cm²/g
# For sand (SiO2): Z_mat/A_mat ~ 0.5, rho = 1600 kg/m3 (loose sand)
# For seawater: Z_mat/A_mat ~ 0.55, rho = 1025 kg/m3

K = 0.307075e6 * eV * 1e-4  # convert MeV·cm²/g → J·m²/kg
rho_sand  = 1600   # kg/m3
rho_water = 1025   # kg/m3
ZA_sand   = 0.499  # Z/A for SiO2
ZA_water  = 0.555  # Z/A for water

# Mean excitation energy I (eV): sand ~145 eV, water ~75 eV
I_sand  = 145 * eV
I_water = 75  * eV

Tmax = 2 * m_e * c**2 * beta**2 * gamma**2   # maximum energy transfer

# Bethe formula:
# -dE/dx = K * Z_proj² * (Z/A)_mat * rho / beta² * [0.5*ln(2*m_e*c²*beta²*gamma²*Tmax/I²) - beta²]

def bethe(Z_proj, ZA_mat, rho_mat, I_mat, beta, gamma):
    Tmax_loc = 2 * m_e * c**2 * beta**2 * gamma**2
    log_term = 0.5 * math.log(2 * m_e * c**2 * beta**2 * gamma**2 * Tmax_loc / I_mat**2)
    dEdx = K * Z_proj**2 * ZA_mat * rho_mat / beta**2 * (log_term - beta**2)
    return dEdx

dEdx_bethe_sand  = bethe(Z_eff, ZA_sand,  rho_sand,  I_sand,  beta, gamma)
dEdx_bethe_water = bethe(Z_eff, ZA_water, rho_water, I_water, beta, gamma)

print("\n[SECTION 7] Bethe-Bloch Ionization Energy Loss")
print(f"  β = {beta:.6f},  γ = {gamma:.6f}")
print(f"  T_max = {Tmax/eV:.4e} eV")
print(f"\n  -dE/dx (sand,  Bethe): {dEdx_bethe_sand:.4e} J/m  ({dEdx_bethe_sand/1e9:.4e} GJ/m)")
print(f"  -dE/dx (water, Bethe): {dEdx_bethe_water:.4e} J/m  ({dEdx_bethe_water/1e9:.4e} GJ/m)")

# Radiation dose in a cylinder of radius R_dose around the path
R_dose = 100   # m — 100 m radius
depth_sand  = 10   # m — UFO enters 10 m into desert
depth_water = 100  # m — UFO enters 100 m into ocean

# Volume of affected cylinder
V_cyl_sand  = math.pi * R_dose**2 * depth_sand
V_cyl_water = math.pi * R_dose**2 * depth_water
mass_sand   = rho_sand  * V_cyl_sand
mass_water  = rho_water * V_cyl_water

E_dep_sand  = dEdx_bethe_sand  * depth_sand
E_dep_water = dEdx_bethe_water * depth_water

dose_sand  = E_dep_sand  / mass_sand   # J/kg = Gy
dose_water = E_dep_water / mass_water  # J/kg = Gy

print(f"\n  Radiation dose (100m radius, {depth_sand}m path in sand):")
print(f"    Energy deposited : {E_dep_sand:.4e} J")
print(f"    Mass of material : {mass_sand:.4e} kg")
print(f"    Absorbed dose    : {dose_sand:.4e} Gy  ({dose_sand:.4e} Sv)")
print(f"    (Lethal dose for humans ~ 4-5 Gy; fatal dose ~ 6 Gy)")

print(f"\n  Radiation dose (100m radius, {depth_water}m path in ocean):")
print(f"    Energy deposited : {E_dep_water:.4e} J")
print(f"    Mass of material : {mass_water:.4e} kg")
print(f"    Absorbed dose    : {dose_water:.4e} Gy  ({dose_water:.4e} Sv)")

# ─────────────────────────────────────────────────────────────
# SECTION 8: THERMAL EFFECTS — PLASMA CHANNEL
# ─────────────────────────────────────────────────────────────
# Energy deposited per meter heats a column of material.
# Temperature rise: ΔT = E_dep / (m * c_p)
# c_p (sand) ~ 840 J/(kg·K), c_p (water) ~ 4182 J/(kg·K)

cp_sand  = 840    # J/(kg·K)
cp_water = 4182   # J/(kg·K)

# Per meter of path, in a 1 m radius column
r_col = 1.0   # m
V_col_sand  = math.pi * r_col**2 * 1   # m³ per meter
V_col_water = math.pi * r_col**2 * 1

m_col_sand  = rho_sand  * V_col_sand
m_col_water = rho_water * V_col_water

dT_sand  = dEdx_bethe_sand  / (m_col_sand  * cp_sand)
dT_water = dEdx_bethe_water / (m_col_water * cp_water)

print("\n[SECTION 8] Thermal Effects — Plasma Channel (1 m radius column)")
print(f"  ΔT per meter (sand) : {dT_sand:.4e} K/m")
print(f"  ΔT per meter (water): {dT_water:.4e} K/m")
print(f"  Sand melting point  : ~1710 K (SiO2)")
print(f"  Water boiling point : 373 K")
print(f"  → Both media are instantly vaporized/plasma-ized along the path.")

# ─────────────────────────────────────────────────────────────
# SECTION 9: GRAVITATIONAL WAVE EMISSION (BONUS)
# ─────────────────────────────────────────────────────────────
# A mass M accelerating through Earth emits gravitational waves.
# Power: P_gw = (G/5c^5) * (d³Q/dt³)² where Q is quadrupole moment
# For a mass M moving at v through Earth (centripetal acceleration a):
# Simplified: P_gw ≈ (32/5) * G^4 * M^2 * M_earth^3 / (c^5 * R^5)
# (Peters formula for circular orbit — approximate for straight pass)

# For straight-line deceleration, use:
# P_gw = (G * M^2 * a^2) / (5 * c^5)  (quadrupole approximation)
# Deceleration: a = dv/dt — assume it decelerates from v to 0 over R_earth
a_decel = v_ufo**2 / (2 * R_earth)   # m/s²

P_gw = (G * M_ufo**2 * a_decel**2) / (5 * c**5)
print("\n[SECTION 9] Gravitational Wave Emission")
print(f"  Deceleration (approx) : {a_decel:.4e} m/s²  ({a_decel/9.81:.4e} g)")
print(f"  GW power emitted      : {P_gw:.4e} W")
print(f"  (For comparison, Hulse-Taylor binary pulsar: ~7.35e24 W)")

# ─────────────────────────────────────────────────────────────
# SECTION 10: SUMMARY TABLE
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SUMMARY OF KEY RESULTS")
print("=" * 70)
print(f"  UFO mass               : {M_ufo:.2e} kg")
print(f"  UFO velocity           : {v_ufo/c*100:.1f}% c = {v_ufo:.4e} m/s")
print(f"  de Broglie wavelength  : {lambda_dB:.4e} m")
print(f"  Tunneling probability  : 10^({log10_T_slow:.3e}) [at v=0.01c]")
print(f"  Earth diameter (barrier): {2*R_earth/1000:.0f} km")
print(f"  Cherenkov angle (sand) : {theta_sand:.4f}°")
print(f"  Cherenkov angle (water): {theta_water:.4f}°")
print(f"  Ionization dE/dx (sand): {dEdx_bethe_sand:.4e} J/m")
print(f"  Ionization dE/dx (water): {dEdx_bethe_water:.4e} J/m")
print(f"  Radiation dose (sand)  : {dose_sand:.4e} Gy")
print(f"  Radiation dose (water) : {dose_water:.4e} Gy")
print(f"  Plasma channel ΔT/m (sand) : {dT_sand:.4e} K/m")
print(f"  Plasma channel ΔT/m (water): {dT_water:.4e} K/m")
print(f"  GW power emitted       : {P_gw:.4e} W")
print("=" * 70)
