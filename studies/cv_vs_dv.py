# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Study to compare the energetics cost of DV protocols with CV ones.
"""

import numpy as np
import matplotlib.pyplot as plt
from qenergy import components as comp
from qenergy.experiments_cv import CVQKDProtocol
from qenergy.experiments_dv import BB84Experiment

from studies import FIGSIZE_FULL, EXPORT_DIR

"""This script produces a plot of the comparison of energy consumption of the BB84 protocol and the one of CV-QKD, for different hardware. 
    The components can be modified and the list of available component is in component.py"""


dist = [d for d in range(200)]
wavelength = 1550
gigabit = 1e9  # Target number of secret bits
MJ = 1e6  # Change of scale to megajoules

cvqkd_rate = 100e6
# DV hardware
##Source
laser = comp.LaserNKTkoheras1550()
mu = 0.1
sourcerate = 80 * 10**6
pcoupling = 0.9

# Detector
detectorsnspd = comp.DetectorSNSPD1550()
detectoringaas = comp.DetectorInGAs1550()


# Parameters of the CV implementation
eta = 0.7  # Detector efficiency
Vel = 0.005  # Electrical noise
beta_PSK = 0.95  # Information reconciliation efficiency for PSK
beta_GM = 0.95  # Information reconciliation efficiency for GM
source = comp.SourceCV()  # Source (same for all protocols)
xi = 0.005  # Excess noise
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
    comp.ThorlabsPDB(),
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
    comp.ThorlabsPDB(),
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
    comp.ThorlabsPDB(),
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
    comp.ThorlabsPDB(),
]
#############################################################################

# DV Experiment
# Other components
other = [
    comp.MotorizedWavePlate(),
    comp.MotorizedWavePlate(),
    comp.Computer(),
    comp.Computer(),
    comp.SwitchIntensityModulator(),
    comp.TimeTagger(),
]

ExperimentBB84SNSPD = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength, 0.01, laser, detectorsnspd, dist, other
)
ExperimentBB84APD = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength, 0.01, laser, detectoringaas, dist, other
)


tskr = ExperimentBB84SNSPD.time_skr(gigabit)
tskr2 = ExperimentBB84APD.time_skr(gigabit)


Energysnspd = [ExperimentBB84SNSPD.total_energy(t) / MJ for t in tskr]
Energyingaas = [ExperimentBB84APD.total_energy(t) / MJ for t in tskr2]

# CV Experiment, Gaussian Modulation

Experiment_GM_Hm1P = CVQKDProtocol(
    eta, Vel, beta_GM, cvqkd_rate, source, DetectorHomodyne1P, xi, dist, "Gauss"
)
Experiment_GM_Hm2P = CVQKDProtocol(
    eta, Vel, beta_GM, cvqkd_rate, source, DetectorHomodyne2P, xi, dist, "Gauss"
)
Experiment_GM_Ht1P = CVQKDProtocol(
    eta, Vel, beta_GM, cvqkd_rate, source, DetectorHeterodyne1P, xi, dist, "Gauss"
)
Experiment_GM_Ht2P = CVQKDProtocol(
    eta, Vel, beta_GM, cvqkd_rate, source, DetectorHeterodyne2P, xi, dist, "Gauss"
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

# addition of the DSP costs
skrCV = Experiment_GM_Ht2P.compute_secret_key_rate()
taudsp = 0.006
taudsp2 = 0.018
taudsp3 = 0.0003
Edsp = []
Edsp2 = []
Edsp3 = []
for t in skrCV:
    Edsp.append(taudsp * gigabit / t * cvqkd_rate / MJ)
    Edsp2.append(taudsp2 * gigabit / t * cvqkd_rate / MJ)
    Edsp3.append(taudsp3 * gigabit / t * cvqkd_rate / MJ)

Energy_GM_Ht2P_withDSPsupersmall = []
Energy_GM_Ht2P_withDSPsmall = []
Energy_GM_Ht2P_withDSPbig = []

for i in range(len(Energy_GM_Ht2P)):
    Energy_GM_Ht2P_withDSPsmall.append(Energy_GM_Ht2P[i] + Edsp[i])
    Energy_GM_Ht2P_withDSPbig.append(Energy_GM_Ht2P[i] + Edsp2[i])
    Energy_GM_Ht2P_withDSPsupersmall.append(Energy_GM_Ht2P[i] + Edsp3[i])


fig, ax = plt.subplots(1, figsize=FIGSIZE_FULL)
ax.plot(dist, Energysnspd, color="tab:blue", ls="--", label="BB84 with SNSPDs")
ax.plot(dist, Energyingaas, color="tab:blue", label="BB84 with APDs")
# ax.plot(dist, Energy_GM_Hm1P, label="CV-QKD, Hom, 1P")
# ax.plot(dist, Energy_GM_Hm2P, label="CV-QKD, Hom, 2P")
# ax.plot(dist, Energy_GM_Ht1P, label="CV-QKD, Het, 1P")
ax.plot(dist, Energy_GM_Ht2P, color="tab:orange", label="CV-QKD $\\tau_{DSP}=0$")
ax.plot(
    dist,
    Energy_GM_Ht2P_withDSPsmall,
    color="tab:orange",
    ls="--",
    label="CV-QKD $\\tau_{DSP}=0.006$",
)
ax.plot(
    dist,
    Energy_GM_Ht2P_withDSPbig,
    color="tab:orange",
    ls="-.",
    label="CV-QKD $\\tau_{DSP}=0.018$",
)
ax.plot(dist, Energy_GM_Ht2P_withDSPsupersmall,
        color="tab:orange",
        ls=":",
        label="CV-QKD $\\tau_{DSP}=0.0003$"
)

# axins = ax.inset_axes(
#     [0.1, 0.3, 0.3, 0.4],
#     xlim=(0, 20),
#     ylim=(0, 40),
# )
dist = np.array(dist)
Energyingaas = np.array(Energyingaas)
Energy_GM_Ht2P = np.array(Energy_GM_Ht2P)
Energy_GM_Ht2P_withDSPsmall = np.array(Energy_GM_Ht2P_withDSPsmall)
Energy_GM_Ht2P_withDSPbig = np.array(Energy_GM_Ht2P_withDSPbig)
mask = np.where(dist <= 20)[0]
# axins.plot(dist[mask], Energyingaas[mask], color="tab:blue", label="BB84 with APDs")
# axins.plot(
#     dist[mask], Energy_GM_Ht2P[mask], color="tab:orange", label="CV-QKD, without DSP"
# )
# axins.plot(
#     dist[mask],
#     Energy_GM_Ht2P_withDSPsmall[mask],
#     color="tab:orange",
#     ls="--",
#     label="CV-QKD, with $\\tau_{DSP}=0.006$",
# )
# axins.plot(
#     dist[mask],
#     Energy_GM_Ht2P_withDSPbig[mask],
#     color="tab:orange",
#     ls="-.",
#     label="CV-QKD, with $\\tau_{DSP}=0.018$",
# )

# ax.indicate_inset_zoom(axins, edgecolor="black")

ax.set(xlabel="Distance [km]", ylabel="Energy consumption [MJ]")
ax.tick_params(axis="both", which="major")
ax.legend(loc="upper left", ncols=2)
ax.set_xlim(left=0, right=200)
ax.set_title("$N_{\\rm target} = 1$ GBit")

ax.set_yscale("log")
ax.set_ylim(top=1e6)

fig.savefig(EXPORT_DIR / "CVVSDVstudy.pdf", format="pdf")
plt.show()
