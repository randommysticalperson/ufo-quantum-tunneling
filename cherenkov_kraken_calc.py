"""
Comprehensive Speculative Physics Calculations:
1. Cherenkov Radiation in the Deep Ocean — Effects on Kraken & Deep-Sea Life
2. Radiation and the Origin of Life
3. WKB Quantum Tunneling of Space Debris and Meteorites
"""

import numpy as np
import scipy.integrate as integrate

# ============================================================
# CONSTANTS
# ============================================================
c = 2.998e8          # speed of light (m/s)
hbar = 1.055e-34     # reduced Planck constant (J·s)
e_charge = 1.602e-19 # electron charge (C)
m_e = 9.109e-31      # electron mass (kg)
m_p = 1.673e-27      # proton mass (kg)
amu = 1.661e-27      # atomic mass unit (kg)
k_B = 1.381e-23      # Boltzmann constant (J/K)
N_A = 6.022e23       # Avogadro's number
eV = 1.602e-19       # 1 eV in Joules
MeV = 1.602e-13      # 1 MeV in Joules
GeV = 1.602e-10      # 1 GeV in Joules

print("=" * 70)
print("PART 1: CHERENKOV RADIATION IN THE DEEP OCEAN")
print("=" * 70)

# ============================================================
# 1A. SEAWATER CHERENKOV PROPERTIES
# ============================================================
n_seawater = 1.340       # refractive index of seawater at ~400nm (blue)
n_freshwater = 1.333     # freshwater
n_ice = 1.310            # deep ice (IceCube detector)

# Threshold velocity: v_threshold = c/n
v_thresh_sea = c / n_seawater
beta_thresh_sea = 1.0 / n_seawater

print("\n--- Seawater Cherenkov Threshold ---")
print(f"Refractive index of seawater (n): {n_seawater}")
print(f"Threshold velocity: v_thresh = c/n = {v_thresh_sea:.4e} m/s = {beta_thresh_sea:.4f}c")

# Threshold kinetic energy for electrons
gamma_thresh_e = 1.0 / np.sqrt(1 - beta_thresh_sea**2)
KE_thresh_e = (gamma_thresh_e - 1) * m_e * c**2 / eV * 1e-3  # keV
print(f"\nElectron threshold kinetic energy: {KE_thresh_e:.2f} keV")

# Threshold for muons
m_mu = 105.66 * MeV / c**2
gamma_thresh_mu = 1.0 / np.sqrt(1 - beta_thresh_sea**2)
KE_thresh_mu = (gamma_thresh_mu - 1) * m_mu * c**2 / MeV
print(f"Muon threshold kinetic energy: {KE_thresh_mu:.2f} MeV")

# Cherenkov angle as function of beta
def cherenkov_angle(beta, n):
    cos_theta = 1.0 / (n * beta)
    if cos_theta > 1.0:
        return None  # below threshold
    return np.degrees(np.arccos(cos_theta))

# At various particle velocities
print("\n--- Cherenkov Angles in Seawater ---")
betas = [0.75, 0.80, 0.90, 0.95, 0.99, 0.999]
for b in betas:
    angle = cherenkov_angle(b, n_seawater)
    if angle:
        print(f"  beta = {b:.3f}: theta_C = {angle:.2f}°")

# Frank-Tamm formula: energy radiated per unit path length per unit wavelength
# d²E/dxdλ = (q²/4π) * (2π/λ²) * (1 - 1/(n²β²)) for n*beta > 1
# Total photons in visible range (400-700 nm) per cm of path
def frank_tamm_photons_per_cm(beta, n, lambda1=400e-9, lambda2=700e-9):
    """Number of visible Cherenkov photons per cm of path (Frank-Tamm)"""
    # N/L = 2π * alpha * sin²(theta_C) * (1/lambda1 - 1/lambda2)
    alpha = 1/137.036  # fine structure constant
    cos_theta = 1.0 / (n * beta)
    if cos_theta >= 1.0:
        return 0
    sin2_theta = 1 - cos_theta**2
    N_per_m = 2 * np.pi * alpha * sin2_theta * (1/lambda1 - 1/lambda2)
    return N_per_m / 100  # per cm

print("\n--- Cherenkov Photon Yield in Seawater (visible, 400-700nm) ---")
for b in betas:
    N = frank_tamm_photons_per_cm(b, n_seawater)
    if N > 0:
        print(f"  beta = {b:.3f}: {N:.1f} photons/cm of path")

