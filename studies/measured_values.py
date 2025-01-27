# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""This script produces a plot of the energy consumption of the BB84, E91 and MDIQKD protocol as a function of the distance, with both measured 
    values and theoretical values. 
    The components can be modified and the list of available component is in component.py"""

import matplotlib.pyplot as plt
from qenergy import components as comp
from qenergy.experiments_dv import (
    BB84Experiment,
    EntanglementBasedExperiment,
    MDIQKDExperiment,
)

from studies import FIGSIZE_HALF, EXPORT_DIR

dist = [d for d in range(120)]
gigabit = 1e9
pcoupling = 0.9
sourcerate = 80 * 10**6
mu = 0.1
muE91 = 0.1
QBER = 0.01

## Laser and detectors
wavelength = 1550
laser = comp.LaserNKTkoheras1550()
laserE91 = comp.LaserMira780Pulsed()
detector = comp.DetectorSNSPD1550()
pbsm = 0.5

# Other components
othercomponentBB84 = [
    comp.MotorizedWavePlate(),
    comp.MotorizedWavePlate(),
    comp.Computer(),
    comp.Computer(),
    comp.SwitchIntensityModulator(),
    comp.TimeTagger(),
]
othercomponentE91 = [
    comp.MotorizedWavePlate(),
    comp.MotorizedWavePlate(),
    comp.Computer(),
    comp.Computer(),
    comp.Oven(),
    comp.TimeTagger(),
    comp.TimeTagger(),
]
othercomponentMDI = [
    comp.MotorizedWavePlate(),
    comp.MotorizedWavePlate(),
    comp.Computer(),
    comp.Computer(),
    comp.SwitchIntensityModulator(),
    comp.TimeTagger(),
]

Experiment01 = BB84Experiment(
    sourcerate,
    pcoupling,
    mu,
    wavelength,
    QBER,
    laser,
    detector,
    dist,
    othercomponentBB84,
)
Experiment02 = EntanglementBasedExperiment(
    sourcerate,
    pcoupling,
    muE91,
    wavelength,
    QBER,
    laserE91,
    detector,
    detector,
    dist,
    othercomponentE91,
)
Experiment03 = MDIQKDExperiment(
    sourcerate,
    pcoupling,
    mu,
    wavelength,
    QBER,
    laser,
    laser,
    detector,
    dist,
    pbsm,
    othercomponentMDI,
)

tskr = Experiment01.time_skr(gigabit)
tskr2 = Experiment02.time_skr(gigabit)
tskr3 = Experiment03.time_skr(gigabit)

EnergyBB84 = [Experiment01.total_energy(t) / 1000000 for t in tskr]
EnergyE91 = [Experiment02.total_energy(t) / 1000000 for t in tskr2]
EnergyMDI = [Experiment03.total_energy(t) / 1000000 for t in tskr3]

EnergyBB84meas = [Experiment01.total_energy_measured(t) / 1000000 for t in tskr]
EnergyE91meas = [Experiment02.total_energy_measured(t) / 1000000 for t in tskr2]
EnergyMDImeas = [Experiment03.total_energy_measured(t) / 1000000 for t in tskr3]

fig, ax = plt.subplots(1, figsize=FIGSIZE_HALF)
ax.plot(dist, EnergyBB84, label="BB84", color="red")
ax.plot(dist, EnergyBB84meas, label="BB84 measured", linestyle="--", color="red")
ax.plot(dist, EnergyE91, label="E91", color="blue")
ax.plot(dist, EnergyE91meas, label="E91 measured", linestyle="--", color="blue")
ax.plot(dist, EnergyMDI, label="MDI", color="green")
ax.plot(dist, EnergyMDImeas, label="MDI measured", linestyle="--", color="green")

# plt.yscale("log")
ax.set(xlabel="Distance [km]", ylabel="Energy consumption [MJ]")
ax.tick_params(axis="both", which="major")
# ax.set_ylim(top=3000, bottom= 0)
ax.set_title("$N_{\\rm target} = 1$ GBit")
ax.legend(loc="upper left")
fig.savefig(EXPORT_DIR / "MeasuredValues.pdf", format="pdf")
plt.show()
