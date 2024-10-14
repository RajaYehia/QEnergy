# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Study of the energy efficiency (EE) metric with DV-QKD protocols.
"""

import matplotlib.pyplot as plt
from qenergy import components as comp
from qenergy.experiments_dv import (
    BB84Experiment,
    EntanglementBasedExperiment,
    MDIQKDExperiment,
)

from studies import FIGSIZE_FULL, EXPORT_DIR

dist = [d for d in range(120)]
petabit = 1e15
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
    comp.Computer(),
    comp.SwitchIntensityModulator(),
    comp.TimeTagger(),
]

# Detector
detectorsnspd = comp.DetectorSNSPD1550()
detectoringaas = comp.DetectorInGAs1550()

# Other components
other = [
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
# Experiment01 = BB84Experiment(sourcerate,pcoupling,mu,wavelength,0.01,laser,detectorsnspd,dist,other)
# Experiment02 = BB84Experiment(sourcerate,pcoupling,mu,wavelength,0.01,laser,detectoringaas,dist,other)
# Experiment03 = BB84Experiment(sourcerate,pcoupling,mu,wavelength,0.05,laser,detectoringaas,dist,other)

power01 = Experiment01.power()
rate01 = Experiment01.compute_secret_key_rate()
power02 = Experiment02.power()
rate02 = Experiment02.compute_secret_key_rate()
power03 = Experiment03.power()
rate03 = Experiment03.compute_secret_key_rate()
print(power01)
print(power02)
print(power03)
tskr = Experiment01.time_skr(petabit)
tskr2 = Experiment02.time_skr(petabit)
tskr3 = Experiment03.time_skr(petabit)

EnergyBB84 = [Experiment01.total_energy(t) / 1000000 for t in tskr]
EnergyE91 = [Experiment02.total_energy(t) / 1000000 for t in tskr2]
EnergyMDI = [Experiment03.total_energy(t) / 1000000 for t in tskr3]

EEBB84 = [r / power01 for r in rate01]
EEE91 = [r / power02 for r in rate02]
EEMDI = [r / power03 for r in rate03]


fig, ax1 = plt.subplots(1, figsize=FIGSIZE_FULL)
left, bottom, width, height = [0.55, 0.35, 0.38, 0.38]
ax2 = fig.add_axes([left, bottom, width, height])
ax1.plot(dist, EEBB84, label="BB84")
ax1.plot(dist, EEE91, label="E91")
ax1.plot(dist, EEMDI, label="MDI")
ax2.plot(dist, EnergyBB84, label="BB84")
ax2.plot(dist, EnergyE91, label="E91")
ax2.plot(dist, EnergyMDI, label="MDI")

ax1.set(xlabel="Distance [km]", ylabel="Energy efficiency [Rate/Watt]")
ax2.set(xlabel="Distance [km]", ylabel="$E^{\\text{1 Petabit}}$ [MJ]")
ax1.tick_params(axis="both", which="major")

ax1.legend(loc="best")
plt.savefig(EXPORT_DIR / "EE.pdf", format="pdf")
plt.show()