# ============================================================
# 1B. NATURAL CHERENKOV RADIATION IN THE DEEP OCEAN
# ============================================================
print("\n--- Natural Cherenkov Background in Deep Ocean ---")
# K-40 beta decay: produces electrons up to 1.31 MeV endpoint
# Seawater K-40 activity: ~12.5 Bq/L
K40_activity_per_L = 12.5  # Bq/L
K40_activity_per_m3 = K40_activity_per_L * 1000  # Bq/m³

# Fraction of K-40 electrons above Cherenkov threshold (0.26 MeV in water)
# K-40 beta spectrum endpoint = 1.31 MeV; threshold = 0.26 MeV
# Approximately 70% of electrons are above threshold
frac_above_thresh = 0.70
cherenkov_rate_per_m3 = K40_activity_per_m3 * frac_above_thresh

print(f"K-40 activity in seawater: {K40_activity_per_L} Bq/L = {K40_activity_per_m3:.0f} Bq/m³")
print(f"Cherenkov-producing electrons (>0.26 MeV): ~{frac_above_thresh*100:.0f}% of decays")
print(f"Cherenkov photon-producing events: ~{cherenkov_rate_per_m3:.0f} per m³ per second")

# Photon flux at depth
# Each electron produces ~10 photons/cm in visible range (at ~0.8c)
photons_per_decay = 10  # visible photons per Cherenkov electron (rough estimate, ~10 cm path)
photon_flux_per_m3 = cherenkov_rate_per_m3 * photons_per_decay
print(f"Estimated visible Cherenkov photon production: ~{photon_flux_per_m3:.2e} photons/m³/s")

# ============================================================
# 1C. THE KRAKEN — HYPOTHETICAL GIANT CEPHALOPOD
# ============================================================
print("\n--- The Kraken: Hypothetical Giant Cephalopod ---")
# Giant squid (Architeuthis dux): up to 13m, ~275 kg
# Hypothetical kraken: 50m length, ~50,000 kg
kraken_length = 50.0    # m
kraken_mass = 50000.0   # kg
kraken_depth = 3000.0   # m (typical deep ocean)

# Water pressure at depth
rho_water = 1025.0  # kg/m³ seawater
g = 9.81  # m/s²
pressure_at_depth = rho_water * g * kraken_depth / 1e6  # MPa
print(f"Kraken parameters: Length = {kraken_length} m, Mass = {kraken_mass} kg")
print(f"Habitat depth: {kraken_depth} m")
print(f"Pressure at depth: {pressure_at_depth:.1f} MPa ({pressure_at_depth/0.101325:.0f} atm)")

# Radiation dose to kraken from natural Cherenkov
# Dose rate from K-40 in seawater (background)
# Natural background dose in deep ocean: ~0.1 mGy/year from K-40
dose_rate_ocean = 0.1e-3 / (365.25 * 24 * 3600)  # Gy/s
print(f"\nNatural K-40 Cherenkov dose rate in deep ocean: ~{dose_rate_ocean:.2e} Gy/s")
print(f"  = {dose_rate_ocean * 365.25 * 24 * 3600 * 1000:.2f} mGy/year")

# Lethal dose for cephalopods: ~10-50 Gy (estimated, similar to invertebrates)
LD50_cephalopod = 20.0  # Gy (estimated)
time_to_lethal_natural = LD50_cephalopod / dose_rate_ocean / (365.25 * 24 * 3600)
print(f"Estimated LD50 for cephalopod: ~{LD50_cephalopod} Gy")
print(f"Time to LD50 from natural background: {time_to_lethal_natural:.2e} years (safe)")

# Now: a high-energy cosmic ray muon passing through the kraken
# Cosmic ray muons at sea level: ~10,000/m²/min
# At 3000m depth: heavily attenuated, ~1/m²/min for high-energy muons
muon_flux_deep = 1.0  # /m²/min at 3000m
muon_flux_deep_per_s = muon_flux_deep / 60.0

# Muon energy loss in tissue (similar to water): ~2 MeV/cm (minimum ionizing)
dEdx_muon_tissue = 2.0 * MeV / 0.01  # J/m (2 MeV/cm)
# Path through kraken body (~1m cross section)
path_kraken = 1.0  # m
energy_dep_per_muon = dEdx_muon_tissue * path_kraken  # J

