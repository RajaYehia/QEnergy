# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import matplotlib.pyplot as plt
from qenergy import components as comp
from qenergy.experiments_dv import (
    GHZsharing,
    BB84Experiment,
    EntanglementBasedExperiment,
)

import matplotlib.ticker as mticker
from studies import FIGSIZE_HALF, EXPORT_DIR

dist = range(20)
gigabit = 1e9
pcoupling = 0.9
sourcerate = 100 * 10**6
mu = 0.1
QBER = 0
parties = 5

## Laser and detectors
wavelength = 1550
laserspdc = comp.LaserMira780Pulsed()
laserBB84 = comp.LaserNKTkoheras1550()
detector = comp.DetectorSNSPD1550()
pbsm = 0.5

# Experiment instances
GHZexperiments = []
for i in dist:
    GHZexperiments.append(
        GHZsharing(
            sourcerate,
            pcoupling,
            mu,
            wavelength,
            QBER,
            laserspdc,
            parties,
            detector,
            i,
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
    sourcerate, pcoupling, mu, wavelength, QBER, laserBB84, detector, dist, otherBB84
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
    dist,
    othercomponentE91,
)

tGHZ = []
for i in range(len(GHZexperiments)):
    tGHZ.append(GHZexperiments[i].raw_time_ghz(gigabit))

tE91 = E91experiment.time_skr(gigabit)
tBB84 = BB84Experiment.time_skr(gigabit)


EnergyGHZ = []
for i in range(len(GHZexperiments)):
    EnergyGHZ.append(GHZexperiments[i].total_energy(tGHZ[i]) / 1000000000)


EnergyE91 = [parties * E91experiment.total_energy(t) / 1000000000 for t in tE91]

EnergyBB84 = [parties * BB84Experiment.total_energy(t) / 1000000000 for t in tBB84]

N = 4
fig, ax = plt.subplots(1, figsize=FIGSIZE_HALF)
plt.plot(
    dist,
    EnergyBB84,
    label="BB84-CKA ",
    linestyle="-",
    marker="P",
    markersize=N,
)
plt.plot(
    dist,
    EnergyE91,
    label="Bell-CKA ",
    linestyle="-",
    marker="o",
    markersize=N,
)
plt.plot(
    dist,
    EnergyGHZ,
    label="GHZ-CKA",
    linestyle="-",
    marker="D",
    markersize=N,
)

plt.yscale("log")
ax.set(xlabel="Distance [km]", ylabel="Energy consumption [GJ]")
ax.tick_params(axis="both", which="major")
ax.legend(loc="upper left")
ax.set_title("$N_{\\rm target} = 1$ GBit")
ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
ax.grid(True, which="both")
plt.savefig(EXPORT_DIR / "CKAstudydist.pdf", format="pdf")
plt.show()
