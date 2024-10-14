# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Study of the energetic comsuption of the CV-QKD protocol, with Gaussian modulation, with PSK modulation and for nCV-QKD for CKA.
"""

import matplotlib.pyplot as plt
from qenergy import components as comp
from qenergy.experiments_cv import CVQKDProtocol

from studies import FIGSIZE_HALF, EXPORT_DIR

# Parameters of the plot
dist_PSK = [d / 100 for d in range(850)]  # Points of the plot, PSK
dist_GM = [d / 10 for d in range(2000)]  # Points of the plot, GM
dist_nCV = [d / 10 for d in range(1500)]  # Points of the plot, nCV network

gigabit = 1e9  # Target number of secret bits
MJ = 1e6  # Change of scale to megajoules

# Parameters of the implementation
eta = 0.7  # Detector efficiency
Vel = 0.005  # Electrical noise
beta_PSK = 0.95  # Information reconciliation efficiency for PSK
beta_GM = 0.95  # Information reconciliation efficiency for GM
sourcerate = 1e8  # Laser frequency
xi = 0.005  # Excess noise

#############################################################################
# Source (same for all protocols)
source = [
    comp.LaserCVPPCL590(),
    comp.MBC(),
    comp.DAC(),
    comp.ThorlabsPowerMeter(),
    comp.Computer(),
]


# Components, Homodyne detection single polarization
DetectorHomodyne1P = [
    "Homodyne 1P",
    comp.ADC(),
    comp.LaserCVPPCL590(),
    comp.Computer(),
    comp.SwitchCVQKD(),
    comp.PolarizationController(),
    comp.ThorlabsPDB(),  # Detector
]

# Components, Homodyne detection double polarization
DetectorHomodyne2P = [
    "Homodyne 2P",
    comp.ADC(),
    comp.LaserCVPPCL590(),
    comp.Computer(),
    comp.SwitchCVQKD(),
    comp.PolarizationController(),
    comp.ThorlabsPDB(),
    comp.ThorlabsPDB(),  # Detector
]

# Components, Heterodyne detection single polarization
DetectorHeterodyne1P = [
    "Heterodyne 1P",
    comp.ADC(),
    comp.LaserCVPPCL590(),
    comp.Computer(),
    comp.SwitchCVQKD(),
    comp.PolarizationController(),
    comp.ThorlabsPDB(),
    comp.ThorlabsPDB(),  # Detector
]

# Components, Heterodyne detection double polarization
DetectorHeterodyne2P = [
    "Heterodyne 2P",
    comp.ADC(),
    comp.LaserCVPPCL590(),
    comp.Computer(),
    comp.SwitchCVQKD(),
    comp.PolarizationController(),
    comp.ThorlabsPDB(),
    comp.ThorlabsPDB(),
    comp.ThorlabsPDB(),
    comp.ThorlabsPDB(),  # Detector
]
#############################################################################

# Experiments, PSK
Experiment_PSK_Hm1P = CVQKDProtocol(
    eta, Vel, beta_PSK, sourcerate, source, DetectorHomodyne1P, xi, dist_PSK, "PSK"
)
Experiment_PSK_Hm2P = CVQKDProtocol(
    eta, Vel, beta_PSK, sourcerate, source, DetectorHomodyne2P, xi, dist_PSK, "PSK"
)
Experiment_PSK_Ht1P = CVQKDProtocol(
    eta, Vel, beta_PSK, sourcerate, source, DetectorHeterodyne1P, xi, dist_PSK, "PSK"
)
Experiment_PSK_Ht2P = CVQKDProtocol(
    eta, Vel, beta_PSK, sourcerate, source, DetectorHeterodyne2P, xi, dist_PSK, "PSK"
)

tsk_PSK_Hm1P = Experiment_PSK_Hm1P.time_skr(gigabit)
tsk_PSK_Hm2P = Experiment_PSK_Hm2P.time_skr(gigabit)
tsk_PSK_Ht1P = Experiment_PSK_Ht1P.time_skr(gigabit)
tsk_PSK_Ht2P = Experiment_PSK_Ht2P.time_skr(gigabit)


Energy_PSK_Hm1P = [Experiment_PSK_Hm1P.total_energy(t) / MJ for t in tsk_PSK_Hm1P]
Energy_PSK_Hm2P = [Experiment_PSK_Hm2P.total_energy(t) / MJ for t in tsk_PSK_Hm2P]
Energy_PSK_Ht1P = [Experiment_PSK_Ht1P.total_energy(t) / MJ for t in tsk_PSK_Ht1P]
Energy_PSK_Ht2P = [Experiment_PSK_Ht2P.total_energy(t) / MJ for t in tsk_PSK_Ht2P]


fig, ax = plt.subplots(1, figsize=FIGSIZE_HALF)
ax.plot(dist_PSK[: len(Energy_PSK_Hm1P)], Energy_PSK_Hm1P, label="Hom, 1P")
ax.plot(dist_PSK[: len(Energy_PSK_Hm2P)], Energy_PSK_Hm2P, label="Hom, 2P")
ax.plot(dist_PSK[: len(Energy_PSK_Ht1P)], Energy_PSK_Ht1P, label="Het, 1P")
ax.plot(dist_PSK[: len(Energy_PSK_Ht2P)], Energy_PSK_Ht2P, label="Het, 2P")

ax.set(xlabel="Distance [km]", ylabel="Energy consumption [MJ]")
ax.tick_params(axis="both", which="major")
ax.legend(loc="upper left")
ax.set_title("$N_{\\rm target} = 1$ GBit")

plt.ylim(0, 30)
plt.savefig(EXPORT_DIR / "PSKstudy.pdf", format="pdf")
plt.show()


# Experiments, GM
Experiment_GM_Hm1P = CVQKDProtocol(
    eta, Vel, beta_GM, sourcerate, source, DetectorHomodyne1P, xi, dist_GM, "Gauss"
)
Experiment_GM_Hm2P = CVQKDProtocol(
    eta, Vel, beta_GM, sourcerate, source, DetectorHomodyne2P, xi, dist_GM, "Gauss"
)
Experiment_GM_Ht1P = CVQKDProtocol(
    eta, Vel, beta_GM, sourcerate, source, DetectorHeterodyne1P, xi, dist_GM, "Gauss"
)
Experiment_GM_Ht2P = CVQKDProtocol(
    eta, Vel, beta_GM, sourcerate, source, DetectorHeterodyne2P, xi, dist_GM, "Gauss"
)

tsk_GM_Hm1P = Experiment_GM_Hm1P.time_skr(gigabit)
tsk_GM_Hm2P = Experiment_GM_Hm2P.time_skr(gigabit)
tsk_GM_Ht1P = Experiment_GM_Ht1P.time_skr(gigabit)
tsk_GM_Ht2P = Experiment_GM_Ht2P.time_skr(gigabit)

# Uncomment the zeros in the second argument of total_energy to take the DSP into account
Energy_GM_Hm1P = [Experiment_GM_Hm1P.total_energy(t) / MJ for t in tsk_GM_Hm1P]
Energy_GM_Hm2P = [Experiment_GM_Hm2P.total_energy(t) / MJ for t in tsk_GM_Hm2P]
Energy_GM_Ht1P = [Experiment_GM_Ht1P.total_energy(t) / MJ for t in tsk_GM_Ht1P]
Energy_GM_Ht2P = [Experiment_GM_Ht2P.total_energy(t) / MJ for t in tsk_GM_Ht2P]


fig, ax = plt.subplots(1, figsize=FIGSIZE_HALF)

ax.plot(dist_GM, Energy_GM_Hm1P, label="Hom, 1P")
ax.plot(dist_GM, Energy_GM_Hm2P, label="Hom, 2P")
ax.plot(dist_GM, Energy_GM_Ht1P, label="Het, 1P")
ax.plot(dist_GM, Energy_GM_Ht2P, label="Het, 2P")

ax.set(xlabel="Distance [km]", ylabel="Energy consumption [MJ]")
ax.tick_params(axis="both", which="major")
ax.legend(loc="upper left")

ax.set_title("$N_{\\rm target} = 1$ GBit")

plt.ylim(0, 60)
fig.savefig(EXPORT_DIR / "GMstudy.pdf", format="pdf")
plt.show()


# Experiments, nCV-QKD protocol
"""
This scheme is given by n(n-1)/2 times the results coming from the GM 
case with all users at the same distance. The implementation is
given by homodyne measurements with double polarization.
"""

Nusers = [i for i in range(3, 7)]  # No. of parties involved in the exchange

fig, ax = plt.subplots(1, figsize=FIGSIZE_HALF)

# Loop of the experiments according to the no. of users
for N in Nusers:
    Experiment_nCV = CVQKDProtocol(
        eta, Vel, beta_GM, sourcerate, source, DetectorHomodyne2P, xi, dist_nCV, "Gauss"
    )
    tsk_nCV = Experiment_nCV.time_skr(gigabit)
    # Note the (N-1) since the protocol is executed by every pair of users wrt a central node
    # Uncomment the zeros in the second argument of total_energy to take the DSP into account
    Energy_nCV = [Experiment_nCV.total_energy(t) * (N - 1) / MJ for t in tsk_nCV]
    plt.plot(dist_nCV, Energy_nCV, label=f"{N} users")


ax.set(xlabel="Distance [km]", ylabel="Energy consumption [MJ]")
ax.tick_params(axis="both", which="major")
ax.legend(loc="upper left")
ax.set_title(r"$N_{{\mathrm{{target}}}}$ = {0} GBit".format(int(gigabit / 1e9)))

plt.ylim(0, 20)
fig.savefig(EXPORT_DIR / "nCV.pdf", format="pdf")
plt.show()