# Dose per muon per kg of tissue in path
kraken_cross_section = 1.0  # m² (body cross section)
mass_in_path = kraken_cross_section * 1.0 * 1000  # kg (1m depth, density ~1000 kg/m³)
dose_per_muon = energy_dep_per_muon / mass_in_path  # Gy
dose_rate_muon = dose_per_muon * muon_flux_deep_per_s * kraken_cross_section

print(f"\nCosmic ray muon flux at {kraken_depth}m depth: ~{muon_flux_deep} /m²/min")
print(f"Energy deposited per muon through 1m of tissue: {energy_dep_per_muon/MeV:.1f} MeV")
print(f"Dose rate from cosmic muons: {dose_rate_muon:.2e} Gy/s")
print(f"  = {dose_rate_muon * 365.25 * 24 * 3600 * 1000:.3f} mGy/year")

# ============================================================
# 1D. CHERENKOV RADIATION FROM A HYPOTHETICAL RELATIVISTIC SOURCE
# ============================================================
print("\n--- Cherenkov Radiation from a Relativistic Particle Beam in Ocean ---")
# Imagine a relativistic proton beam (like from a cosmic ray) at 0.99c
beta_beam = 0.99
gamma_beam = 1.0 / np.sqrt(1 - beta_beam**2)
KE_proton = (gamma_beam - 1) * m_p * c**2 / GeV
theta_C_beam = cherenkov_angle(beta_beam, n_seawater)

print(f"Relativistic proton at beta = {beta_beam}: gamma = {gamma_beam:.2f}")
print(f"Kinetic energy: {KE_proton:.2f} GeV")
print(f"Cherenkov angle in seawater: {theta_C_beam:.2f}°")
N_photons = frank_tamm_photons_per_cm(beta_beam, n_seawater)
print(f"Cherenkov photon yield: {N_photons:.1f} photons/cm")

# Cherenkov cone geometry
cone_half_angle = theta_C_beam
print(f"\nCherenkov cone half-angle: {cone_half_angle:.2f}°")
print(f"This cone would illuminate a circle of radius r = L*tan({cone_half_angle:.1f}°) at distance L")
L_values = [1, 5, 10, 50, 100]  # meters
print("Cone radius at various distances:")
for L in L_values:
    r = L * np.tan(np.radians(cone_half_angle))
    print(f"  L = {L:4d} m: r = {r:.2f} m")

print("\n")
print("=" * 70)
print("PART 2: RADIATION AND THE ORIGIN OF LIFE")
print("=" * 70)

# ============================================================
# 2A. EARLY EARTH RADIATION ENVIRONMENT
# ============================================================
print("\n--- Early Earth Radiation Environment (4.0 Ga) ---")
# K-40 was ~85x more abundant 4 Ga ago (half-life 1.25 Ga)
# U-238: half-life 4.47 Ga → ~2x more abundant
# U-235: half-life 0.704 Ga → ~85x more abundant
# Th-232: half-life 14.0 Ga → ~1.3x more abundant

t_early = 4.0e9  # years ago
t_half_K40 = 1.25e9
t_half_U238 = 4.47e9
t_half_U235 = 0.704e9
t_half_Th232 = 14.0e9

ratio_K40 = 2**(t_early / t_half_K40)
ratio_U238 = 2**(t_early / t_half_U238)
ratio_U235 = 2**(t_early / t_half_U235)
ratio_Th232 = 2**(t_early / t_half_Th232)

print(f"Isotope abundance ratios at 4.0 Ga vs today:")
print(f"  K-40:  {ratio_K40:.1f}x more abundant")
print(f"  U-238: {ratio_U238:.2f}x more abundant")
print(f"  U-235: {ratio_U235:.1f}x more abundant")
print(f"  Th-232:{ratio_Th232:.2f}x more abundant")

# Modern background dose rate: ~2.4 mSv/year = 2.4 mGy/year (for low-LET)
modern_dose = 2.4e-3  # Gy/year
early_earth_dose = modern_dose * (ratio_K40 * 0.4 + ratio_U238 * 0.3 + ratio_U235 * 0.1 + ratio_Th232 * 0.2)
print(f"\nModern natural background dose: {modern_dose*1000:.1f} mGy/year")
print(f"Estimated early Earth dose rate: {early_earth_dose*1000:.1f} mGy/year")
print(f"  = {early_earth_dose:.4f} Gy/year")

