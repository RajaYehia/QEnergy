# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Study to generate all to all entanglement.
"""

import numpy as np
import matplotlib.pyplot as plt
from qenergy import components as comp
from qenergy.experiments_dv import GHZsharing, EntanglementBasedExperiment

from studies import EXPORT_DIR, FIGSIZE_FULL

dist = 10
gigabit = 1e9
pcoupling = 0.9
sourcerate = 100 * 10**6
mu = 0.1
QBER = 0
parties = range(2, 11)

## Laser and detectors
wavelength = 1550
laserspdc = comp.LaserMira780Pulsed()
detector = comp.DetectorSNSPD1550()
pbsm = 0.5


GHZexperiments = []

for i in parties:
    GHZexperiments.append(
        GHZsharing(
            sourcerate,
            pcoupling,
            mu,
            wavelength,
            QBER,
            laserspdc,
            i,
            detector,
            np.array([dist]),
            othercomponent=[],
        )
    )

othercomponentE91 = [
    comp.MotorizedWavePlate(),
    comp.MotorizedWavePlate(),
    comp.Computer(),
    comp.Computer(),
    comp.Oven(),
    comp.TimeTagger(),
    comp.TimeTagger(),
]

E91experiments = EntanglementBasedExperiment(
    sourcerate,
    pcoupling,
    mu,
    wavelength,
    QBER,
    laserspdc,
    detector,
    detector,
    np.array([dist]),
    othercomponentE91,
)

tGHZ = []

for i in range(len(GHZexperiments)):
    tGHZ.append(GHZexperiments[i].raw_time_ghz(gigabit))

tE91 = E91experiments.time_skr(gigabit)[0]


EnergyGHZ = []
for i in range(len(GHZexperiments)):
    EnergyGHZ.append(GHZexperiments[i].total_energy(tGHZ[i]) / 1000000)


EnergyE91 = []
tot = 0
for i in parties:
    n = int(i * (i - 1) / 2)
    for i in range(n):
        tot += E91experiments.total_energy(tE91) / 1000000
    EnergyE91.append(tot)


fig, ax = plt.subplots(1, figsize=FIGSIZE_FULL)
ax.plot(
    parties,
    EnergyE91,
    label="Energy to get $10^9$ shared EPR states between all pairs of nodes ",
    linestyle="-",
    marker="s",
    markersize=5,
)
ax.plot(
    parties,
    EnergyGHZ,
    label="Energy to get $10^9$ GHZ states shared between all nodes",
    linestyle="-",
    marker="P",
    markersize=5,
)

plt.yscale("log")
ax.set(xlabel="Number of parties", ylabel="Energy consumption [MJ]")
ax.tick_params(axis="both", which="major")
ax.legend(loc="upper left")
fig.savefig(EXPORT_DIR / "AlltoAll.pdf", format="pdf")

plt.show()
