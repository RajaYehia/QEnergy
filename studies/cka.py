# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
DV CKA study.
"""

import matplotlib.pyplot as plt
from qenergy import components as comp
from qenergy.experiments_dv import (
    GHZsharing,
    BB84Experiment,
    EntanglementBasedExperiment,
)

from studies import FIGSIZE_HALF, EXPORT_DIR

dist = 5
gigabit = 1e9
pcoupling = 0.9
sourcerate = 100 * 10**6
mu = 0.1
QBER = 0
parties = range(2, 11)

## Laser and detectors
wavelength = 1550
laserspdc = comp.LaserMira780Pulsed()
laserBB84 = comp.LaserNKTkoheras1550()
detector = comp.DetectorSNSPD1550()
pbsm = 0.5

# Experiment instances
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
            dist,
            othercomponent=[],
        )
    )

otherBB84 = [
    comp.MotorizedWavePlate(),
    comp.MotorizedWavePlate(),
    comp.Computer(),
    comp.Computer(),
    comp.SwitchIntensityModulator(),
    comp.TimeTagger(),
]
BB84Experiment = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength, QBER, laserBB84, detector, [dist], otherBB84
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
E91experiment = EntanglementBasedExperiment(
    sourcerate,
    pcoupling,
    mu,
    wavelength,
    QBER,
    laserspdc,
    detector,
    detector,
    [dist],
    othercomponentE91,
)

tGHZ = []
for i in range(len(GHZexperiments)):
    tGHZ.append(GHZexperiments[i].raw_time_ghz(gigabit))

tE91 = E91experiment.time_skr(gigabit)[0]
tBB84 = BB84Experiment.time_skr(gigabit)[0]


EnergyGHZ = []
for i in range(len(GHZexperiments)):
    EnergyGHZ.append(GHZexperiments[i].total_energy(tGHZ[i]) / 1000000)


EnergyE91 = []
EnergyBB84 = []
totE91 = 0
totBB84 = 0
for i in parties:
    totE91 += E91experiment.total_energy(tE91) / 1000000
    EnergyE91.append(totE91)
    totBB84 += BB84Experiment.total_energy(tBB84) / 1000000
    EnergyBB84.append(totBB84)

N = 4
fig, ax = plt.subplots(1, figsize=FIGSIZE_HALF)
plt.plot(
    parties, EnergyBB84, label="BB84-CKA ", linestyle="-", marker="P", markersize=N
)
plt.plot(parties, EnergyE91, label="Bell-CKA ", linestyle="-", marker="o", markersize=N)
plt.plot(parties, EnergyGHZ, label="GHZ-CKA", linestyle="-", marker="D", markersize=N)

plt.xticks(parties)

plt.yscale("log")
ax.set(xlabel="Number of parties", ylabel="Energy consumption [MJ]")
ax.tick_params(axis="both", which="major")
ax.legend(loc="upper left")
ax.set_title("$N_{\\rm target} = 1$ GBit")
plt.savefig(EXPORT_DIR / "CKAstudy.pdf", format="pdf")

plt.show()