# UV radiation: early Earth had no ozone layer
# Modern UV-B at surface: ~0.1 W/m²; early Earth: ~100x higher (no ozone)
UV_modern = 0.1  # W/m²
UV_early = UV_modern * 100  # W/m²
print(f"\nUV-B radiation:")
print(f"  Modern (with ozone): {UV_modern} W/m²")
print(f"  Early Earth (no ozone, ~3.8 Ga): ~{UV_early} W/m² (100x higher)")

# Energy for prebiotic chemistry: HCN synthesis requires ~5 eV photons (UV-C)
E_HCN = 5.0 * eV  # J
lambda_HCN = 6.626e-34 * c / E_HCN * 1e9  # nm
print(f"\nHCN synthesis photon energy: {E_HCN/eV:.1f} eV → wavelength = {lambda_HCN:.0f} nm (UV-C)")

# ============================================================
# 2B. METEORITE DELIVERY OF ORGANICS
# ============================================================
print("\n--- Meteorite Delivery of Organic Molecules ---")
# Murchison meteorite: ~2% organic carbon by mass
# Estimated 100 kg/m²/year of cosmic dust to early Earth
cosmic_dust_flux = 100.0  # kg/m²/year (early Earth estimate)
organic_fraction = 0.02   # 2% organic carbon
amino_acid_fraction = 0.001  # ~0.1% amino acids

organic_flux = cosmic_dust_flux * organic_fraction
amino_flux = cosmic_dust_flux * amino_acid_fraction

print(f"Cosmic dust flux to early Earth: ~{cosmic_dust_flux} kg/m²/year")
print(f"Organic carbon delivered: ~{organic_flux} kg/m²/year")
print(f"Amino acids delivered: ~{amino_flux*1000:.1f} g/m²/year")

# Total delivery to Earth surface
R_earth = 6.371e6  # m
A_earth = 4 * np.pi * R_earth**2
total_amino = amino_flux * A_earth  # kg/year
print(f"\nTotal amino acid delivery to Earth: {total_amino:.2e} kg/year")
print(f"  = {total_amino/1000:.2e} tonnes/year")

# ============================================================
# 2C. RADIATION-INDUCED PREBIOTIC CHEMISTRY
# ============================================================
print("\n--- Radiation-Induced Prebiotic Chemistry ---")
# G-value: molecules produced per 100 eV of radiation absorbed
# G(HCN) ~ 0.1 molecules/100 eV in N2/CH4 atmosphere
# G(amino acids) ~ 0.01 molecules/100 eV
G_HCN = 0.1       # molecules per 100 eV
G_amino = 0.01    # molecules per 100 eV

# Energy deposited in early ocean (1 km deep, 1 m² column) per year
# From ionizing radiation (early Earth dose rate)
ocean_depth = 1000.0  # m
ocean_density = 1025.0  # kg/m³
mass_column = ocean_depth * ocean_density  # kg/m²

dose_per_year = early_earth_dose  # Gy = J/kg
energy_per_m2_per_year = dose_per_year * mass_column  # J/m²/year
energy_per_m2_per_year_eV = energy_per_m2_per_year / eV  # eV/m²/year

HCN_per_m2 = G_HCN * energy_per_m2_per_year_eV / 100
amino_per_m2 = G_amino * energy_per_m2_per_year_eV / 100

print(f"Energy deposited in 1km ocean column per year: {energy_per_m2_per_year:.2e} J/m²")
print(f"  = {energy_per_m2_per_year_eV:.2e} eV/m²")
print(f"HCN molecules produced per m² per year (G={G_HCN}): {HCN_per_m2:.2e}")
print(f"Amino acid precursors per m² per year (G={G_amino}): {amino_per_m2:.2e}")

print("\n")
print("=" * 70)
print("PART 3: WKB QUANTUM TUNNELING — SPACE DEBRIS AND METEORITES")
print("=" * 70)

# ============================================================
# 3A. OBJECT PARAMETERS
# ============================================================
print("\n--- Object Parameters ---")

objects = {
    "Paint fleck (1mm)":     {"mass": 1e-6,    "radius": 5e-4,  "velocity": 7800,    "desc": "LEO debris"},
    "Bolt (10g)":            {"mass": 0.01,    "radius": 0.01,  "velocity": 7800,    "desc": "LEO debris"},
    "Defunct satellite":     {"mass": 1000.0,  "radius": 1.0,   "velocity": 7800,    "desc": "LEO debris"},
    "Chondrite meteorite":   {"mass": 10.0,    "radius": 0.12,  "velocity": 20000,   "desc": "stony, 10 kg"},
    "Iron meteorite (1t)":   {"mass": 1000.0,  "radius": 0.34,  "velocity": 25000,   "desc": "iron-nickel, 1 tonne"},
    "Chelyabinsk-class":     {"mass": 1.2e10,  "radius": 10.0,  "velocity": 19000,   "desc": "~12,000 tonnes"},
}

for name, obj in objects.items():
    m = obj["mass"]
    v = obj["velocity"]
    beta = v / c
    gamma = 1.0 / np.sqrt(1 - beta**2)
    KE = (gamma - 1) * m * c**2
    lambda_dB = hbar / (gamma * m * v)  # relativistic de Broglie wavelength
    print(f"\n{name} ({obj['desc']}):")
    print(f"  Mass = {m:.2e} kg, v = {v:.0f} m/s = {beta:.6f}c")
    print(f"  Relativistic KE = {KE:.3e} J = {KE/1e9:.3e} GJ")
    print(f"  de Broglie wavelength = {lambda_dB:.3e} m")

# ============================================================
# 3B. WKB TUNNELING THROUGH EARTH FOR DEBRIS/METEORITES
# ============================================================
print("\n--- WKB Tunneling Through Earth (PREM-based potential) ---")

# Earth parameters
R_earth = 6.371e6  # m
path_length = 2 * R_earth  # diameter

# PREM density profile (simplified polynomial per layer)
def prem_density(r_frac):
    """Density in kg/m³ as function of fractional radius r/R_earth"""
    x = r_frac
    if x <= 0.192:    # inner core
        return 1000 * (13.0885 - 8.8381 * x**2)
    elif x <= 0.546:  # outer core
        return 1000 * (12.5815 - 1.2638*x - 3.6426*x**2 - 5.5281*x**3)
    elif x <= 0.895:  # lower mantle
        return 1000 * (7.9565 - 6.4761*x + 5.5283*x**2 - 3.0807*x**3)
    elif x <= 0.937:  # transition zone
        return 1000 * (5.3197 - 1.4836*x)
    elif x <= 0.965:  # upper mantle
        return 1000 * (11.2494 - 8.0298*x)
    elif x <= 0.996:  # crust
        return 1000 * 2.9
    else:
        return 1000 * 2.6  # surface crust

# Build V(x) profile along diameter
N_points = 50000
s_values = np.linspace(0, 2*R_earth, N_points)
ds = s_values[1] - s_values[0]

density_profile = np.zeros(N_points)
for i, s in enumerate(s_values):
    # Distance from center
    if s <= R_earth:
        r = s
    else:
        r = 2*R_earth - s
    r_frac = r / R_earth
    density_profile[i] = prem_density(r_frac)

# Potential barrier per unit length: V(x) = n(x) * E_bind * A
# n(x) = number density = rho(x) / m_atom
# E_bind = average atomic binding energy ~5 eV
# A = cross-sectional area of object

E_bind = 5.0 * eV   # J per atom
m_atom_avg = 25.0 * amu  # average atomic mass of Earth material

def compute_wkb(mass, radius, velocity):
    """Compute WKB tunneling exponent Gamma for given object through Earth"""
    beta = velocity / c
    gamma_rel = 1.0 / np.sqrt(1 - beta**2)
    KE = (gamma_rel - 1) * mass * c**2  # J
    KE_per_L = KE / path_length  # J/m

    A = np.pi * radius**2  # cross-sectional area

    # V(x) = rho(x)/m_atom * E_bind * A [J/m]
    V_profile = (density_profile / m_atom_avg) * E_bind * A

    # kappa(x) = sqrt(2*M*(V(x) - KE/L)) / hbar where V > KE/L
    kappa_profile = np.zeros(N_points)
    for i in range(N_points):
        V = V_profile[i]
        if V > KE_per_L:
            kappa_profile[i] = np.sqrt(2 * mass * (V - KE_per_L)) / hbar
        else:
            kappa_profile[i] = 0.0

    Gamma = np.trapezoid(kappa_profile, s_values)
    log10_T = -2 * Gamma / np.log(10)
    return Gamma, log10_T, V_profile, kappa_profile

print("\nWKB Results for Space Debris and Meteorites:")
print(f"{'Object':<30} {'Mass (kg)':<12} {'v (m/s)':<10} {'Gamma':<20} {'log10(T)':<20}")
print("-" * 92)

wkb_results = {}
for name, obj in objects.items():
    Gamma, log10_T, V_prof, kappa_prof = compute_wkb(obj["mass"], obj["radius"], obj["velocity"])
    wkb_results[name] = {"Gamma": Gamma, "log10_T": log10_T, "V_prof": V_prof, "kappa_prof": kappa_prof}
    if Gamma == 0:
        print(f"{name:<30} {obj['mass']:<12.2e} {obj['velocity']:<10.0f} {'0 (above barrier)':<20} {'0 (classical)':<20}")
    else:
        print(f"{name:<30} {obj['mass']:<12.2e} {obj['velocity']:<10.0f} {Gamma:<20.4e} {log10_T:<20.4e}")

# ============================================================
# 3C. CLASSICAL THRESHOLD VELOCITY FOR EACH OBJECT
# ============================================================
print("\n--- Classical Penetration Threshold Velocities ---")
# Find velocity where KE = V_max * path_length
# V_max occurs at inner core center

# Peak potential per unit length (at center, rho ~ 13,000 kg/m³)
rho_center = 13088.0  # kg/m³
for name, obj in objects.items():
    A = np.pi * obj["radius"]**2
    V_max = (rho_center / m_atom_avg) * E_bind * A  # J/m
    E_thresh = V_max * path_length  # J
    # Solve (gamma-1)*mc² = E_thresh
    mc2 = obj["mass"] * c**2
    gamma_thresh = E_thresh / mc2 + 1
    if gamma_thresh > 1:
        beta_thresh = np.sqrt(1 - 1/gamma_thresh**2)
        v_thresh = beta_thresh * c
        print(f"{name:<30}: V_max = {V_max:.2e} J/m, E_thresh = {E_thresh:.2e} J, v_thresh = {beta_thresh:.6f}c = {v_thresh:.2e} m/s")
    else:
        print(f"{name:<30}: Already above barrier at any velocity")

# ============================================================
# 3D. METEORITE IMPACT ENERGY COMPARISON
# ============================================================
print("\n--- Impact Energy Comparison ---")
TNT_J = 4.184e9  # J per tonne of TNT

impact_objects = {
    "Chelyabinsk (2013)":  {"mass": 1.2e10, "velocity": 19000},
    "Tunguska (1908)":     {"mass": 1.0e8,  "velocity": 27000},
    "Chicxulub (66 Ma)":   {"mass": 2.0e15, "velocity": 20000},
    "Iron meteorite 1t":   {"mass": 1000,   "velocity": 25000},
    "LEO satellite 1t":    {"mass": 1000,   "velocity": 7800},
}

for name, obj in impact_objects.items():
    m = obj["mass"]
    v = obj["velocity"]
    beta = v / c
    gamma = 1.0 / np.sqrt(1 - beta**2)
    KE = (gamma - 1) * m * c**2
    KE_classical = 0.5 * m * v**2
    TNT_equiv = KE_classical / TNT_J
    print(f"{name:<25}: KE = {KE_classical:.2e} J = {TNT_equiv:.2e} tonnes TNT")

print("\n--- Summary ---")
print("Space debris and meteorites at typical solar system velocities (7-30 km/s)")
print("are VASTLY sub-relativistic (beta ~ 0.00003 to 0.0001).")
print("Their WKB tunneling probability through Earth is even more impossibly small")
print("than the UFO case, because their kinetic energies are smaller relative to")
print("their cross-sectional barrier heights.")
print("\nFor a 10 kg chondrite at 20 km/s:")
name = "Chondrite meteorite"
G = wkb_results[name]["Gamma"]
lT = wkb_results[name]["log10_T"]
print(f"  Gamma = {G:.4e}")
print(f"  log10(T) = {lT:.4e}")
print(f"  T = 10^({lT:.2e}) — absolutely impossible")

print("\nAll calculations complete.")
